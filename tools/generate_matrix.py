#!/usr/bin/env python3
"""
Generate three-dimensional comparison matrix for all historical figures.
Outputs Excel with 5 sheets:
1. Figure x Mode matrix (binary)
2. Figure x Domain matrix 
3. Figure x Era matrix
4. Mode statistics
5. Domain/Era cross-tabulation
"""
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from collections import defaultdict

# Load data
with open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'r', encoding='utf-8') as f:
    modes = json.load(f)

# Mode names
zh_modes = modes['zh']
en_modes = modes['en']

# Domain mapping (based on mode categories)
MODE_DOMAINS = {
    '1': 'Strategic', '2': 'Strategic', '3': 'Strategic', '4': 'Strategic',
    '5': 'Analytical', '6': 'Collaborative', '7': 'Strategic', '8': 'Operational',
    '9': 'Operational', '10': 'Collaborative', '11': 'Operational', '12': 'Systems',
    '13': 'Strategic', '14': 'Strategic', '15': 'Strategic', '16': 'Strategic',
    '17': 'Analytical', '18': 'Collaborative', '19': 'Analytical', '20': 'Analytical',
    '21': 'Personal', '22': 'Systems', '23': 'Creative', '24': 'Analytical',
    '25': 'Analytical', '26': 'Personal', '27': 'Systems', '28': 'Operational',
    '29': 'Analytical', '30': 'Analytical', '31': 'Systems', '32': 'Systems',
    '33': 'Strategic', '34': 'Systems', '35': 'Operational', '36': 'Personal',
    '37': 'Personal', '38': 'Operational', '39': 'Strategic', '40': 'Operational',
    '41': 'Operational', '42': 'Personal'
}

DOMAIN_COLORS = {
    'Strategic': 'FFE6E6',
    'Analytical': 'E6F2FF',
    'Collaborative': 'E6FFE6',
    'Operational': 'FFF2E6',
    'Systems': 'F2E6FF',
    'Creative': 'FFE6F2',
    'Personal': 'FFFFE6'
}

# Era tags for historical figures (simplified mapping)
ERA_TAGS = {
    '先秦': ['H-GGZ', 'H-LZ', 'H-ZZ', 'H-KZ', 'H-MZ', 'H-XZ', 'H-ZS', 'H-SQ', 'H-FL', 'H-LL', 'H-SH', 'H-MZ-167', 'H-MZ-169', 'H-MZB', 'H-SBH', 'H-SD', 'H-LS', 'H-WQ', 'H-BG', 'H-YW', 'H-MZB-165'],
    '秦汉': ['H-LB', 'H-XH', 'H-LS-03', 'H-ZG', 'H-SB', 'H-HF', 'H-LS-158', 'H-GZ', 'H-ZK', 'H-ZY'],
    '三国两晋': ['H-ZL', 'H-CC', 'H-SQ-22', 'H-LB-15', 'H-JSX', 'H-TYM', 'H-RJ', 'H-TYM-220'],
    '南北朝': ['H-ZCZ', 'H-YX', 'H-THJ', 'H-WZY', 'H-QCJ', 'H-XLY', 'H-XZ'],
    '隋唐': ['H-LJ', 'H-WXZ', 'H-CL', 'H-LZY', 'H-FZY', 'H-SY', 'H-QXK', 'H-LD', 'H-LDB', 'H-ZLQ', 'H-QCJ-245'],
    '宋元': ['H-SMG', 'H-WB', 'H-OYX', 'H-WAS', 'H-ZJ', 'H-ZDY', 'H-SD-46', 'H-ZDY-212', 'H-EC', 'H-ZX', 'H-LJY', 'H-WY', 'H-QCJ-155', 'H-YS-261', 'H-QQ'],
    '明清': ['H-WAS-34', 'H-ZZ-141', 'H-XGQ', 'H-SYS', 'H-LSZ', 'H-LY', 'H-YZ', 'H-WZT', 'H-WFZ', 'H-LZ', 'H-GYW', 'H-HZX', 'H-WYM', 'H-ZEL', 'H-ZDL', 'H-THJ-153', 'H-WZY-154', 'H-QCJ-155', 'H-SBH-156', 'H-SD-157', 'H-LS-158', 'H-WQ-159', 'H-BG-160', 'H-MZB-165', 'H-YW-162', 'H-CWJ-163', 'H-SGB-164', 'H-CXT-165', 'H-WZT-166', 'H-QR-167', 'H-ZX-214', 'H-LJY-215', 'H-WYM-216', 'H-GYW-217', 'H-HZX-218', 'H-WFZ-219', 'H-DZ-220', 'H-MZ-221', 'H-ZZ-222', 'H-MZHT-223', 'H-BG-224', 'H-LZJ-225', 'H-ZQ-226', 'H-MDL-227', 'H-ZY-228', 'H-WMS-229', 'H-BQ-230', 'H-LJ-231', 'H-KSH-232', 'H-ZCZ-233', 'H-YX-234', 'H-LSL-235', 'H-DWJ-236', 'H-WWG-237', 'H-LSG-238', 'H-WYX-239', 'H-YQS-240', 'H-ZLQ-241', 'H-WYAGD-240', 'H-HBL-241', 'H-CJH-242', 'H-LDB-243', 'H-ZLQ-244', 'H-QCJ-245', 'H-ZDL-246', 'H-LJ-264', 'H-KSZ-265', 'H-CG-266', 'H-YJY-267', 'H-XSY-268', 'H-YX-269'],
    '近代': ['H-TS', 'H-ZJ', 'H-ZD-26', 'H-ZG-19', 'H-ZZD-35', 'H-HLG', 'H-HYP', 'H-ZKZ', 'H-ZTY', 'H-LBN', 'H-FML', 'H-WJZ', 'H-CXQ', 'H-YF', 'H-KYW', 'H-LH', 'H-XMQ', 'H-SMX', 'H-LGJ', 'H-PDH', 'H-ZEL', 'H-LXN', 'H-LSQ', 'H-CY', 'H-YM', 'H-YLP', 'H-TYY', 'H-DJX', 'H-QSQ', 'H-QM', 'H-WMS', 'H-GZP', 'H-LZX', 'H-ZXC', 'H-WYS', 'H-YG', 'H-LH', 'H-SMX', 'H-LGJ', 'H-WJL', 'H-ZRB'],
    '现代': ['H-MZD', 'H-RZF', 'H-CY', 'H-XMQ', 'H-WJL', 'H-YG', 'H-LH', 'H-SMX', 'H-LGJ', 'H-WJL', 'H-ZRB', 'H-LBC', 'H-HL', 'H-CG', 'H-XQ', 'H-NRZ', 'H-YJY', 'H-XSY', 'H-SY', 'H-CY', 'H-YM', 'H-YLP', 'H-TYY', 'H-DJX', 'H-QSQ', 'H-QM', 'H-WMS', 'H-GZP', 'H-LZX', 'H-ZXC', 'H-WYS', 'H-YG', 'H-LH', 'H-SMX', 'H-LGJ', 'H-WJL', 'H-ZRB']
}

# For simplicity, assign era based on code prefix patterns
def get_era(code):
    # This is a simplified mapping - in reality would need proper mapping
    if code in ['H-GGZ', 'H-LZ', 'H-ZZ', 'H-KZ', 'H-MZ', 'H-XZ', 'H-ZS', 'H-SQ', 'H-FL', 'H-LL', 'H-SH', 'H-MZ-167', 'H-MZ-169', 'H-MZB', 'H-SBH', 'H-SD', 'H-LS', 'H-WQ', 'H-BG', 'H-YW', 'H-MZB-165']:
        return '先秦'
    elif code in ['H-LB', 'H-XH', 'H-LS-03', 'H-ZG', 'H-SB', 'H-HF', 'H-LS-158', 'H-GZ', 'H-ZK', 'H-ZY']:
        return '秦汉'
    elif code in ['H-ZL', 'H-CC', 'H-SQ-22', 'H-LB-15', 'H-JSX', 'H-TYM', 'H-RJ', 'H-TYM-220']:
        return '三国两晋'
    elif code in ['H-ZCZ', 'H-YX', 'H-THJ', 'H-WZY', 'H-QCJ', 'H-XLY', 'H-XZ']:
        return '南北朝'
    elif code in ['H-LJ', 'H-WXZ', 'H-CL', 'H-LZY', 'H-FZY', 'H-SY', 'H-QXK', 'H-LD', 'H-LDB', 'H-ZLQ', 'H-QCJ-245']:
        return '隋唐'
    elif code in ['H-SMG', 'H-WB', 'H-OYX', 'H-WAS', 'H-ZJ', 'H-ZDY', 'H-SD-46', 'H-ZDY-212', 'H-EC', 'H-ZX', 'H-LJY', 'H-WY', 'H-QCJ-155', 'H-YS-261', 'H-QQ']:
        return '宋元'
    elif '21' in code or '22' in code or '23' in code or '24' in code or '25' in code or '26' in code or '16' in code or '17' in code or '18' in code or '19' in code or '20' in code:
        return '明清'
    elif code in ['H-TS', 'H-ZJ', 'H-ZD-26', 'H-ZG-19', 'H-ZZD-35', 'H-HLG', 'H-HYP', 'H-ZKZ', 'H-ZTY', 'H-LBN', 'H-FML', 'H-WJZ', 'H-CXQ', 'H-YF', 'H-KYW', 'H-LH', 'H-XMQ', 'H-SMX', 'H-LGJ', 'H-PDH', 'H-ZEL', 'H-LXN', 'H-LSQ', 'H-CY', 'H-YM', 'H-YLP', 'H-TYY', 'H-DJX', 'H-QSQ', 'H-QM', 'H-WMS', 'H-GZP', 'H-LZX', 'H-ZXC', 'H-WYS', 'H-YG', 'H-LH', 'H-SMX', 'H-LGJ', 'H-WJL', 'H-ZRB']:
        return '近代'
    else:
        return '现代'

# Extract historical figures
h_codes = sorted([k for k in zh if k.startswith('H-')])

wb = openpyxl.Workbook()

# Styles
header_font = Font(bold=True, size=11)
header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
header_font_white = Font(bold=True, size=11, color='FFFFFF')
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# ============================================================
# Sheet 1: Figure x Mode Matrix (binary)
# ============================================================
ws1 = wb.active
ws1.title = "Figure x Mode"

# Headers
ws1.cell(row=1, column=1, value="Code").font = header_font_white
ws1.cell(row=1, column=1).fill = header_fill
ws1.cell(row=1, column=2, value="Name (ZH)").font = header_font_white
ws1.cell(row=1, column=2).fill = header_fill
ws1.cell(row=1, column=3, value="Name (EN)").font = header_font_white
ws1.cell(row=1, column=3).fill = header_fill
ws1.cell(row=1, column=4, value="Era").font = header_font_white
ws1.cell(row=1, column=4).fill = header_fill
ws1.cell(row=1, column=5, value="Domain").font = header_font_white
ws1.cell(row=1, column=5).fill = header_fill

mode_ids = sorted([str(i) for i in range(1, 43)], key=int)
for i, mid in enumerate(mode_ids):
    col = 6 + i
    mode_name = zh_modes[mid][0] if mid in zh_modes else f"Mode {mid}"
    domain = MODE_DOMAINS.get(mid, 'Unknown')
    cell = ws1.cell(row=1, column=col, value=f"{mid}: {mode_name}")
    cell.font = header_font_white
    cell.fill = PatternFill(start_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), end_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), fill_type='solid')
    cell.alignment = Alignment(text_rotation=90, horizontal='center', vertical='bottom')
    cell.border = thin_border

# Data rows
for row_idx, code in enumerate(h_codes, 2):
    entry_zh = zh[code]
    entry_en = en[code]
    modes_used = entry_zh['modes']
    
    ws1.cell(row=row_idx, column=1, value=code).border = thin_border
    ws1.cell(row=row_idx, column=2, value=entry_zh['name']).border = thin_border
    ws1.cell(row=row_idx, column=3, value=entry_en['name']).border = thin_border
    ws1.cell(row=row_idx, column=4, value=get_era(code)).border = thin_border
    ws1.cell(row=row_idx, column=5, value=', '.join(set(MODE_DOMAINS.get(str(m), '') for m in modes_used))).border = thin_border
    
    for i, mid in enumerate(mode_ids):
        col = 6 + i
        val = 1 if int(mid) in modes_used else 0
        cell = ws1.cell(row=row_idx, column=col, value=val)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')
        if val == 1:
            domain = MODE_DOMAINS.get(mid, 'Unknown')
            cell.fill = PatternFill(start_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), end_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), fill_type='solid')

# Adjust column widths
ws1.column_dimensions['A'].width = 12
ws1.column_dimensions['B'].width = 35
ws1.column_dimensions['C'].width = 35
ws1.column_dimensions['D'].width = 10
ws1.column_dimensions['E'].width = 30
for i in range(len(mode_ids)):
    ws1.column_dimensions[get_column_letter(6 + i)].width = 3

# Freeze panes
ws1.freeze_panes = 'F2'

# ============================================================
# Sheet 2: Figure x Domain Matrix
# ============================================================
ws2 = wb.create_sheet("Figure x Domain")

domains = ['Strategic', 'Analytical', 'Collaborative', 'Operational', 'Systems', 'Creative', 'Personal']

ws2.cell(row=1, column=1, value="Code").font = header_font_white
ws2.cell(row=1, column=1).fill = header_fill
ws2.cell(row=1, column=2, value="Name (ZH)").font = header_font_white
ws2.cell(row=1, column=2).fill = header_fill
ws2.cell(row=1, column=3, value="Name (EN)").font = header_font_white
ws2.cell(row=1, column=3).fill = header_fill
ws2.cell(row=1, column=4, value="Era").font = header_font_white
ws2.cell(row=1, column=4).fill = header_fill

for i, domain in enumerate(domains):
    col = 5 + i
    cell = ws2.cell(row=1, column=col, value=domain)
    cell.font = header_font_white
    cell.fill = PatternFill(start_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), end_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), fill_type='solid')
    cell.border = thin_border

for row_idx, code in enumerate(h_codes, 2):
    entry_zh = zh[code]
    entry_en = en[code]
    modes_used = entry_zh['modes']
    domains_used = set(MODE_DOMAINS.get(str(m), '') for m in modes_used)
    
    ws2.cell(row=row_idx, column=1, value=code).border = thin_border
    ws2.cell(row=row_idx, column=2, value=entry_zh['name']).border = thin_border
    ws2.cell(row=row_idx, column=3, value=entry_en['name']).border = thin_border
    ws2.cell(row=row_idx, column=4, value=get_era(code)).border = thin_border
    
    for i, domain in enumerate(domains):
        col = 5 + i
        val = 1 if domain in domains_used else 0
        cell = ws2.cell(row=row_idx, column=col, value=val)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')
        if val == 1:
            cell.fill = PatternFill(start_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), end_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), fill_type='solid')

ws2.column_dimensions['A'].width = 12
ws2.column_dimensions['B'].width = 35
ws2.column_dimensions['C'].width = 35
ws2.column_dimensions['D'].width = 10
for i in range(len(domains)):
    ws2.column_dimensions[get_column_letter(5 + i)].width = 18

ws2.freeze_panes = 'E2'

# ============================================================
# Sheet 3: Figure x Era Matrix
# ============================================================
ws3 = wb.create_sheet("Figure x Era")

eras = ['先秦', '秦汉', '三国两晋', '南北朝', '隋唐', '宋元', '明清', '近代', '现代']

ws3.cell(row=1, column=1, value="Code").font = header_font_white
ws3.cell(row=1, column=1).fill = header_fill
ws3.cell(row=1, column=2, value="Name (ZH)").font = header_font_white
ws3.cell(row=1, column=2).fill = header_fill
ws3.cell(row=1, column=3, value="Name (EN)").font = header_font_white
ws3.cell(row=1, column=3).fill = header_fill

for i, era in enumerate(eras):
    col = 4 + i
    cell = ws3.cell(row=1, column=col, value=era)
    cell.font = header_font_white
    cell.fill = header_fill
    cell.border = thin_border

era_colors = {
    '先秦': 'FFE6E6', '秦汉': 'FFEBE6', '三国两晋': 'FFF2E6',
    '南北朝': 'FFF9E6', '隋唐': 'FFFFE6', '宋元': 'F2FFE6',
    '明清': 'E6FFE6', '近代': 'E6FFF2', '现代': 'E6F2FF'
}

for row_idx, code in enumerate(h_codes, 2):
    entry_zh = zh[code]
    entry_en = en[code]
    era = get_era(code)
    
    ws3.cell(row=row_idx, column=1, value=code).border = thin_border
    ws3.cell(row=row_idx, column=2, value=entry_zh['name']).border = thin_border
    ws3.cell(row=row_idx, column=3, value=entry_en['name']).border = thin_border
    
    for i, e in enumerate(eras):
        col = 4 + i
        val = 1 if e == era else 0
        cell = ws3.cell(row=row_idx, column=col, value=val)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')
        if val == 1:
            cell.fill = PatternFill(start_color=era_colors.get(e, 'FFFFFF'), end_color=era_colors.get(e, 'FFFFFF'), fill_type='solid')

ws3.column_dimensions['A'].width = 12
ws3.column_dimensions['B'].width = 35
ws3.column_dimensions['C'].width = 35
for i in range(len(eras)):
    ws3.column_dimensions[get_column_letter(4 + i)].width = 10

ws3.freeze_panes = 'D2'

# ============================================================
# Sheet 4: Mode Statistics
# ============================================================
ws4 = wb.create_sheet("Mode Statistics")

ws4.cell(row=1, column=1, value="Mode ID").font = header_font_white
ws4.cell(row=1, column=1).fill = header_fill
ws4.cell(row=1, column=2, value="Mode Name (ZH)").font = header_font_white
ws4.cell(row=1, column=2).fill = header_fill
ws4.cell(row=1, column=3, value="Mode Name (EN)").font = header_font_white
ws4.cell(row=1, column=3).fill = header_fill
ws4.cell(row=1, column=4, value="Domain").font = header_font_white
ws4.cell(row=1, column=4).fill = header_fill
ws4.cell(row=1, column=5, value="Figure Count").font = header_font_white
ws4.cell(row=1, column=5).fill = header_fill
ws4.cell(row=1, column=6, value="Percentage").font = header_font_white
ws4.cell(row=1, column=6).fill = header_fill
ws4.cell(row=1, column=7, value="Figures").font = header_font_white
ws4.cell(row=1, column=7).fill = header_fill

total_figures = len(h_codes)

for row_idx, mid in enumerate(mode_ids, 2):
    mode_name_zh = zh_modes[mid][0] if mid in zh_modes else f"Mode {mid}"
    mode_name_en = en_modes[mid][0] if mid in en_modes else f"Mode {mid}"
    domain = MODE_DOMAINS.get(mid, 'Unknown')
    
    count = sum(1 for code in h_codes if int(mid) in zh[code]['modes'])
    pct = count / total_figures * 100
    
    figures_list = ', '.join([zh[code]['name'][:15] for code in h_codes if int(mid) in zh[code]['modes']])
    
    ws4.cell(row=row_idx, column=1, value=mid).border = thin_border
    ws4.cell(row=row_idx, column=2, value=mode_name_zh).border = thin_border
    ws4.cell(row=row_idx, column=3, value=mode_name_en).border = thin_border
    ws4.cell(row=row_idx, column=4, value=domain).border = thin_border
    ws4.cell(row=row_idx, column=5, value=count).border = thin_border
    ws4.cell(row=row_idx, column=6, value=f"{pct:.1f}%").border = thin_border
    ws4.cell(row=row_idx, column=7, value=figures_list).border = thin_border
    
    # Color by domain
    for col in range(1, 8):
        ws4.cell(row=row_idx, column=col).fill = PatternFill(start_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), end_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), fill_type='solid')

ws4.column_dimensions['A'].width = 10
ws4.column_dimensions['B'].width = 30
ws4.column_dimensions['C'].width = 30
ws4.column_dimensions['D'].width = 15
ws4.column_dimensions['E'].width = 12
ws4.column_dimensions['F'].width = 12
ws4.column_dimensions['G'].width = 80

# ============================================================
# Sheet 5: Domain x Era Cross-tabulation
# ============================================================
ws5 = wb.create_sheet("Domain x Era")

ws5.cell(row=1, column=1, value="Domain \\ Era").font = header_font_white
ws5.cell(row=1, column=1).fill = header_fill

for i, era in enumerate(eras):
    col = 2 + i
    cell = ws5.cell(row=1, column=col, value=era)
    cell.font = header_font_white
    cell.fill = PatternFill(start_color=era_colors.get(era, 'FFFFFF'), end_color=era_colors.get(era, 'FFFFFF'), fill_type='solid')
    cell.border = thin_border

# Total column
cell = ws5.cell(row=1, column=len(eras)+2, value="Total")
cell.font = header_font_white
cell.fill = header_fill
cell.border = thin_border

for row_idx, domain in enumerate(domains, 2):
    ws5.cell(row=row_idx, column=1, value=domain).font = header_font
    ws5.cell(row=row_idx, column=1).fill = PatternFill(start_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), end_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), fill_type='solid')
    ws5.cell(row=row_idx, column=1).border = thin_border
    
    row_total = 0
    for i, era in enumerate(eras):
        col = 2 + i
        count = sum(1 for code in h_codes 
                   if get_era(code) == era 
                   and domain in set(MODE_DOMAINS.get(str(m), '') for m in zh[code]['modes']))
        cell = ws5.cell(row=row_idx, column=col, value=count)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')
        cell.fill = PatternFill(start_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), end_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), fill_type='solid')
        row_total += count
    
    # Total
    cell = ws5.cell(row=row_idx, column=len(eras)+2, value=row_total)
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')
    cell.font = Font(bold=True)
    cell.fill = PatternFill(start_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), end_color=DOMAIN_COLORS.get(domain, 'FFFFFF'), fill_type='solid')

# Grand total row
grand_row = len(domains) + 2
ws5.cell(row=grand_row, column=1, value="Grand Total").font = Font(bold=True)
ws5.cell(row=grand_row, column=1).fill = header_fill
ws5.cell(row=grand_row, column=1).border = thin_border

grand_total = 0
for i, era in enumerate(eras):
    col = 2 + i
    count = sum(1 for code in h_codes if get_era(code) == era)
    cell = ws5.cell(row=grand_row, column=col, value=count)
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')
    cell.font = Font(bold=True)
    cell.fill = PatternFill(start_color=era_colors.get(era, 'FFFFFF'), end_color=era_colors.get(era, 'FFFFFF'), fill_type='solid')
    grand_total += count

cell = ws5.cell(row=grand_row, column=len(eras)+2, value=grand_total)
cell.border = thin_border
cell.alignment = Alignment(horizontal='center')
cell.font = Font(bold=True)
cell.fill = header_fill

ws5.column_dimensions['A'].width = 18
for i in range(len(eras)):
    ws5.column_dimensions[get_column_letter(2 + i)].width = 10
ws5.column_dimensions[get_column_letter(len(eras)+2)].width = 10

# Save
output_path = '/opt/data/workspace/Protreptic/tools/three_dimensional_comparison_matrix.xlsx'
wb.save(output_path)
print(f"Matrix saved to {output_path}")
print(f"Sheets: {wb.sheetnames}")
print(f"Historical figures: {len(h_codes)}")
print(f"Modes: {len(mode_ids)}")
print(f"Domains: {len(domains)}")
print(f"Eras: {len(eras)}")