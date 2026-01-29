# src/pe_orgair/services/sector_config.py
"""Sector configuration service with caching + explicit contract validation."""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List, Optional

import structlog
from pydantic import ValidationError

from pe_orgair.db.snowflake import db
from pe_orgair.infrastructure.cache import cache
from pe_orgair.schemas.sector_config import SectorConfigContract

logger = structlog.get_logger()


@dataclass
class SectorConfig:
    """Internal configuration representation for a PE sector."""
    focus_group_id: str
    group_name: str
    group_code: str
    dimension_weights: Dict[str, Decimal] = field(default_factory=dict)
    calibrations: Dict[str, Decimal] = field(default_factory=dict)

    @property
    def h_r_baseline(self) -> Decimal:
        return self.calibrations.get("h_r_baseline", Decimal("75"))

    @property
    def ebitda_multiplier(self) -> Decimal:
        return self.calibrations.get("ebitda_multiplier", Decimal("1.0"))

    @property
    def position_factor_delta(self) -> Decimal:
        return self.calibrations.get("position_factor_delta", Decimal("0.15"))

    @property
    def talent_concentration_threshold(self) -> Decimal:
        return self.calibrations.get("talent_concentration_threshold", Decimal("0.25"))

    def get_dimension_weight(self, dimension_code: str) -> Decimal:
        return self.dimension_weights.get(dimension_code, Decimal("0"))

    def validate_weights_sum(self) -> bool:
        total = sum(self.dimension_weights.values()) if self.dimension_weights else Decimal("0")
        return abs(total - Decimal("1.0")) < Decimal("0.001")


class SectorConfigService:
    """Service for loading and caching sector configurations."""

    CACHE_KEY_SECTOR = "sector:{focus_group_id}"
    CACHE_KEY_ALL = "sectors:all"
    CACHE_TTL = 3600  # 1 hour

    async def get_config(self, focus_group_id: str) -> Optional[SectorConfigContract]:
        """Get configuration for a single sector (validated contract)."""
        cache_key = self.CACHE_KEY_SECTOR.format(focus_group_id=focus_group_id)

        cached = cache.get(cache_key)
        if cached:
            cfg = self._dict_to_config(cached)
            return self._to_contract(cfg)

        cfg = await self._load_from_db(focus_group_id)
        if not cfg:
            return None

        cache.set(cache_key, self._config_to_dict(cfg), self.CACHE_TTL)
        return self._to_contract(cfg)

    async def get_all_configs(self) -> List[SectorConfigContract]:
        """Get all sector configurations (validated contract)."""
        cache_key = self.CACHE_KEY_ALL

        cached = cache.get(cache_key)
        if cached:
            return [self._to_contract(self._dict_to_config(c)) for c in cached]

        cfgs = await self._load_all_from_db()
        cache.set(cache_key, [self._config_to_dict(c) for c in cfgs], self.CACHE_TTL)
        return [self._to_contract(c) for c in cfgs]

    async def _load_from_db(self, focus_group_id: str) -> Optional[SectorConfig]:
        """Load a single configuration from database.

        Behavior:
        - Unknown focus_group_id => return None
        - DB/infra issues => log + return None (keeps negative tests deterministic)
        """
        try:
            # 1) Base focus group
            fg_query = """
                SELECT focus_group_id, group_name, group_code
                FROM focus_groups
                WHERE focus_group_id = %(focus_group_id)s
                  AND platform = 'pe_org_air'
                  AND is_active = TRUE
            """
            fg_row = db.fetch_one(fg_query, {"focus_group_id": focus_group_id})
            if not fg_row:
                return None

            # 2) Dimension weights
            weights_query = """
                SELECT d.dimension_code, w.weight
                FROM focus_group_dimension_weights w
                JOIN dimensions d ON w.dimension_id = d.dimension_id
                WHERE w.focus_group_id = %(focus_group_id)s
                  AND w.is_current = TRUE
                ORDER BY d.display_order
            """
            weights_rows = db.fetch_all(weights_query, {"focus_group_id": focus_group_id})
            dimension_weights = {
                row["dimension_code"]: Decimal(str(row["weight"]))
                for row in weights_rows
            }

            # 3) Calibrations
            calib_query = """
                SELECT parameter_name, parameter_value
                FROM focus_group_calibrations
                WHERE focus_group_id = %(focus_group_id)s
                  AND is_current = TRUE
            """
            calib_rows = db.fetch_all(calib_query, {"focus_group_id": focus_group_id})
            calibrations = {
                row["parameter_name"]: Decimal(str(row["parameter_value"]))
                for row in calib_rows
            }

        except RuntimeError as e:
            # Example: "DATABASE_URL not set in environment/.env"
            logger.warning(
                "sector_config_db_unavailable",
                focus_group_id=focus_group_id,
                error=str(e),
            )
            return None
        except Exception as e:
            logger.exception(
                "sector_config_db_error",
                focus_group_id=focus_group_id,
                error=str(e),
            )
            return None

        cfg = SectorConfig(
            focus_group_id=fg_row["focus_group_id"],
            group_name=fg_row["group_name"],
            group_code=fg_row["group_code"],
            dimension_weights=dimension_weights,
            calibrations=calibrations,
        )

        if not cfg.validate_weights_sum():
            logger.warning("invalid_weights_sum", focus_group_id=focus_group_id)

        # Deterministic contract validation (case study requirement)
        self._validate_contract(cfg)

        return cfg

    async def _load_all_from_db(self) -> List[SectorConfig]:
        """Load all sector configurations from database."""
        try:
            fg_query = """
                SELECT focus_group_id
                FROM focus_groups
                WHERE platform = 'pe_org_air'
                  AND is_active = TRUE
                ORDER BY display_order
            """
            fg_rows = db.fetch_all(fg_query)
        except RuntimeError as e:
            logger.warning("sector_configs_db_unavailable", error=str(e))
            return []
        except Exception as e:
            logger.exception("sector_configs_db_error", error=str(e))
            return []

        cfgs: List[SectorConfig] = []
        for row in fg_rows:
            cfg = await self._load_from_db(row["focus_group_id"])
            if cfg:
                cfgs.append(cfg)
        return cfgs

    def _validate_contract(self, cfg: SectorConfig) -> None:
        payload = {
            "sector_id": cfg.focus_group_id,
            "sector_name": cfg.group_name,
            "sector_code": cfg.group_code,
            "dimension_weights": cfg.dimension_weights,
            "calibrations": cfg.calibrations,
        }
        try:
            SectorConfigContract.model_validate(payload)
        except ValidationError as e:
            logger.error(
                "sector_config_contract_invalid",
                focus_group_id=cfg.focus_group_id,
                errors=e.errors(),
            )
            raise

    def _to_contract(self, cfg: SectorConfig) -> SectorConfigContract:
        """Convert internal dataclass to validated contract model."""
        payload = {
            "sector_id": cfg.focus_group_id,
            "sector_name": cfg.group_name,
            "sector_code": cfg.group_code,
            "dimension_weights": cfg.dimension_weights,
            "calibrations": cfg.calibrations,
        }
        return SectorConfigContract.model_validate(payload)

    def _config_to_dict(self, cfg: SectorConfig) -> dict:
        """Convert config to dict for caching."""
        return {
            "focus_group_id": cfg.focus_group_id,
            "group_name": cfg.group_name,
            "group_code": cfg.group_code,
            "dimension_weights": {k: str(v) for k, v in cfg.dimension_weights.items()},
            "calibrations": {k: str(v) for k, v in cfg.calibrations.items()},
        }

    def _dict_to_config(self, data: dict) -> SectorConfig:
        """Convert cached dict to internal config."""
        return SectorConfig(
            focus_group_id=data["focus_group_id"],
            group_name=data["group_name"],
            group_code=data["group_code"],
            dimension_weights={k: Decimal(v) for k, v in data["dimension_weights"].items()},
            calibrations={k: Decimal(v) for k, v in data["calibrations"].items()},
        )

    def invalidate_cache(self, focus_group_id: Optional[str] = None) -> None:
        """Invalidate cached configurations."""
        if focus_group_id:
            cache.delete(self.CACHE_KEY_SECTOR.format(focus_group_id=focus_group_id))
        cache.invalidate_pattern("sectors:*")
        logger.info("sector_cache_invalidated", focus_group_id=focus_group_id)


# Singleton instance
sector_service = SectorConfigService()