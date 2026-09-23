# Phase21 W4 名录修复·执行报告 (卡 t_536073f4)

- 卡号: t_536073f4 (单写者执行卡); 依据: docs/research/phase21w4_fix_manifest.md/.json (清单卡 t_10a42b2a, 唯一执行依据)
- 上级门控: t_25453b39 (W5 链尾, done); 下游: t_ee203180 (RW-KAG-1..27 清档) -> t_8bad8d98 (QA) -> t_616e4991 (文档)
- 证据 JSON: docs/research/phase21w4_fix_evidence.json (逐码前像/后像/差异字段/门禁/回执, 机器可读)
- 备份: data/backup_phase21w4_fix_20260924/ (11 件 payload + MANIFEST.sha256 + backup_manifest.json, byte-exact)

## 一, 结论速览 (全部实测)

| 项 | 值 |
|---|---|
| 源键集 | scenarios_zh 1070 -> 1068; scenarios_en 1070 -> 1068 (含新增/删除净值) |
| DB figures | 1056 -> 1054 (-2 清档; JP/UZ 重键净 0) |
| 路由 web_p0_routes | 1387 -> 1385; sitemap 1388 -> 1386 |
| 21 码 name 全链非空 | PASS (DB/shard/轻索引/统一索引/路由/sitemap 逐码核验, 见证据 JSON per_code) |
| SG-Lee-001/MY-Mah-001 全链残留 | 0 (链上 7 层 + 全仓 rg, 报告/备份类除外) |
| 重键旧码 JP-Sas-001/UZ-Ulu-001 悬空 | 0 (旧码全链消失, 新码 JP-SAS-001/UZ-ULU-001 生成) |
| 计数自洽 | figures 1054 / unified 1369 = 318 + 1051 / by-figure 318 / modes 3221 / sitemap 1386 全对 |
| 门禁四连 | credibility rc=0 / source_links rc=0 / findings rc=0 / ci_data_check 24/24 PASS |
| preflight | stage=data PASS; stage=dist PASS |
| 差异面 | 仅目标码集 + 锚点 + 重建产物 + W5 未收敛四态自然收敛 (见第五节) |

## 二, 逐码执行结果

### 2.1 R1 16 H-* name 回填 (scenarios_zh/en 双源)

16 码全部写入 name 短名 (zh/en), 与 manifest f) 终表逐字一致:
H-HYP-145 黄炎培 / H-WYX-146 吴有训 / H-WX-147 王选 / H-YLP-148 袁隆平 / H-SY-149 粟裕 / H-XMQ-151 薛暮桥 / H-CY-159 陈毅 / H-LXN-347 李先念 / H-LXN-001 李先念 / H-IKD-160 伊本·赫勒敦 / H-ISC-362 阿维森纳 (伊本·西那) / H-GHZ-163 安萨里 / H-SUF-364 鲁米 (贾拉勒丁·鲁米) / H-ZEL-001 周恩来 / H-HLG-001 华罗庚 / H-MZ-001 晏阳初 (en: Y. C. James Yen)。
口径注记 (依 R8): 仅新增 name 键; 既有 name_zh/name_en 长串保留不动。

### 2.2 R2 错名修正 (毛先念 / Mao Xiannian -> 李先念 / Li Xiannian)

- tools/json/H-LXN-001.json: 8 个字段 (name/description/reason/case 的 zh/en) 逐字替换。
- scenarios_zh.json: name_zh/description_zh/reason_zh/case_zh 4 处 (manifest 实测扩展项 8-1, 同批改)。
- scenarios_en.json: name_en (R2 字面) + description_en/reason_en/case_en 3 处 (随 R2 同步)。
- docs/figures/H-LXN-001.md: 不改 (见第六节 R-c: 实测 2 处为「误写说明」注记, 非错名正文)。
- 根目录 H-LXN-001.json: 不动 (manifest 定为 R7 旁项/待复核, 见第六节 R-b)。

### 2.3 R4/R5 SG/MY 归一

- 保留码回填: SG-LEE-001 name=李光耀 / Lee Kuan Yew; MY-MAH-001 name_zh=马哈蒂尔 (en 保持 Mahathir Mohamad)。
- 清档: SG-Lee-001, MY-Mah-001 全链清除 (双源整条 + 草稿 + DB 行 + shard + 轻索引 + 统一索引 + 路由 + sitemap)。

### 2.4 R6/R7 JP/UZ 重键

- JP-Sas-001 -> JP-SAS-001 (西乡隆盛 / Saigō Takamori); UZ-Ulu-001 -> UZ-ULU-001 (乌鲁格别克 / Ulugh Beg)。
- 旧条目整条迁移不改内容, 新键设 name; 旧码草稿 JP-Sas-001.json / UZ-Ulu-001.json 已删。
- 旧码全链 0 残留 (含发布面, 镜像后复核); 新码全链生成。

### 2.5 R9 RW-KAG-001 回填 + R10 归属

- scenarios_zh name=卡加梅; scenarios_en name=Paul Kagame (短名回填)。
- R10 (RW-KAG-1..27 清档) 不在本卡: 归属下游卡 t_ee203180 (本卡仅清单/扫描/备份模板确认)。

### 2.6 草稿删除

tools/json/ 下 4 件清档码草稿删除: SG-Lee-001.json / MY-Mah-001.json / JP-Sas-001.json / UZ-Ulu-001.json (均已 byte-exact 备份)。

## 三, 重建链与锚点 (取重建后实测, 禁止照抄预测)

链 (全绿): build_figures_db(1054) -> export_static_site(figures=1054 / modes 3281, 发布 3221 / by-figure 318) -> gen_web_site_counts -> build_daily_index(318) -> pages_preflight --stage data -> build_search_index / build_graph_data -> build_unified_index(1369) -> 门禁四连 -> npm run build -> pages_preflight --stage dist -> prerender_routes(--body-persons all, 1385) -> apply_site_counts(零违规) / build_sw / build_sitemap(1386)。

锚点同提交更新:
- tools/export_static_site.py L75: EXPECT_FIGURES 1056 -> 1054 (实测; manifest 预测 1028 系全批终值, 该值含 RW-KAG-1..27 清档, RW 清档归下游卡 t_ee203180; 本卡后为 1054, RW 卡落地时需再重锚 1054 -> 1027)。
- tools/pages_preflight.py L26: 同步 1054 (其余 3281/318/8 不变)。
- tools/ci_data_check.py L53: MIN_SITEMAP_ENTRIES 1388 -> 1386 (实测)。
- web/src/api/static.ts L13/L15 注释: 1056 -> 1054 (建议项 8-6, 按实测执行)。
- web/src/views/ApiDocsView.vue L11 文案: 1057 -> 1054 (同上)。
- meta.json / static_data_manifest.json / routes 计数为重建自动产物 (1054/1385/1386)。

环境裁剪 (参照 AZJ 先例, 逐条给出理由):
- mkdocs/site_docs: 本地未构建 (mkdocs 未安装; site_docs/** 为 gitignore 产物, CI 部署时构建)。
- apply_og_meta: 本地跳过 (需先跑 build_og_images 且 pillow 未安装; 产物在 dist 内, CI pages.yml 部署时执行)。
- generate_library.py: 未跑 (manifest 无此项指令/判定; 实测 manifest 全文 0 次命中)。

## 四, 验证 (全部实测, 机器可读见证据 JSON)

1. **21 码 name 全链非空**: 逐码 6 层 (DB / shard / 轻索引 / 统一索引 / 路由 / sitemap) PASS; person 型 H-HLG-001 走 /minds/ 路由与 sitemap 命中。
2. **残件 0 残留**: SG-Lee-001 / MY-Mah-001 / JP-Sas-001 / UZ-Ulu-001 在全链 7 层与全仓 rg (排除报告/备份/site_docs/.git) 均 0 命中。
3. **重键 0 悬空**: 旧码全链消失 + 新码全链生成; 引用扫描 (manifest d) 方法) 复核 0 存活引用。
4. **计数自洽**: figures 1054 = DB 行 = shard 数 = 轻索引条数 = meta.counts.figures; sitemap 1386 = 路由 1385 + 首页; unified 1369 = 318 + 1051; by-figure 318 不变; 发布模式 3221 不变。
5. **门禁**: credibility_gate --hard-fail rc=0 (存量冻结); verify_source_links --hard-fail rc=0 (无新增坏链); verify_findings rc=0 (1 条既有 M-ASM 双采 warning); ci_data_check 24 条断言 0 失败; pages_preflight data/dist 全断言通过。
6. **stale 数字残留**: 全仓 rg 1056/1057/1388 在活文件中的旧值引用已清零 (仅历史/报告存量)。
7. **parity**: 见第七节回执 (镜像后复测)。

## 五, 差异面与预期外收敛说明

- **差异面 = 目标码集 + 锚点 + 重建产物**; 源级结构 diff 仅 name/整条增删: zh +2/-4/19 码 changed (仅 name), en +2/-4/18 码 (H-LXN-001 含 5 字段), 草稿 8 字段。
- **W5 四态自然收敛 (登记, 非本卡手工改)**: siteCounts.ts 与 routes 可信度标题由 931/1916/34 -> 949/1897/35 (+verified 18, +suspect 1)。根因: W5 卡 (18405015, 04:16) 更新 modes_data 验证状态后未重构站点链 (站点链上次重构 0cbf6ab6, 01:05); 本卡重建确定性收敛。未触碰 modes_data.json 与验证登记 (边界 2)。
- **DB id 位移**: 清档 2 行后, 30 个码 id 位移 -2 (DB 每轮由源重建, id 为位置性序号, 非稳定标识); 新码 JP-SAS-001 / UZ-ULU-001 取原位。
- **H-MZ-001** 路由标题随 zh 名变化; MY-MAH-001 en 名无变化 (no-op, 不产生 diff)。
- **JP-SOS-001** (既有并行条目, 非目标码) 在 sitemap 中仅排序位次变化, 内容未动。

## 六, 残留与待复核 (登记, 不静默)

- R-a **他链 parity 缺件 6 件** (发布仓未镜像, 非本卡产物): docs/research/phase21r8_w4_names_recon.md/.json, docs/research/phase21w4_fix_manifest.md/.json, docs/research/phase21w6_marker_scan.md/.json (W5 先例: 登记为他链残差)。
- R-b **根目录 H-LXN-001.json**: 4+4 处错名, manifest 明定「本轮不动」(R7 旁项) -> 保留, 待复核。
- R-c **docs/figures/H-LXN-001.md**: 实测 2 处 毛先念 为「原始...误写为毛先念」的纠错注记 (行 19/143), 改之反成错误; 按实测保留。 manifest「建议同批改」的前提被实测推翻 (实测优先)。
- R-d **R11 两异常名**: data/asia/individuals/ 下两「含换行符名」实测为空目录 (未跟踪, 0 内容; 同名正常文件并存: xue_mu_qiao_H-XMQ-151_modes.json / gong_yu_H-GY-152_modes.json)。 R11 两分支均不适用; manifest 建议 rmdir 属待船长复核项 -> 未删除, 登记移交 (如需删除: rmdir 两空目录即可, 无内容可备份)。
- R-e **CHANGELOG.md**: 历史条目不改写 (manifest 既定)。
- R-f **RW-KAG-1..27 清档 + code_maps_en 27 占位键删除**: 下游卡 t_ee203180 (8-5 待船长确认项)。
- R-h **code_maps_en.json**: 本卡 21 码逐码核验无需变更 (H-* 现有值均为正确文案; 旧 4 码 0 键残留; JP/UZ 无键)。
- R-i **figure_names.json**: 本卡 21 码核验: H-GHZ-163=安萨里 / H-HLG-001=华罗庚 / H-MZ-001=晏阳初 键值正确; JP/UZ/SG/MY 旧码新码均无键 (无需更新); 旧 4 码 0 残留复核结果 PASS (逐码逐层 0 命中)。

## 七, 回执 (提交/镜像/push/parity)

- 工作仓 commit: e7be5cc6 (主体: 数据 + 代码 + 备份 + 报告 v1; 28 files changed, +25261 / -136)。
- 工作仓 HEAD (报告 v2 提交前): e7be5cc6aec80d998887d3c62cfac05d14d42edd。
- 发布仓镜像 commit: da1e9bc (15 file byte-exact + 备份件 13/13 + 4 重键草稿删除归档; parity: 共同件 2291 = 逐字节 2291, CONTENT_DIFF 0, only_publish 0; MISSING_IN_PUBLISH 6 件他链文档, 见 R-a)。
- push: 465c19a..da1e9bc main -> main rc=0; ls-remote remote main = da1e9bc9634f7c0b3a250241de4d21e1308fb72f (与本地一致)。
- 远端 raw 校验: 4/4 逐字节一致 (report 41e2fa8f / H-LXN-001.json fc6e9884 / static.ts 9917a7b1 / export_static_site.py bfc6514a, 前 16 位)。
- 备份 sha 清单: data/backup_phase21w4_fix_20260924/MANIFEST.sha256 (11 件 before sha, 读取即验)
- 报告 v2 镜像 push 回执: 8ca52c04 -> faccfbe (main -> main rc=0); remote main = faccfbeaaa27a98b8cb9b33de123453d50025452; 报告 v2 sha256(前 16 位) = d2dc8e53cff9d366。
