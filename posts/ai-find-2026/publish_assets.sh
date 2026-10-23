# Copy aif.css/aif.js to 3vl-share/ai-find and push (GitHub Pages serves them in ~1 min; browsers may cache 10 min)
cd "$(dirname "$0")"
cp aif.css aif.js ~/Documents/3vl-share/ai-find/
cd ~/Documents/3vl-share && git add ai-find && git commit -qm "ai-find assets" && git stash -q; git pull -q --rebase && git push -q; git stash pop -q; git log --oneline -1
