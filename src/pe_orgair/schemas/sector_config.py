# src/pe_orgair/schemas/sector_config.py
from __future__ import annotations

from decimal import Decimal
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field


class SectorConfigContract(BaseModel):
    """
    Explicit contract for a sector configuration payload.
    Used to validate what SectorConfigService returns (deterministic + typed).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    sector_id: str = Field(..., min_length=3)
    sector_name: str = Field(..., min_length=1)
    sector_code: str = Field(..., min_length=2)

    # Keys are dimension_code like "AI_GOV", values are Decimal weights
    dimension_weights: Dict[str, Decimal]

    # Keys are calibration parameter_name like "h_r_baseline"
    calibrations: Dict[str, Decimal]