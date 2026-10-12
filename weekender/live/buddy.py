"""3VL clock buddy. Run by .github/workflows/clock-buddy.yml.
GitHub sometimes kills a runner mid-job (10/12/2026: the clock died at 8:53 AM ET and nothing restarted it for 80 min,
because the hourly cron backup runs hours late). The buddy stays awake next to the clock and restarts it within
CHECK seconds if no clock run is running or queued. The clock does the same for the buddy on every tick.
    python3 weekender/live/buddy.py"""
import os, subprocess, time

CHECK = 5 * 60
RUN_FOR = 5 * 3600 + 35 * 60                   # leave room under the 355-minute job limit
REPO = os.environ.get("GITHUB_REPOSITORY", "threevillagelocal-cloud/3vl-assets")


def alive(workflow):
    """True if the workflow has a run in progress, queued or waiting (or the check itself failed: never restart blind)."""
    for status in ("in_progress", "queued", "waiting", "pending"):
        r = subprocess.run("gh run list -R %s -w %s -s %s -L 1 --json databaseId -q length" % (REPO, workflow, status),
                           shell=True, capture_output=True, text=True)
        if r.returncode:
            print("could not check", workflow, r.stderr[-300:]); return True
        if r.stdout.strip() not in ("", "0"):
            return True
    return False


def ensure(workflow):
    if not alive(workflow):
        r = subprocess.run("gh workflow run %s -R %s" % (workflow, REPO), shell=True, capture_output=True, text=True)
        print(time.strftime("%H:%M UTC"), workflow, "was not running:", "restarted" if r.returncode == 0 else "RESTART FAILED " + r.stderr[-300:])


def main():
    start = time.time()
    while time.time() - start < RUN_FOR:
        ensure("clock.yml")
        time.sleep(CHECK)
    subprocess.run("gh workflow run clock-buddy.yml -R %s" % REPO, shell=True)
    print("next buddy started")


if __name__ == "__main__":
    main()
