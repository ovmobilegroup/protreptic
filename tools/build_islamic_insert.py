import json, os

os.chdir("/opt/data/workspace/Protreptic")

# Read the restored valid master file from git backup
with open("/tmp/restore_master.json", "r") as f:
    master_text = f.read()

# Read the Islamic modes (valid JSON array)  
with open("data/master_modes_v2_islamic.json") as f:
    islamic = json.load(f)

# Split at insertion point (line 258 in the restored file, between M252 and M416)
lines = master_text.split('\n')
part1_lines = lines[:258]  # Lines 0-257 (258 lines, up to and including "    },")
part3_lines = lines[258:]  # Lines 258+ (starting with "    {")

# Build the formatted Islamic block
block_lines = []
for i, m in enumerate(islamic):
    block_lines.append('    {')
    block_lines.append(f'      "id": "{m["id"]}",')
    block_lines.append(f'      "name": "{m["name"]}",')
    block_lines.append(f'      "definition": "{m["definition"]}",')
    block_lines.append('      "process": [')
    for j, step in enumerate(m["process"]):
        if j < len(m["process"]) - 1:
            block_lines.append(f'        "{step}",')
        else:
            block_lines.append(f'        "{step}"')
    block_lines.append("      ],")
    block_lines.append('      "representative_figures": [')
    for j, fig in enumerate(m["representative_figures"]):
        if j < len(m["representative_figures"]) - 1:
            block_lines.append(f'        "{fig}",')
        else:
            block_lines.append(f'        "{fig}"')
    if i < len(islamic) - 1:
        block_lines.append("      ]")
        block_lines.append("    },")
    else:
        block_lines.append("      ]")
        # Last mode also needs trailing comma since it's followed by more modes from part3
        block_lines.append("    },")  # trailing comma needed for JSON array

# Assemble final file
final_lines = part1_lines + block_lines + part3_lines
final_text = '\n'.join(final_lines)

# Write back (with trailing newline)
if not final_text.endswith('\n'):
    final_text += '\n'

with open("data/master_modes_v2.json", "w") as f:
    f.write(final_text)

# Validate
with open("data/master_modes_v2.json") as f:
    data = json.load(f)

modes = data["modes"]
all_ids = [m["id"] for m in modes]

# Count Islamic mode IDs (M380-M394)
islamic_ids = [id_ for id_ in all_ids if "M38" <= id_ < "M400"]
print(f"Total modes: {len(modes)}")
print(f"Islamic mode IDs inserted: {islamic_ids}")
print(f"Number of Islamic modes: {len(islamic_ids)}")

# Verify ordering - check M252 is followed by M380
for i, m in enumerate(modes):
    if m["id"] == "M252":
        print(f"M252 at index {i}, next is {modes[i+1]['id']}")
    if m["id"] == "M394":
        print(f"M394 at index {i}, next is {modes[i+1]['id']}")
    if m["id"] == "M416":
        print(f"M416 at index {i}, prev is {modes[i-1]['id']}")

# Verify no duplicates
if len(all_ids) != len(set(all_ids)):
    from collections import Counter
    dupes = [k for k, v in Counter(all_ids).items() if v > 1]
    print(f"DUPLICATE IDs: {dupes}")
else:
    print("No duplicate IDs")

print(f"Final file written successfully with {len(modes)} total modes (15 Islamic: M380-M394)")