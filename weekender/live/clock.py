"""3VL clock. Run by .github/workflows/clock.yml; see the notes there.
Sleeps until each event, fires it, and before the job's time limit starts a fresh copy of itself.
    python3 weekender/live/clock.py [--plan]   (--plan prints the next 24 hours of events and exits)"""
import datetime as dt, os, subprocess, sys, time
from zoneinfo import ZoneInfo
from buddy import ensure                       # the buddy restarts this clock if GitHub kills it; the clock restarts the buddy

ET = ZoneInfo("America/New_York")
SPECIALS = {(8, 0), (11, 0), (15, 0)}          # Instagram specials refresh (ET)
TICK_FROM, TICK_TO = (6, 30), (22, 0)          # site guard every 30 min in this window (ET), inclusive; 6:30 = fresh data before the 7:05 briefing
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


def guard_due(now):
    """Owner 10/12/2026 (GitHub minutes): site guard, watchdog and the events/ferry feed run every 2 hours, not every 30 min.
    6:30 AM (fresh data for the 7:05 briefing), then 9, 11 AM, 1, 3, 5, 7, 9 PM ET."""
    hm = (now.hour, now.minute)
    return hm == (6, 30) or (now.minute == 0 and now.hour % 2 == 1 and 9 <= now.hour <= 21)


def tick(now, name="tick.txt", msg="clock tick"):
    """Push data/clock/<name> to 3vl-site-guard; each file starts the workflows that watch it."""
    if not os.path.isdir(GUARD):
        sh("git clone -q --depth 1 git@github.com:threevillagelocal-cloud/3vl-site-guard.git %s" % GUARD, check=True)
        sh('git config user.name "3VL clock" && git config user.email "actions@users.noreply.github.com"', cwd=GUARD)
    for i in range(4):
        sh("git pull -q --rebase", cwd=GUARD)
        os.makedirs(os.path.join(GUARD, "data", "clock"), exist_ok=True)
        open(os.path.join(GUARD, "data", "clock", name), "w").write(now.isoformat() + "\n")
        sh("git add data/clock/%s && git commit -qm '%s %s'" % (name, msg, now.strftime("%H:%M ET")), cwd=GUARD)
        if sh("git push -q", cwd=GUARD).returncode == 0:
            print(msg, now.strftime("%H:%M")); return
        time.sleep(10)
    print(msg, "could not be pushed")


def radar(now):
    """Owner 10/17/2026 "news as it happens": news_radar.py every tick (30 min); new finds go to 3vl-site-guard
    data/news_radar/, whose news-radar-mail workflow emails the owner. Runs in this public-repo job (no extra minutes)."""
    if not os.path.isdir(GUARD):
        sh("git clone -q --depth 1 git@github.com:threevillagelocal-cloud/3vl-site-guard.git %s" % GUARD, check=True)
        sh('git config user.name "3VL clock" && git config user.email "actions@users.noreply.github.com"', cwd=GUARD)
    sh("git pull -q --rebase --autostash")                       # latest radar code without restarting the clock
    sh("git pull -q --rebase --autostash", cwd=GUARD)
    try:
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "news_radar.py"), "--guard", GUARD],
                           capture_output=True, text=True, timeout=300)
        print("radar:", (r.stdout or "").strip().splitlines()[-1:] or r.stderr[-200:])
    except subprocess.TimeoutExpired:
        print("radar: timed out"); return
    sh("git checkout -q -- weekender/live/ferry.json 2>/dev/null")  # ferry.py rewrites it; the events feed job owns it
    if sh("git status --porcelain data/news_radar", cwd=GUARD).stdout.strip():
        sh("git add data/news_radar && git commit -qm 'news radar %s'" % now.strftime("%H:%M ET"), cwd=GUARD)
        for i in range(4):
            if sh("git push -q", cwd=GUARD).returncode == 0:
                return
            sh("git pull -q --rebase --autostash", cwd=GUARD); time.sleep(5)
        print("radar: could not push")


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
    ensure("clock-buddy.yml")
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
            if now.weekday() == 4 and (now.hour, now.minute) == (7, 0):   # owner 10/16/2026: weekly email preview Fri 7 AM (GitHub's cron runs hours late)
                tick(now, "weekly.txt", "weekly email build")
            if guard_due(now):   # owner 10/12/2026: site guard, watchdog AND events/ferry feed every 2 hours
                tick(now)
                sh("gh workflow run events-live.yml -R %s" % REPO, check=True)   # events feed + Port Jefferson Ferry alerts
            try:
                radar(now)
            except Exception as e:                    # the radar must never stop the clock
                print("radar error:", type(e).__name__)
            ensure("clock-buddy.yml")
    if time.time() - start < 600:                  # safety: never restart in a tight loop; the hourly cron picks it up
        print("run ended after %d s: not restarting" % (time.time() - start)); return
    r = sh("gh workflow run clock.yml -R %s" % REPO, check=True)
    print("next clock started" if r.returncode == 0 else "could not restart the clock (the hourly cron will)")


if __name__ == "__main__":
    main()
