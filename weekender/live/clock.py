"""3VL clock. Run by .github/workflows/clock.yml; see the notes there.
Sleeps until each event, fires it, and before the job's time limit starts a fresh copy of itself.
    python3 weekender/live/clock.py [--plan]   (--plan prints the next 24 hours of events and exits)"""
import datetime as dt, os, subprocess, sys, time
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
SPECIALS = {(8, 0), (11, 0), (15, 0)}          # Instagram specials refresh (ET)
TICK_FROM, TICK_TO = (7, 0), (22, 0)           # site guard every 30 min in this window (ET), inclusive
RUN_FOR = 5 * 3600 + 35 * 60                   # leave room under the 355-minute job limit
REPO = os.environ.get("GITHUB_REPOSITORY", "threevillagelocal-cloud/3vl-assets")
GUARD = "/tmp/guard"
SSH = "ssh -i ~/.ssh/guard -o StrictHostKeyChecking=accept-new"


def events_after(t):
    """The next event time after t (ET) and what to do then."""
    t = t.astimezone(ET).replace(second=0, microsecond=0)
    nxt = t + dt.timedelta(minutes=30 - t.minute % 30)
    while True:
        hm = (nxt.hour, nxt.minute)
        acts = []
        if hm in SPECIALS:
            acts.append("specials")
        if TICK_FROM <= hm <= TICK_TO:
            acts.append("tick")
        if acts:
            return nxt, acts
        nxt += dt.timedelta(minutes=30)


def sh(cmd, cwd=None, check=False):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, env=dict(os.environ, GIT_SSH_COMMAND=SSH))
    if r.returncode and check:
        print("FAILED:", cmd, r.stdout[-400:], r.stderr[-400:])
    return r


def specials():
    r = sh("gh workflow run ig-specials.yml -R %s" % REPO, check=True)
    print("specials started" if r.returncode == 0 else "specials could not start")


def tick(now):
    if not os.path.isdir(GUARD):
        sh("git clone -q --depth 1 git@github.com:threevillagelocal-cloud/3vl-site-guard.git %s" % GUARD, check=True)
        sh('git config user.name "3VL clock" && git config user.email "actions@users.noreply.github.com"', cwd=GUARD)
    for i in range(4):
        sh("git pull -q --rebase", cwd=GUARD)
        os.makedirs(os.path.join(GUARD, "data", "clock"), exist_ok=True)
        open(os.path.join(GUARD, "data", "clock", "tick.txt"), "w").write(now.isoformat() + "\n")
        sh("git add data/clock/tick.txt && git commit -qm 'clock tick %s'" % now.strftime("%H:%M ET"), cwd=GUARD)
        if sh("git push -q", cwd=GUARD).returncode == 0:
            print("tick", now.strftime("%H:%M")); return
        time.sleep(10)
    print("tick could not be pushed")


def catch_up(now):
    """A restarted clock runs a missed specials refresh right away (last run > 4.5 h ago, daytime)."""
    if not ((7, 30) <= (now.hour, now.minute) <= (21, 0)):
        return
    r = sh("gh run list -R %s -w ig-specials.yml -L 1 --json createdAt -q '.[0].createdAt'" % REPO)
    try:
        last = dt.datetime.fromisoformat(r.stdout.strip().replace("Z", "+00:00"))
    except ValueError:
        return
    if (dt.datetime.now(dt.timezone.utc) - last).total_seconds() > 4.5 * 3600:
        print("specials last ran", last.isoformat(), "- catching up"); specials()


def main():
    if "--plan" in sys.argv:
        t = dt.datetime.now(ET)
        for _ in range(48):
            t, acts = events_after(t); print(t.strftime("%a %H:%M"), acts)
            if t > dt.datetime.now(ET) + dt.timedelta(hours=24):
                break
        return
    start = time.time()
    catch_up(dt.datetime.now(ET))
    while True:
        at, acts = events_after(dt.datetime.now(ET))
        if at.timestamp() - start > RUN_FOR:      # next event is past this run's lifetime (overnight): wait out the run, then hand over
            time.sleep(max(0, start + RUN_FOR - time.time()))
            break
        time.sleep(max(0, at.timestamp() - time.time()))
        now = dt.datetime.now(ET)
        if "specials" in acts:
            specials()
        if "tick" in acts:
            tick(now)
    if time.time() - start < 600:                  # safety: never restart in a tight loop; the hourly cron picks it up
        print("run ended after %d s: not restarting" % (time.time() - start)); return
    r = sh("gh workflow run clock.yml -R %s" % REPO, check=True)
    print("next clock started" if r.returncode == 0 else "could not restart the clock (the hourly cron will)")


if __name__ == "__main__":
    main()
