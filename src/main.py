"""Main entry point for Phase I CLI Todo Application"""
from src.cli.menu import run_menu


def main() -> None:
    """Application entry point."""
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Please restart the application.")
        exit(1)


if __name__ == "__main__":
    main()
