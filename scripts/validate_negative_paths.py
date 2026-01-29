"""
Case Study 1 - Step 1.4.2
Negative-path validation:
- Prove contract fails when weights don't sum to 1.0
- Prove contract fails when required calibration keys are missing
- Prove service returns None for unknown sector_id
"""

from __future__ import annotations

import asyncio
from decimal import Decimal

from pydantic import ValidationError

from pe_orgair.schemas.sector_config import SectorConfigContract
from pe_orgair.services.sector_config import sector_service


def expect_validation_error(label: str, payload: dict) -> None:
    try:
        SectorConfigContract.model_validate(payload)
        raise AssertionError(f"[FAIL] {label}: expected ValidationError but got success")
    except ValidationError:
        print(f"✅ [PASS] {label}: ValidationError raised as expected")


async def main() -> None:
    print("\n=== Case Study 1: Negative Path Validation ===\n")

    # Base "good" payload skeleton (we will tweak it)
    good_payload = {
        "sector_id": "pe_technology",
        "sector_name": "Technology",
        "sector_code": "TECHNOLOGY",
        "dimension_weights": {
            "AI_GOV": Decimal("0.15"),
            "TECH_STACK": Decimal("0.30"),
            "TALENT": Decimal("0.20"),
            "LEADERSHIP": Decimal("0.10"),
            "USE_CASES": Decimal("0.15"),
            "CULTURE": Decimal("0.10"),
        },
        "calibrations": {
            "ebitda_multiplier": Decimal("1.40"),
            "h_r_baseline": Decimal("80.00"),
            "position_factor_delta": Decimal("0.18"),
            "talent_concentration_threshold": Decimal("0.25"),
        },
    }

    # 1) weights sum wrong
    bad_weights = dict(good_payload)
    bad_weights["dimension_weights"] = dict(good_payload["dimension_weights"])
    bad_weights["dimension_weights"]["CULTURE"] = Decimal("0.50")  # now sum > 1.0
    expect_validation_error("weights sum != 1.0", bad_weights)

    # 2) missing required calibrations
    bad_calibs = dict(good_payload)
    bad_calibs["calibrations"] = dict(good_payload["calibrations"])
    bad_calibs["calibrations"].pop("h_r_baseline")
    expect_validation_error("missing required calibration key", bad_calibs)

    # 3) unknown sector id should return None from service
    unknown_id = "pe_does_not_exist"
    cfg = await sector_service.get_config(unknown_id)
    if cfg is None:
        print(f"✅ [PASS] unknown sector_id returns None: {unknown_id}")
    else:
        raise AssertionError(f"[FAIL] expected None for unknown id, got: {cfg}")

    print("\n✅ Negative-path validation complete.\n")


if __name__ == "__main__":
    asyncio.run(main())