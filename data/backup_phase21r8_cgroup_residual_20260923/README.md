# Phase21-R8 C组遗留微收口：改动前字节备份（卡 t_8183b8fd）

- 日期：2026-09-23（CST）；执行：elcano
- 用途：本卡三处逐键微改前的 byte-exact 前像留档（备份而非删除；先取证后动手）
- 恢复法（任一）：
  1. `cp data/backup_phase21r8_cgroup_residual_20260923/<file>.before <原路径>`；
  2. `git show <blob> > <原路径>`（blob 见下表，取自改动前 git 对象库）。

| 原路径 | 备份文件 | bytes | sha256 | git blob | 末次实质提交 |
|---|---|---|---|---|---|
| data/figure_names.json | figure_names.json.before | 30750 | fa4b43d41a8c450e22768745a90b3ff0349ea0dd04235ac5f792791b4de3f661 | 1d071b881bc14b031649aa3dc6e3cda2af5557f1 | d33e1122 |
| data/code_maps.json | code_maps.json.before | 857380 | df62a33f9671702640c3d45cf8996fdce4c3fb87925e432241af008e7b5d2449 | 711c3e508d0ba44a6a43ff6efc3d6801dfd1899d | d33e1122 |
| data/individuals/H-BG-001.json | H-BG-001.json.before | 8859 | f374af6b7937dc2ea963919076701d086820ff0a170ff2abd7c41bc73dd5eba2 | fcc976cedb73bb209885ea22af574bc9967475b9 | f66bb2fd |

两仓同体：三个 before 件的 sha256 与发布仓（/opt/data/release/Protreptic-publish）同名现役件实测一致（改动前）。
本目录随卡提交并镜像发布仓（data/** 属 parity 边界）。
