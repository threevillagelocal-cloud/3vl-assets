"""BD API key: env BD_API_KEY, else read from the local Claude MCP config (never printed or committed)."""
import json, os
def key():
    k = os.environ.get("BD_API_KEY")
    if k: return k
    cfg = json.load(open(os.path.expanduser("~/.claude.json"), encoding="utf-8"))
    def walk(o):
        if isinstance(o, dict):
            for n, v in o.items():
                if n == "brilliant-directories" and isinstance(v, dict) and "args" in v:
                    a = v["args"]; return a[a.index("--api-key") + 1]
                r = walk(v)
                if r: return r
    return walk(cfg)
