import calendar
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
    year_filled = round(year_progress / 5)
    year_bar = "█" * year_filled + "░" * (20 - year_filled)
    countdown = (next_year_start.date() - now.date()).days
    month_days = calendar.monthrange(now.year, now.month)[1]
    month_progress = now.day / month_days * 100
    month_filled = round(month_progress / 5)
    month_bar = "█" * month_filled + "░" * (20 - month_filled)
    iso_week = now.isocalendar().week
    weekday_cn = ["Mon/周一", "Tue/周二", "Wed/周三", "Thu/周四", "Fri/周五", "Sat/周六", "Sun/周日"][
        now.weekday()
    ]
    focus_words = [
        "Focus: Build",
        "Focus: Learn",
        "Focus: Refine",
        "Focus: Ship",
        "Focus: Explore",
        "Focus: Simplify",
        "Focus: Improve",
    ]

    quotes = [
        line.strip()
        for line in Path(".github/readme-quotes.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    quote = quotes[(day_of_year - 1) % len(quotes)]
    focus = focus_words[(day_of_year - 1) % len(focus_words)]

    panel = "\n".join(
        [
            "<!-- daily-panel:start -->",
            "```text",
            "+------------------------------------------+",
            f"| Date      : {now.strftime('%Y/%m/%d')} {weekday_cn}",
            f"| Year      : {year_progress:6.2f}% [{year_bar}]",
            f"| Month     : {month_progress:6.2f}% [{month_bar}]",
            f"| Day       : {day_of_year:>3} / {days_in_year}    Week {iso_week}",
            f"| Countdown : {countdown:>3} days to {next_year_start.year}",
            f"| {focus}",
            f"| Quote     : {quote}",
            "+------------------------------------------+",
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
