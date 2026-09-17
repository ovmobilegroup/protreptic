# Append Li Si scenarios to scenarios_en.json using Python
import json, os

ws = "<repo>"
path = os.path.join(ws, "data", "scenarios_en.json")

with open(path) as f:
    data = json.load(f)

qin_en_entries = [
  {"code": "C-QIN-001E", "figure_id": "H-QIN-001", "mode_id": "M391", "title_en": "C-QIN-E001: The Rat at Shangcai — Cross-Cultural Strategic Selection", "description_en": "One's worth is like a rat — it depends on where one places oneself. Identifying efficiency differences across political systems through cross-cultural comparison to make optimal strategic choices.", "application_area": []},
  {"code": "C-QIN-002E", "figure_id": "H-QIN-001", "mode_id": "M392", "title_en": "C-QIN-E002: Xunzi Transformation — Theory to Practice", "description_en": "Disciples need not be inferior to teachers. Li Si transformed Xunzi's moral idealism into Qin dynasty political technology.", "application_area": []},
  {"code": "C-QIN-003E", "figure_id": "H-QIN-001", "mode_id": "M393", "title_en": "C-QIN-E003: Expelling Foreign Guests — Reductio ad Absurdum", "description_en": "'Not one of these treasures is produced in Qin — why does Your Majesty delight in them?' Using reductio ad absurdum to reveal the contradiction of expelling foreign guests, becoming a classical model of ancient political argumentation.", "application_area": []},
  {"code": "C-QIN-004E", "figure_id": "H-QIN-001", "mode_id": "M394", "title_en": "C-QIN-E004: Placing Feudal Lords — County System Design", "description_en": "'Placing feudal lords is inconvenient.' Li Si advocated abolishing enfeoffment and fully implementing the county system with three mutually checking positions.", "application_area": []},
  {"code": "C-QIN-005E", "figure_id": "H-QIN-001", "mode_id": "M395", "title_en": "C-QIN-E005: Unified Scripts — Cultural Identity Engineering", "description_en": "'Unify scripts.' Li Si developed small seal script as the national writing standard, replacing various regional characters with unified 'Qin script'.", "application_area": []},
  {"code": "C-QIN-006E", "figure_id": "H-QIN-001", "mode_id": "M396", "title_en": "C-QIN-E006: Book Burning Strategy — Information Control", "description_en": "'Non-scholars who dare to possess Poetry, Documents, or works of the hundred schools must be burned.' Controlling information flow to unify thought.", "application_area": []},
  {"code": "C-QIN-007E", "figure_id": "H-QIN-001", "mode_id": "M397", "title_en": "C-QIN-E007: Shaqiu Conspiracy — Political Realism", "description_en": "'Li Si committed great crimes, but if I die it benefits no one in Qin.' To maintain power he participated in the Shaqiu plot, ultimately being waist-executed.", "application_area": []},
  {"code": "C-QIN-008E", "figure_id": "H-QIN-001", "mode_id": "M398", "title_en": "C-QIN-E008: Guest Ministers — Strategic Talent Strategy", "description_en": "'Not one of these treasures is produced in Qin — why does Your Majesty delight in them?' The Memorial advocated open employment of external talents.", "application_area": []},
  {"code": "C-QIN-009E", "figure_id": "H-QIN-001", "mode_id": "M399", "title_en": "C-QIN-E009: Standardize Laws and Measures — Institutional Continuity", "description_en": "'Standardize laws, weights, measures.' The systems Li Si designed were not completely eliminated after Qin's fall but inherited by Han and subsequent dynasties.", "application_area": []},
  {"code": "C-QIN-010E", "figure_id": "H-QIN-001", "mode_id": "M400", "title_en": "C-QIN-E010: Five Vermin Critique — Social Purification", "description_en": "'Scholars confuse law with their writings, knights transgress prohibitions... these five are the state's vermin.' Li Si (influenced by Han Fei) proposed the 'Five Vermin' concept.", "application_area": []}
]

data.extend(qin_en_entries)

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Written {len(qin_en_entries)} Li Si entries to scenarios_en.json")
# Verify
with open(path) as f:
    v = json.load(f)
qin_count = sum(1 for e in v if 'QIN' in e.get('code', ''))
print(f"Total C-QIN entries in file: {qin_count}")