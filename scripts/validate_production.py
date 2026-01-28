from pydantic import ValidationError

# IMPORTANT: import the class, not the cached `settings` object
from pe_orgair.config.settings import Settings

def run_case(title: str):
    print(f"\n=== {title} ===")
    try:
        s = Settings()  # reads from .env
        print("✅ Settings loaded")
        print("APP_ENV:", s.APP_ENV)
        print("DEBUG:", s.DEBUG)
        print("OPENAI_API_KEY set?:", bool(s.OPENAI_API_KEY))
        print("ANTHROPIC_API_KEY set?:", bool(s.ANTHROPIC_API_KEY))
    except ValidationError as e:
        print("❌ ValidationError")
        print(e)

if __name__ == "__main__":
    run_case("Current .env")