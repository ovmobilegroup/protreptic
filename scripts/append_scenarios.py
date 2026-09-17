# Append Li Si scenarios to scenarios_zh.json using Python
import json, os

ws = "<repo>"
path = os.path.join(ws, "data", "scenarios_zh.json")

with open(path) as f:
    data = json.load(f)

qin_entries = [
  {"code": "C-QIN-001", "figure_id": "H-QIN-001", "mode_id": "M391", "title_zh": "C-QIN-001: 上蔡观鼠——跨文化战略选择", "description_zh": "人之贤不肖譬如鼠矣，在所自所处耳——通过跨文化比较识别不同政治体制的运行效率差异，从而做出最优战略选择。", "application_area": []},
  {"code": "C-QIN-002", "figure_id": "H-QIN-001", "mode_id": "M392", "title_zh": "C-QIN-002: 荀门转化——理论转化实践", "description_zh": "弟子不必不如师，师不必贤于弟子——李斯将荀子的道德理想转化为秦朝政治技术。", "application_area": []},
  {"code": "C-QIN-003", "figure_id": "H-QIN-001", "mode_id": "M393", "title_zh": "C-QIN-003: 谏逐客书——归谬法突破", "description_zh": "此数宝者，秦不生一焉——以归谬法揭示逐客令的逻辑矛盾，成为古代政论经典。", "application_area": []},
  {"code": "C-QIN-004", "figure_id": "H-QIN-001", "mode_id": "M394", "title_zh": "C-QIN-004: 置诸侯——郡县制设计", "description_zh": "置诸侯不便——李斯主张废除分封制，全面推行郡县制，设三职互相制衡。", "application_area": []},
  {"code": "C-QIN-005", "figure_id": "H-QIN-001", "mode_id": "M395", "title_zh": "C-QIN-005: 书同文——文化认同工程", "description_zh": "同文字——李斯主持制定小篆作为全国统一书写标准，以秦篆取代各国异体字。", "application_area": []},
  {"code": "C-QIN-006", "figure_id": "H-QIN-001", "mode_id": "M396", "title_zh": "C-QIN-006: 焚书策略——信息控制", "description_zh": "非博士官所职，天下敢有藏书诗书百家语者——通过控制信息流通来统一思想认识。", "application_area": []},
  {"code": "C-QIN-007", "figure_id": "H-QIN-001", "mode_id": "M397", "title_zh": "C-QIN-007: 沙丘之谋——权术现实主义", "description_zh": "李斯得大罪矣，然臣不死，死则无益于秦——为保权而参与沙丘之谋，最终被腰斩。", "application_area": []},
  {"code": "C-QIN-008", "figure_id": "H-QIN-001", "mode_id": "M398", "title_zh": "C-QIN-008: 客卿使用——战略人才", "description_zh": "此数宝者，秦不生一焉——谏逐客书主张以开放态度任用外来人才。", "application_area": []},
  {"code": "C-QIN-009", "figure_id": "H-QIN-001", "mode_id": "M399", "title_zh": "C-QIN-009: 一法度衡石——制度延续", "description_zh": "一法度、衡石、寸尺——李斯设计的制度在秦亡后并未完全消失，被汉及后世王朝所继承。", "application_area": []},
  {"code": "C-QIN-010", "figure_id": "H-QIN-001", "mode_id": "M400", "title_zh": "C-QIN-010: 五蠹批判——社会净化", "description_zh": "儒以文乱法，侠以武犯禁——李斯受韩非影响提出五蠹概念，认为学者等五类是国家的蛀虫。", "application_area": []}
]

data.extend(qin_entries)

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Written {len(qin_entries)} Li Si entries to scenarios_zh.json")
# Verify
with open(path) as f:
    v = json.load(f)
qin_count = sum(1 for e in v if e.get('code', '').startswith('C-QIN'))
print(f"Total C-QIN entries in file: {qin_count}")