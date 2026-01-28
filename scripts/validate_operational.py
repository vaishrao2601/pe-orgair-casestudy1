from pe_orgair.config.settings import get_settings

def main():
    # IMPORTANT: reload settings each run (so .env changes take effect)
    get_settings.cache_clear()
    settings = get_settings()

    print("RATE_LIMIT_PER_MINUTE:", settings.RATE_LIMIT_PER_MINUTE)
    print("DAILY_COST_BUDGET_USD:", settings.DAILY_COST_BUDGET_USD)
    print("COST_ALERT_THRESHOLD_PCT:", settings.COST_ALERT_THRESHOLD_PCT)
    print("HITL_SCORE_CHANGE_THRESHOLD:", settings.HITL_SCORE_CHANGE_THRESHOLD)
    print("HITL_EBITDA_PROJECTION_THRESHOLD:", settings.HITL_EBITDA_PROJECTION_THRESHOLD)
    print("ALPHA_VR_WEIGHT:", settings.ALPHA_VR_WEIGHT)
    print("BETA_SYNERGY_WEIGHT:", settings.BETA_SYNERGY_WEIGHT)
    print("LAMBDA_PENALTY:", settings.LAMBDA_PENALTY)
    print("DELTA_POSITION:", settings.DELTA_POSITION)

    print("\n✅ All settings loaded successfully (validation passed).")

if __name__ == "__main__":
    main()