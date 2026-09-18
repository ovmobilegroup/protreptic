from pathlib import Path
p = Path('tools/build_sitemap.py')
s = p.read_text(encoding='utf-8')
old = """        kind = "person" if it.get("type") == "figure" else "scenario"
        path = ("minds/%s" if kind == "person" else "figures/%s") % code
        out.append(("%s%s%s/" % (origin, base, path), kind, path))"""
new = """        kind = "person" if it.get("type") == "figure" else "scenario"
        route_path = ("minds/%s" if kind == "person" else "figures/%s") % code
        out.append(("%s%s%s/" % (origin, base, route_path), kind, route_path))"""
assert old in s, "pattern not found"
p.write_text(s.replace(old, new), encoding='utf-8')
print("patched")
