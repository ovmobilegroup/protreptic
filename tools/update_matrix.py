import json
import openpyxl
from collections import defaultdict

# Load data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

name_to_modes = {}
for code, sc in zh.items():
    if code.startswith('H-'):
        name = sc['name'].split('：')[0] if '：' in sc['name'] else sc['name'].split(':')[0]
        name_to_modes[name] = sc['modes']

# Modern entrepreneurs
modern = {
    '张一鸣(字节)': [11, 16, 20, 31, 33],
    '任正非(华为)': [3, 10, 13, 17, 28, 33, 35],
    '马云(阿里)': [6, 16, 20, 31, 33],
    '雷军(小米)': [8, 11, 14, 16, 19, 28, 33],
    '王兴(美团)': [8, 11, 14, 16, 19, 28, 33],
    '黄峥(拼多多)': [4, 8, 11, 14, 20, 28, 33],
    '李想(理想)': [5, 7, 11, 16, 20, 28, 33],
    '何小鹏(小鹏)': [8, 11, 14, 16, 20, 28, 33],
    '王传福(比亚迪)': [3, 7, 10, 19, 28, 33, 35],
    '杨元庆(联想)': [8, 11, 16, 20, 28, 33],
}

# Mode names
mode_names = [
    "矛盾分析法", "群众路线法", "持久战思维", "农村包围城市", "实事求是法",
    "统一战线法", "战略预判法", "渐进改革法", "独立自主法", "批评与自我批评",
    "灵活策略法", "系统思维法", "全胜思维", "战争重心法", "运动歼灭法",
    "游击战十六字诀", "多元思维模型", "目标管理法", "边际思维", "博弈论思维",
    "无为而治法", "总体性思维", "自然选择法", "间断均衡法", "抽象归纳法",
    "损失厌恶思维", "双系统思维", "冗余备份法", "反馈回路法", "认知偏差识别法",
    "框架效应法", "程序正义法", "格局授权思维", "制度化制衡/杯酒释兵权", "蛰伏积势思维",
    "笨功夫/死磕到底", "知行合一/致良知", "摸石头过河/实验主义",
    "鸟笼经济/边界思维", "三衙分兵/权力制衡架构", "驿站制/信息流速思维", "三民主义/体系化纲领"
]

# Load workbook
wb = openpyxl.load_workbook('three_dimensional_comparison_matrix.xlsx')

# Get all figure names
all_historical = set(name_to_modes.keys())

# Groups
modern = {
    '张一鸣(字节)': [11, 16, 20, 31, 33],
    '任正非(华为)': [3, 10, 13, 17, 28, 33, 35],
    '马云(阿里)': [6, 16, 20, 31, 33],
    '雷军(小米)': [8, 11, 14, 16, 19, 28, 33],
    '王兴(美团)': [8, 11, 14, 16, 19, 28, 33],
    '黄峥(拼多多)': [4, 8, 11, 14, 20, 28, 33],
    '李想(理想)': [5, 7, 11, 16, 20, 28, 33],
    '何小鹏(小鹏)': [8, 11, 14, 16, 20, 28, 33],
    '王传福(比亚迪)': [3, 7, 10, 19, 28, 33, 35],
    '杨元庆(联想)': [8, 11, 16, 20, 28, 33],
}

groups = {
    '毛泽东(238篇)': ['毛泽东'],
    '历史人物': list(sorted(name_to_modes.keys())),
    '现代企业家': list(modern.keys()),
}

# Get weights for a figure
def get_weights(name):
    if name in name_to_modes:
        modes = name_to_modes[name]
    elif name in modern:
        modes = modern[name]
    else:
        return [0]*42
    
    weights = [0]*42
    for i, m in enumerate(modes):
        if m >= 1 and m <= 42:
            if i == 0: w = 0.95
            elif i == 1: w = 0.9
            elif i == 2: w = 0.85
            elif i == 3: w = 0.8
            else: w = 0.75
            weights[m-1] = w
    return weights

# Mode names
mode_names = [
    "矛盾分析法", "群众路线法", "持久战思维", "农村包围城市", "实事求是法",
    "统一战线法", "战略预判法", "渐进改革法", "独立自主法", "批评与自我批评",
    "灵活策略法", "系统思维法", "全胜思维", "战争重心法", "运动歼灭法",
    "游击战十六字诀", "多元思维模型", "目标管理法", "边际思维", "博弈论思维",
    "无为而治法", "总体性思维", "自然选择法", "间断均衡法", "抽象归纳法",
    "损失厌恶思维", "双系统思维", "冗余备份法", "反馈回路法", "认知偏差识别法",
    "框架效应法", "程序正义法", "格局授权思维", "制度化制衡/杯酒释兵权", "蛰伏积势思维",
    "笨功夫/死磕到底", "知行合一/致良知", "摸石头过河/实验主义",
    "鸟笼经济/边界思维", "三衙分兵/权力制衡架构", "驿站制/信息流速思维", "三民主义/体系化纲领"
]

# Load workbook
wb = openpyxl.load_workbook('three_dimensional_comparison_matrix.xlsx')

# Compute group averages
group_data = {}
groups = {
    '毛泽东(238篇)': ['毛泽东'],
    '历史人物': list(sorted(name_to_modes.keys())),
    '现代企业家': list(modern.keys()),
}

for group_name, members in groups.items():
    if not members:
        group_data[group_name] = [0]*42
        continue
    
    avg = [0]*42
    counts = [0]*42
    
    for name in members:
        if name in name_to_modes:
            modes = name_to_modes[name]
        elif name in modern:
            modes = modern[name]
        else:
            continue
        
        for i, m in enumerate(modes):
            if m >= 1 and m <= 42:
                if i == 0: w = 0.95
                elif i == 1: w = 0.9
                elif i == 2: w = 0.85
                elif i == 3: w = 0.8
                else: w = 0.75
                avg[m-1] += w
                counts[m-1] += 1
    
    avg_vals = []
    for i in range(42):
        if counts[i] > 0:
            avg_vals.append(avg[i] / counts[i])
        else:
            avg_vals.append(0)
    group_data[group_name] = avg_vals

# Load workbook
wb = openpyxl.load_workbook('three_dimensional_comparison_matrix.xlsx')

mode_names_list = [
    "矛盾分析法", "群众路线法", "持久战思维", "农村包围城市", "实事求是法",
    "统一战线法", "战略预判法", "渐进改革法", "独立自主法", "批评与自我批评",
    "灵活策略法", "系统思维法", "全胜思维", "战争重心法", "运动歼灭法",
    "游击战十六字诀", "多元思维模型", "目标管理法", "边际思维", "博弈论思维",
    "无为而治法", "总体性思维", "自然选择法", "间断均衡法", "抽象归纳法",
    "损失厌恶思维", "双系统思维", "冗余备份法", "反馈回路法", "认知偏差识别法",
    "框架效应法", "程序正义法", "格局授权思维", "制度化制衡/杯酒释兵权", "蛰伏积势思维",
    "笨功夫/死磕到底", "知行合一/致良知", "摸石头过河/实验主义",
    "鸟笼经济/边界思维", "三衙分兵/权力制衡架构", "驿站制/信息流速思维", "三民主义/体系化纲领"
]

# ===== 2. 群体平均权重 =====
ws = wb['群体平均权重']
ws.delete_rows(2, ws.max_row)
row_num = 2
for group_name, avg in group_data.items():
    row = [group_name] + [round(v, 3) for v in avg]
    for col_idx, val in enumerate(row, 1):
        ws.cell(row=row_num, column=col_idx, value=val)
    row_num += 1

# ===== 3. 各群体Top10模式 =====
ws = wb['各群体Top10模式']
ws.delete_rows(2, ws.max_row)
row_num = 2
for group_name, avg in group_data.items():
    mode_weights = [(mode_names[i], avg[i]) for i in range(42)]
    mode_weights.sort(key=lambda x: x[1], reverse=True)
    for mode_name, weight in mode_weights[:10]:
        ws.cell(row=row_num, column=1, value=group_name)
        ws.cell(row=row_num, column=2, value=mode_name)
        ws.cell(row=row_num, column=3, value=round(weight, 3))
        row_num += 1

# ===== 3. 模式覆盖率分析 =====
ws = wb['模式覆盖率分析']
ws.delete_rows(2, ws.max_row)
row_num = 2

# Build groups mapping
groups_map = {
    '毛泽东(238篇)': ['毛泽东'],
    '历史人物': list(sorted(name_to_modes.keys())),
    '现代企业家': list(modern.keys()),
}

for group_name, avg in group_data.items():
    members = groups.get(group_name, [])
    for i in range(42):
        high_count = 0
        total = 0
        for name in members:
            if name in name_to_modes:
                modes = name_to_modes[name]
            elif name in modern:
                modes = modern[name]
            else:
                continue
            total += 1
            if (i+1) in name_to_modes.get(name, []):
                idx = name_to_modes[name].index(i+1)
                if idx <= 3:
                    high_count += 1
        if total > 0:
            ws.cell(row=row_num, column=1, value=group_name)
            ws.cell(row=row_num, column=2, value=mode_names[i])
            ws.cell(row=row_num, column=3, value=high_count)
            ws.cell(row=row_num, column=4, value=total)
            ws.cell(row=row_num, column=5, value=round(high_count/total, 3))
            row_num += 1

# ===== 4. 群体特有高权重模式 =====
ws = wb['群体特有高权重模式']
ws.delete_rows(2, ws.max_row)
row_num = 2

for i in range(42):
    mode_name = mode_names[i]
    max_avg = 0
    max_group = ''
    second_max = 0
    for group_name, avg in group_data.items():
        if avg[i] > max_avg:
            second_max = max_avg
            max_avg = avg[i]
            max_group = group_name
        elif avg[i] > second_max:
            second_max = avg[i]
    if max_avg > 0:
        ws.cell(row=row_num, column=1, value=mode_names[i])
        ws.cell(row=row_num, column=2, value=max_group)
        ws.cell(row=row_num, column=3, value=round(max_avg, 3))
        ws.cell(row=row_num, column=4, value=round(second_max, 3))
        ws.cell(row=row_num, column=5, value=round(max_avg - second_max, 3))
        row_num += 1

wb.save('three_dimensional_comparison_matrix.xlsx')
print("✅ All sheets updated successfully!")

PYEOF