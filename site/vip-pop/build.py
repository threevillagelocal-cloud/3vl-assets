"""Reusable VIP popup.
Same popup as the VIP card's "See everything you get" on /join, packaged so ANY page on threevillagelocal.com can open it.

    python site/vip-pop/build.py      -> writes 3vl-share/site/vip-pop/pop.js (public, GitHub Pages)

How a page uses it (needs LOADER once on the page, e.g. sitewide footer):
    <a href="/join#plan-vip" data-vip-pop>See what VIPs get</a>
    data-vip-go="dash" (optional) opens straight to a section: profile, dash, vip, seen, perks
Without JS the link still goes to /join#plan-vip, which opens the same popup there.
"""
import importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.expanduser("~"), "Documents", "3vl-share", "site", "vip-pop")
URL = "https://threevillagelocal-cloud.github.io/3vl-share/site/vip-pop/pop.js"

sys.argv = [sys.argv[0]]   # join builder reads flags at import; we only borrow its pieces
spec = importlib.util.spec_from_file_location("joinb", os.path.join(HERE, "..", "join-v2", "build.py"))
J = importlib.util.module_from_spec(spec); spec.loader.exec_module(J)

# small, sitewide: loads the popup only on first click (zero cost on normal page views)
LOADER = ('<script>(function(){if(window.__vpL)return;window.__vpL=1;function go(t){var k=t&&t.getAttribute("data-vip-go");'
          'if(window.jvOpen)return window.jvOpen("vip",k,t);var s=document.createElement("script");s.src="%s?v=V";'
          's.onload=function(){window.jvOpen&&window.jvOpen("vip",k,t);};document.head.appendChild(s);}'
          'document.addEventListener("click",function(e){var t=e.target.closest&&e.target.closest("[data-vip-pop]");'
          'if(!t||document.getElementById("jv"))return;e.preventDefault();go(t);},true);})();</script>') % URL


def main():
    if not J.PARTNER_ON:
        J._partner_off()
    html = J.nowrap_hyphens(J.sprite() + J.modal_tpl("vip"))
    css = open(os.path.join(HERE, "..", "join-v2", "page.css"), encoding="utf-8").read()
    js = open(os.path.join(HERE, "..", "join-v2", "page.js"), encoding="utf-8").read()
    for nm, s in (("html", html), ("css", css)):
        assert "—" not in s and "&mdash;" not in s and "–" not in s, nm + " has an em/en dash"
    out = ("/* 3VL VIP popup - built by 3vl-assets/site/vip-pop/build.py from the /join page. Do not edit by hand. */\n"
           "(function(){if(window.jvOpen||document.getElementById('jv'))return;\n"
           "var st=document.createElement('style');st.textContent=" + json.dumps(css) + ";document.head.appendChild(st);\n"
           "var d=document.createElement('div');d.id='jv';d.setAttribute('aria-hidden','true');d.style.cssText='display:none!important';d.innerHTML="
           + json.dumps(html) + ";document.body.appendChild(d);\n})();\n" + js +
           "\ntry{if(window.gtag)gtag('event','vip_popup_open_elsewhere',{page:location.pathname});}catch(x){}\n")
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "pop.js"), "w", encoding="utf-8").write(out)
    open(os.path.join(HERE, "loader.html"), "w", encoding="utf-8").write(LOADER)
    print("pop.js", len(out), "bytes ->", OUT)
    print("loader", len(LOADER), "bytes -> site/vip-pop/loader.html")


if __name__ == "__main__":
    main()
