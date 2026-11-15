# Copy ais.css/ais.js/img + share images to 3vl-share/ai-5-ways and push (GitHub Pages serves them in ~1 min)
cd "$(dirname "$0")"
D=~/Documents/3vl-share/ai-5-ways
mkdir -p $D/img/logos
cp ais.css ais.js $D/ && cp img/*.webp $D/img/ && cp img/logos/*.svg $D/img/logos/ && cp share/out/ai-5-ways-li-business-og.jpg share/out/ai-5-ways-li-business-ig.jpg $D/
cd ~/Documents/3vl-share && git add ai-5-ways && git commit -qm "ai-5-ways article assets" && git stash -q; git pull -q --rebase && git push -q; git stash pop -q; git log --oneline -1
