from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def main() -> None:
    tz = ZoneInfo("Asia/Shanghai")
    now = datetime.now(tz)
    year_start = datetime(now.year, 1, 1, tzinfo=tz)
    next_year_start = datetime(now.year + 1, 1, 1, tzinfo=tz)
    days_in_year = (next_year_start - year_start).days
    day_of_year = now.timetuple().tm_yday
    year_progress = day_of_year / days_in_year * 100
    filled = round(year_progress / 5)
    bar = "█" * filled + "░" * (20 - filled)
    countdown = (next_year_start.date() - now.date()).days

    quotes = [
        line.strip()
        for line in Path(".github/readme-quotes.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    quote = quotes[(day_of_year - 1) % len(quotes)]

    panel = "\n".join(
        [
            "<!-- daily-panel:start -->",
            "```text",
            f"Date: {now.strftime('%Y/%m/%d %A')}",
            f"Year Progress: {year_progress:.2f}% [{bar}]",
            f"Day: {day_of_year} / {days_in_year}",
            f"Countdown to {next_year_start.year}: {countdown} days",
            f"Quote: {quote}",
            "```",
            "<!-- daily-panel:end -->",
        ]
    )

    readme = Path("README.md")
    content = readme.read_text(encoding="utf-8")
    start_marker = "<!-- daily-panel:start -->"
    end_marker = "<!-- daily-panel:end -->"

    if start_marker in content and end_marker in content:
        start = content.index(start_marker)
        end = content.index(end_marker) + len(end_marker)
        content = content[:start] + panel + content[end:]
    else:
        content = panel + "\n\n" + content

    readme.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")


if __name__ == "__main__":
    main()
