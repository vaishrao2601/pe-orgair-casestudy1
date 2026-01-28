from pydantic import ValidationError
from pe_orgair.config.settings import Settings

def main():
    try:
        s = Settings()  # reads .env automatically
        total = sum(s.dimension_weights)
        print("✅ Settings loaded")
        print("Dimension weights:", s.dimension_weights)
        print("Sum:", total)
    except ValidationError as e:
        print("❌ Validation failed")
        print(e)

if __name__ == "__main__":
    main()