"""Score workstation health 0-100 from a simple metrics CSV.

Usage: python3 main.py hosts.csv
CSV columns: host,disk_free_pct,cpu_idle_pct,pending_updates,last_reboot_days
Score starts at 100 and loses points: disk under 20% free (-20, under
10% -30), CPU idle under 20% (-15), each pending update -2 (max -20),
no reboot in 30+ days (-10). Verdict: HEALTHY >= 80, REVIEW 60-79,
ACTION below 60.
"""
import argparse, csv, sys


def score(row):
    points = 100
    disk = float(row["disk_free_pct"])
    if disk < 10:
        points -= 30
    elif disk < 20:
        points -= 20
    if float(row["cpu_idle_pct"]) < 20:
        points -= 15
    points -= min(20, 2 * int(row["pending_updates"]))
    if int(row["last_reboot_days"]) >= 30:
        points -= 10
    points = max(0, points)
    verdict = "HEALTHY" if points >= 80 else ("REVIEW" if points >= 60 else "ACTION")
    return points, verdict


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    action = 0
    with open(args.path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            points, verdict = score(row)
            if verdict == "ACTION":
                action += 1
            print(f"{row['host']}: {points}/100 {verdict}")
    print(f"{action} host(s) needing action.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
