# src/pe_orgair/schemas/sector_config.py
from __future__ import annotations

from decimal import Decimal
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SectorConfigContract(BaseModel):
    """
    Explicit contract for a sector configuration payload.
    Validates what SectorConfigService returns (deterministic + typed).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    sector_id: str = Field(..., min_length=3)
    sector_name: str = Field(..., min_length=1)
    sector_code: str = Field(..., min_length=2)

    # Keys are dimension_code like "AI_GOV", values are Decimal weights
    dimension_weights: Dict[str, Decimal]

    # Keys are calibration parameter_name like "h_r_baseline"
    calibrations: Dict[str, Decimal]

    @model_validator(mode="after")
    def _validate_constraints(self) -> "SectorConfigContract":
        # 1) weights must sum to ~1.0
        total = sum(self.dimension_weights.values(), Decimal("0"))
        if abs(total - Decimal("1.0")) > Decimal("0.001"):
            raise ValueError(f"dimension_weights must sum to 1.0 (got {total})")

        # 2) required calibration keys must exist
        required = {
            "ebitda_multiplier",
            "h_r_baseline",
            "position_factor_delta",
            "talent_concentration_threshold",
        }
        missing = required - set(self.calibrations.keys())
        if missing:
            raise ValueError(f"missing required calibrations: {sorted(missing)}")

        return self