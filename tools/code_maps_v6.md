# Code Maps v6 更新

## 概述
Phase 13-16 新增 95 个新模式 (M262-M356) 和 14 个新国家/地区前缀 (AM/AZ/CY/GE/GT/MD/ME/MN/MY/NI/OM/SV/XK/YE)。

### CODE_MAP 扩展
以下新条目加入 `code_maps.json` 中的 CODE_MAP 和 CODE_MAP_EN：

**Mode ID 扩展**: M262-M356 (对应 modes_expansion_v4.md 中定义的 95 个新模式)

**国家/地区前缀扩展** (14 个全新前缀，未覆盖于 v5):
| Prefix | Country/Region |
|--------|----------------|
| AM | Armenia |
| AZ | Azerbaijan |
| CY | Cyprus |
| GE | Georgia |
| GT | Guatemala |
| MD | Moldova |
| ME | Montenegro |
| MN | Mongolia |
| MY | Malaysia |
| NI | Nicaragua |
| OM | Oman |
| SV | El Salvador |
| XK | Kosovo |
| YE | Yemen |

### Code Maps 格式
`code_maps.json` 的 `CODE_MAP` 和 `CODE_MAP_EN` 结构为 `{code: name}` 映射。

**CODE_MAP (中文)** 新增条目:
- M262-M356: 对应新思维模式的中文名称
- AM-*, AZ-*, CY-*, GE-*, GT-*, MD-*, ME-*, MN-*, MY-*, NI-*, OM-*, SV-*, XK-*, YE-* 人物 scenario code -> 中文名称

**CODE_MAP_EN (英文)** 新增条目:
- M262-M356: 对应新思维模式的英文名称
- AM-*, AZ-*, CY-*, GE-*, GT-*, MD-*, ME-*, MN-*, MY-*, NI-*, OM-*, SV-*, XK-*, YE-* 人物 scenario code -> 英文名称

### 扩展统计
- **CODE_MAP 数量**: 753 → 753 + 95 (modes) + 96 (scenarios) = 944
- **CODE_MAP_EN 数量**: 753 → 753 + 95 (modes) + 96 (scenarios) = 944
- **CODE_MAP_EN 数量**: 753 → 944

---

## 更新指令

```bash
# 1. 扩展 CODE_MAP 和 CODE_MAP_EN
python3 update_code_maps.py

# 2. 扩展 scenarios_zh.json 和 scenarios_en.json
python3 update_scenarios.py

# 3. 更新 scenario_tags.json
python3 update_tags.py
```

---

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v5.0 | Phase 9-12 | 753 个 code 映射 |
| v6.0 | Phase 13-16 | **+191 个 code 映射** (95 个新模式 + 96 个新 scenario) |