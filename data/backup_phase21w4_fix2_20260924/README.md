# backup_phase21w4_fix2_20260924 (卡 t_33240de8)

对象: tools/json/scenarios_zh.json 全文件 byte-exact (before = 落盘前态) + 4 字段 before 摘要。
编辑: $.H-LXN-001.name_zh/description_zh/reason_zh/case_zh 毛先念->李先念 (4 处, 等长最小 diff)。
校验: cd 本目录 && sha256sum -c MANIFEST.sha256; fields_before.json 载有逐字段 before/after_expected 与字节偏移。
