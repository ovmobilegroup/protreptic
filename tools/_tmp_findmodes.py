import re, glob, os
base = "/opt/data/workspace/Protreptic"
# Search for mode rows "# 34 |", "# 37 |", "# 39 |", "# 19 |" across all docs/md files
targets = {19, 34, 37, 39}
found = {}
for f in glob.glob(base + "/docs/**/*.md", recursive=True):
    try:
        txt = open(f, encoding="utf-8", errors="ignore").read()
    except Exception:
        continue
    for line in txt.splitlines():
        m = re.match(r"\|\s*#?\s*(\d{1,3})\s*\|", line)
        if m:
            mid = int(m.group(1))
            if mid in targets:
                # extract name (second cell)
                cells = [c.strip() for c in line.split("|")]
                # cells[0] empty, cells[1]=num, cells[2]=name
                name = cells[2] if len(cells) > 2 else ""
                if name and mid not in found:
                    found[mid] = (f, name, line.strip()[:160])
for mid in sorted(targets):
    if mid in found:
        f, name, ln = found[mid]
        print(mid, "::", name, "  [", os.path.basename(f), "]")
    else:
        print(mid, ":: NOT FOUND")
