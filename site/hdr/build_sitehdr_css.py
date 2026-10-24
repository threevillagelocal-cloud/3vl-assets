"""Make site/hdr/sitehdr.css from the homepage front layout CSS (weekender/front/front.css): every header (.yh*) and footer (.yf*) rule,
re-scoped from #wk-top.wk-y to #tvl-sh / #tvl-sf, so the sitewide header looks exactly like the homepage. Rerun after front.css header changes."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(HERE, "..", "..", "weekender", "front", "front.css"), encoding="utf-8").read()
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def blocks(s):
    out, i, n = [], 0, len(s)
    while i < n:
        j = s.find("{", i)
        if j < 0: break
        sel = s[i:j].strip(); depth, k = 1, j + 1
        while depth and k < n:
            depth += {"{": 1, "}": -1}.get(s[k], 0); k += 1
        out.append((sel, s[j + 1:k - 1])); i = k
    return out


def keep(sel, body):
    sels = [x.strip() for x in sel.split(",")]
    good = [x for x in sels if re.search(r"\.y[hf](\b|-)", x)]
    if not good: return ""
    good = [x.replace("#wk-top.wk-y .yf", "#tvl-sf .yf").replace("#wk-top.wk-y .yh", "#tvl-sh .yh").replace("#wk-top.wk-y ", "#tvl-sh ") for x in good]
    return ",".join(good) + "{" + body.strip() + "}"


out = []
for sel, body in blocks(css):
    if sel.startswith("@media"):
        inner = [r for r in (keep(s, b) for s, b in blocks(body)) if r]
        if inner: out.append(sel + "{" + "".join(inner) + "}")
    else:
        r = keep(sel, body)
        if r: out.append(r)
base = open(os.path.join(HERE, "sitehdr-base.css"), encoding="utf-8").read()
open(os.path.join(HERE, "sitehdr.css"), "w", encoding="utf-8").write(base + "\n" + "\n".join(out) + "\n")
print(len(out), "rules")
