import asyncio
from gactivity import activity

def main():
    asyncio.run(activity.fetch_and_print_user_events())


if __name__ == "__main__":
    main()