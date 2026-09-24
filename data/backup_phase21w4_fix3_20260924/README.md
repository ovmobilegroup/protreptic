# backup_phase21w4_fix3_20260924 (卡 t_def07a84)

对象: tools/json/scenarios_zh.json 全文件 byte-exact (before = 落盘前态) + en 侧 4 字段 before 摘要。
编辑: $.H-LXN-001.name_en/description_en/reason_en/case_en Mao Xiannian->Li Xiannian (4 处, 全文 -4B)。
校验: cd 本目录 && sha256sum -c MANIFEST.sha256; fields_before.json 载有逐字段 before/after_expected 与真字节偏移 (byte_window_before/after)。
