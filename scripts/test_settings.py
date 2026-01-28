from pe_orgair.config.settings import settings

print("APP_ENV:", settings.APP_ENV)
print("DEBUG:", settings.DEBUG)
print("LOG_LEVEL:", settings.LOG_LEVEL)
print("SNOWFLAKE_ACCOUNT:", settings.SNOWFLAKE_ACCOUNT)
print("Dimension weights sum:", sum(settings.dimension_weights))