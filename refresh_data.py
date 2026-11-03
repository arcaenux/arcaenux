#!/usr/bin/env python3
"""Refresh the ARCAENUX data snapshots, then rebuild every SVG.

Requires the GitHub CLI (`gh`) to be authenticated as the profile owner.

Run:
    python refresh_data.py

This updates:
    data/contributions.json   the last year of contribution counts
    data/repos.json           public repositories + aggregated language bytes
    assets/*.svg              header, pulse, spectrum, layers, divider, footer

Then commit the changes:
    git add -A && git commit -m "Refresh profile assets" && git push
"""
import collections
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGIN = "arcaenux"


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


def main():
    query = (
        "query { user(login: \"%s\") { login name contributionsCollection { "
        "contributionCalendar { totalContributions weeks { contributionDays { "
        "date contributionCount } } } } } }" % LOGIN
    )
    raw = json.loads(gh("api", "graphql", "-f", "query=" + query))["data"]["user"]
    calendar = raw["contributionsCollection"]["contributionCalendar"]
    days = [day for week in calendar["weeks"] for day in week["contributionDays"]]
    contributions = {
        "login": raw["login"],
        "name": raw["name"],
        "total": calendar["totalContributions"],
        "start": days[0]["date"],
        "end": days[-1]["date"],
        "days": [
            {"date": day["date"], "count": day["contributionCount"]} for day in days
        ],
    }

    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", "contributions.json"), "w", encoding="utf-8") as handle:
        json.dump(contributions, handle, indent=2)

    repos = json.loads(gh("api", f"users/{LOGIN}/repos?per_page=100&sort=pushed"))
    repos = [repo for repo in repos if not repo["fork"]]
    languages = collections.Counter()
    metadata = []
    for repo in repos:
        try:
            counts = json.loads(gh("api", f"repos/{LOGIN}/{repo['name']}/languages"))
        except subprocess.CalledProcessError:
            counts = {}
        languages.update(counts)
        metadata.append(
            {
                "name": repo["name"],
                "description": repo.get("description") or "",
                "stars": repo["stargazers_count"],
                "language": repo.get("language") or "",
                "pushed": repo["pushed_at"],
                "url": repo["html_url"],
                "topics": repo.get("topics", []),
            }
        )
    metadata.sort(key=lambda item: item["pushed"], reverse=True)
    with open(os.path.join(ROOT, "data", "repos.json"), "w", encoding="utf-8") as handle:
        json.dump({"repos": metadata, "languages": dict(languages)}, handle, indent=2)

    print(f"contributions: {contributions['total']} across {len(days)} days")
    print(f"repos:         {len(metadata)}")
    print(f"languages:     {len(languages)}")
    subprocess.check_call(["python", os.path.join(ROOT, "build_assets.py")])


if __name__ == "__main__":
    main()
