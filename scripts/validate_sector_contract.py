"""
Case Study 1 – Sector Configuration Contract Validation

This script validates that a PE sector configuration can be
loaded deterministically from the platform foundation.
"""
from dotenv import load_dotenv
load_dotenv()

import asyncio
from decimal import Decimal

from pe_orgair.services.sector_config import sector_service


async def main():
    focus_group_id = "pe_technology"

    print("\n=== Case Study 1: Sector Configuration Contract ===\n")

    config = await sector_service.get_config(focus_group_id)

    if not config:
        raise RuntimeError(f"Sector config not found for {focus_group_id}")

    # Basic identity checks
    print(f"Sector ID      : {config.sector_id}")
    print(f"Sector Name    : {config.sector_name}")
    print(f"Sector Code    : {config.sector_code}")

    # Dimension contract
    dimension_count = len(config.dimension_weights)
    weights_sum = sum(config.dimension_weights.values())

    print(f"\nDimensions Loaded : {dimension_count}")
    print(f"Weight Sum       : {weights_sum}")

    if abs(weights_sum - Decimal("1.0")) > Decimal("0.001"):
        raise ValueError("❌ Dimension weights do not sum to 1.0")

    # Calibration contract
    print("\nCalibration Parameters:")
    for key in sorted(config.calibrations.keys()):
        print(f"  - {key}")

    print("\n✅ Sector configuration contract validated successfully.\n")


if __name__ == "__main__":
    asyncio.run(main())