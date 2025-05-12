import aiohttp
import asyncio
import argparse

def get_event_description(item: dict) -> str:
    payload = item["payload"]
    repo = item["repo"]

    event_types = {
        "CommitCommentEvent":
            f"{payload.get('action','').capitalize()} a commit comment in {repo.get('name')}",
        "CreateEvent":
            f"{payload.get('action','').capitalize()} a {payload.get('ref_type')} in {repo.get('name')}",
        "DeleteEvent":
            f"{payload.get('action','').capitalize()} a {payload.get('ref_type')} in {repo.get('name')}",
        "ForkEvent":
            f"Forked {repo.get('name')}",
        "IssueCommentEvent":
            f"{payload.get('action','').capitalize()} an issue in {repo.get('name')}",
        "IssuesEvent":
            f"{payload.get('action','').capitalize()} an issue in {repo.get('name')}",
        "MemberEvent":
            f"{payload.get('action','').capitalize()} an new member to {repo.get('name')}",
        "PublicEvent":
            f"Made {repo.get('name')} public",
        "PullRequestEvent":
            f"{payload.get('action','').capitalize()} pull request: {payload.get('number')} in {repo.get('name')}",
        "PullRequestReviewEvent":
            f"{payload.get('action','').capitalize()} a pull request review in {repo.get('name')}",
        "PullRequestReviewCommentEvent":
            f"{payload.get('action','').capitalize()} a comment in a pull request in {repo.get('name')}",
        "PullRequestReviewThreadEvent":
            f"Marked a pull request as {payload.get('action','').capitalize()} in {repo.get('name')}",
        "PushEvent":
            f"Pushed {payload.get('size')} commits to {repo.get('name')}",
        "ReleaseEvent":
            f"{payload.get('action','').capitalize()} a released in {repo.get('name')}",
        "SponsorshipEvent":
            f"{payload.get('action','').capitalize()} a sponsorship in {repo.get('name')}",
        "WatchEvent":
            f"{payload.get('action','').capitalize()} starts in {repo.get('name')}",
        "default":
            "Unknown event"
    }

    return event_types[item["type"]]

async def fetch_user_name(user_name: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.github.com/users/{user_name}/events') as response:
            return await response.json()

def parse_args() -> str:
    parser = argparse.ArgumentParser(description="Fetch github user history")
    parser.add_argument('username', type=str, help="github username")
    return parser.parse_args().username

async def fetch_and_print_user_events():
    username = parse_args()
    response = await fetch_user_name(username)
    print("Output:")
    for item in response:
        print(f"- {get_event_description(item)}")

if __name__ == "__main__":
    asyncio.run(fetch_and_print_user_events())
