import asyncio
import time
from dotenv import load_dotenv
load_dotenv()
from pe_orgair.services.sector_config import sector_service

async def main():
    focus_group_id = "pe_technology"   # change to pe_manufacturing if you seeded that

    print("\n--- First call (should hit DB) ---")
    t0 = time.time()
    cfg1 = await sector_service.get_config(focus_group_id)
    t1 = time.time()

    if not cfg1:
        print("❌ No config returned. Check focus_group_id exists in focus_groups.")
        return

    print("✅ focus_group_id:", cfg1.focus_group_id)
    print("✅ group_name:", cfg1.group_name)
    print("✅ group_code:", cfg1.group_code)
    print("✅ weights:", cfg1.dimension_weights)
    print("✅ calibrations:", cfg1.calibrations)
    print("✅ weights_sum_ok:", cfg1.validate_weights_sum())
    print("✅ h_r_baseline:", cfg1.h_r_baseline)
    print("✅ ebitda_multiplier:", cfg1.ebitda_multiplier)

    print(f"⏱️ first call time: {(t1 - t0):.4f}s")

    print("\n--- Second call (should hit cache) ---")
    t2 = time.time()
    cfg2 = await sector_service.get_config(focus_group_id)
    t3 = time.time()
    print(f"⏱️ second call time: {(t3 - t2):.4f}s")

    # Optional: force cache invalidation and load again
    print("\n--- Invalidate cache and call again (should hit DB again) ---")
    sector_service.invalidate_cache(focus_group_id)
    t4 = time.time()
    cfg3 = await sector_service.get_config(focus_group_id)
    t5 = time.time()
    print(f"⏱️ after invalidation call time: {(t5 - t4):.4f}s")

if __name__ == "__main__":
    asyncio.run(main())