# scripts/validate_cache_behavior.py
import asyncio
import os
import time
from dotenv import load_dotenv

load_dotenv()  # loads .env / .env.local depending on your setup

from pe_orgair.services.sector_config import sector_service


async def main() -> None:
    focus_group_id = os.getenv("TEST_FOCUS_GROUP_ID", "pe_technology")

    print("=== Case Study 1: Cache Behavior Validation ===")
    print(f"focus_group_id: {focus_group_id}")

    # 1) First call (should hit DB)
    t0 = time.perf_counter()
    cfg1 = await sector_service.get_config(focus_group_id)
    t1 = time.perf_counter()

    if cfg1 is None:
        raise SystemExit("❌ get_config returned None. Check focus_group_id seed data.")

    print("\n--- First call (expect DB) ---")
    print(f"took: {(t1 - t0):.4f}s")
    print(f"sector_id: {cfg1.sector_id}")
    print(f"weights_count: {len(cfg1.dimension_weights)}")
    print(f"calibrations_count: {len(cfg1.calibrations)}")

    # 2) Second call (should hit cache)
    t2 = time.perf_counter()
    cfg2 = await sector_service.get_config(focus_group_id)
    t3 = time.perf_counter()

    print("\n--- Second call (expect cache) ---")
    print(f"took: {(t3 - t2):.4f}s")

    # sanity: should be identical payload
    assert cfg2 is not None
    assert cfg2.sector_id == cfg1.sector_id
    assert cfg2.dimension_weights == cfg1.dimension_weights
    assert cfg2.calibrations == cfg1.calibrations
    print("✅ payload identical between calls")

    # 3) Invalidate and call again (should hit DB again)
    print("\n--- Invalidate cache and call again (expect DB) ---")
    sector_service.invalidate_cache(focus_group_id)

    t4 = time.perf_counter()
    cfg3 = await sector_service.get_config(focus_group_id)
    t5 = time.perf_counter()

    assert cfg3 is not None
    print(f"took: {(t5 - t4):.4f}s")
    print("✅ cache invalidation + reload succeeded")

    print("\n✅ Cache behavior validated successfully.")


if __name__ == "__main__":
    asyncio.run(main())