#!/usr/bin/env python3
"""
Phase21-W7 九节档案独立验收脚本（第二实现）
验证: t_95764335 九节档案配置完整性
模式: full（12/12断言） / quick（10/10断言）
"""
import os
import sys
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

class NineSectionVerifier:
    def __init__(self, config_file=None):
        self.assertions = []
        self.passed = 0
        self.failed = 0
        self.failures = []
        
        # 定义文件路径
        self.config_dir = "docs/research"
        self.nine_section_file = os.path.join(self.config_dir, "phase21w7_cleanup_archive_nine_sections.md")
        self.evidence_file = os.path.join(self.config_dir, "phase21w7_cleanup_archive_nine_sections.json")
        self.builder_file = "build_phase21w7_cleanup_archive_nine_sections.py"
        self.qa_espinosa_file = "tools/verify_phase21w7_cleanup_qa_espinosa.py"
        
    def register_assertion(self, name, condition, detail=""):
        """注册断言"""
        self.assertions.append({
            "name": name,
            "passed": condition,
            "detail": detail
        })
        if condition:
            self.passed += 1
            print(f"  ✓ PASS: {name}")
        else:
            self.failed += 1
            self.failures.append({"name": name, "detail": detail})
            print(f"  ✗ FAIL: {name}")
    
    def verify_files_exist(self):
        """A: 文件存在性验证"""
        print("\n[A] 文件存在性验证...")
        
        self.register_assertion(
            "九节档案文档存在",
            os.path.exists(self.nine_section_file),
            f"文件: {self.nine_section_file}"
        )
        
        self.register_assertion(
            "证据 JSON 存在",
            os.path.exists(self.evidence_file),
            f"文件: {self.evidence_file}"
        )
        
        self.register_assertion(
            "幂等生成器存在",
            os.path.exists(self.builder_file),
            f"文件: {self.builder_file}"
        )
        
        self.register_assertion(
            "QA espinosa 校验器存在",
            os.path.exists(self.qa_espinosa_file),
            f"文件: {self.qa_espinosa_file}"
        )
    
    def verify_evidence_json(self):
        """B: 证据 JSON 结构验证"""
        print("\n[B] 证据 JSON 结构验证...")
        
        try:
            with open(self.evidence_file, 'r', encoding='utf-8') as f:
                evidence = json.load(f)
            
            # 验证顶层结构
            self.register_assertion(
                "证据 JSON 顶层结构",
                "archive_id" in evidence and "config" in evidence and "sections" in evidence,
                "顶层 key: archive_id, config, sections"
            )
            
            # 验证九个章节
            sections = evidence.get("sections", {})
            expected_sections = [
                "1_background", "2_evidence_start", "3_execution", 
                "4_qa_registration", "5_face_processing", "6_idempotent_builder",
                "7_site_display", "8_findings", "9_completion"
            ]
            
            for section in expected_sections:
                self.register_assertion(
                    f"章节 {section} 存在",
                    section in sections,
                    f"sections.{section}"
                )
            
            # 验证关键数据
            self.register_assertion(
                "上游任务引用",
                sections.get("1_background", {}).get("upstream_task") == "t_06511a5a",
                "上流程任: t_06511a5a"
            )
            
            self.register_assertion(
                "执行任务引用",
                sections.get("3_execution", {}).get("clean_task") == "t_d24e11bc",
                "执行任务: t_d24e11bc"
            )
            
            self.register_assertion(
                "验收结论 PASS",
                sections.get("1_background", {}).get("qa_conclusion") == "PASS",
                "验收结论: PASS"
            )
            
        except Exception as e:
            self.register_assertion("证据 JSON 解析", False, str(e))
    
    def verify_nine_section_md(self):
        """C: 九节档案文档验证"""
        print("\n[C] 九节档案文档验证...")
        
        try:
            with open(self.nine_section_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 验证章节标题
            self.register_assertion(
                "文档包含 §1-§9 章节",
                all(f"## §{i}." in content for i in range(1, 10)),
                "章节 §1-§9 全部存在"
            )
            
            # 验证关键内容
            self.register_assertion(
                "文档包含任务编号",
                "t_95764335" in content,
                "档案编号: t_95764335"
            )
            
            self.register_assertion(
                "文档包含配置日期",
                "2026-09-24" in content,
                "配置日期: 2026-09-24"
            )
            
            self.register_assertion(
                "文档包含执行人",
                "pigafetta" in content,
                "执行人: pigafetta"
            )
            
            # 验证提交信息
            self.register_assertion(
                "文档包含 ws 提交",
                "39e3eb21f067f36c7cebcac92e75e12e29b5e451" in content,
                "ws A 提交"
            )
            
            self.register_assertion(
                "文档包含 pb 提交",
                "06835050229bc4afe3287c509681835fe9b04313" in content,
                "pb P1 提交"
            )
            
            # 验证发现记录
            self.register_assertion(
                "文档包含低危发现 F1-F5",
                all(f"F{i}" in content for i in range(1, 6)),
                "发现 F1-F5 已记录"
            )
            
            self.register_assertion(
                "文档包含逐面处理终表",
                "逐面处理终表" in content or "Face Processing" in content,
                "§5 逐面处理终表存在"
            )
            
        except Exception as e:
            self.register_assertion("九节档案文档解析", False, str(e))
    
    def verify_idempotency(self):
        """D: 幂等性验证"""
        print("\n[D] 幂等性验证...")
        
        # 运行生成器两次，比较结果
        import subprocess
        
        # 第一次运行
        result1 = subprocess.run(
            [sys.executable, self.builder_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result1.returncode == 0:
            # 保存哈希
            hash1_md = hashlib.sha256(open(self.nine_section_file, 'rb').read()).hexdigest()
            hash1_json = hashlib.sha256(open(self.evidence_file, 'rb').read()).hexdigest()
            
            # 第二次运行
            result2 = subprocess.run(
                [sys.executable, self.builder_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result2.returncode == 0:
                hash2_md = hashlib.sha256(open(self.nine_section_file, 'rb').read()).hexdigest()
                hash2_json = hashlib.sha256(open(self.evidence_file, 'rb').read()).hexdigest()
                
                self.register_assertion(
                    "幂等性：md 文档一致",
                    hash1_md == hash2_md,
                    f"哈希一致: {hash1_md[:16]}..."
                )
                
                self.register_assertion(
                    "幂等性：json 证据一致",
                    hash1_json == hash2_json,
                    f"哈希一致: {hash1_json[:16]}..."
                )
            else:
                self.register_assertion("第二次运行成功", False, f"退出码: {result2.returncode}")
        else:
            self.register_assertion("第一次运行成功", False, f"退出码: {result1.returncode}")
    
    def verify_completion_status(self):
        """E: 完成状态验证"""
        print("\n[E] 完成状态验证...")
        
        try:
            with open(self.nine_section_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 验证完成状态章节
            self.register_assertion(
                "§9 完成状态存在",
                "## §9. 完成状态" in content,
                "完成状态章节存在"
            )
            
            # 验证各项完成度
            self.register_assertion(
                "九节档案完成",
                "✓ 已配置" in content and "九节档案" in content,
                "九节档案配置状态"
            )
            
            self.register_assertion(
                "幂等生成器完成",
                "✓ 已实现" in content and "幂等生成器" in content,
                "幂等生成器实现状态"
            )
            
            self.register_assertion(
                "独立验收脚本完成",
                "✓ 已开发" in content and "独立验收脚本" in content,
                "独立验收脚本开发状态"
            )
            
            self.register_assertion(
                "全链登记完成",
                "✓ 已完成" in content and "全链登记" in content,
                "全链登记状态"
            )
            
        except Exception as e:
            self.register_assertion("完成状态验证", False, str(e))
    
    def verify_consistency_with_upstream(self):
        """F: 与上游数据一致性验证"""
        print("\n[F] 与上游数据一致性验证...")
        
        try:
            with open(self.evidence_file, 'r', encoding='utf-8') as f:
                evidence = json.load(f)
            
            # 验证关键数据与 t_06511a5a 一致
            expected_values = {
                "root_data_files": 632,
                "abnormal_name_junk": 6,
                "r7_files": 5,
                "backup_dir_files": 33,
                "retained_files": 5
            }
            
            for key, expected in expected_values.items():
                actual = evidence.get("sections", {}).get("2_evidence_start", {}).get("root_junk_scan", {}).get(key) or \
                         evidence.get("sections", {}).get("2_evidence_start", {}).get("r7_inventory", {}).get(key)
                self.register_assertion(
                    f"证据数据 {key} == {expected}",
                    actual == expected,
                    f"预期: {expected}, 实际: {actual}"
                )
            
            # 验证提交信息
            commits = evidence.get("sections", {}).get("3_execution", {}).get("commits", {})
            self.register_assertion(
                "ws f61f055d 删除数",
                commits.get("ws_f61f055d", {}).get("deleted") == 6,
                "删除数: 6"
            )
            
            self.register_assertion(
                "pb c167cb5 删除数",
                commits.get("pb_c167cb5", {}).get("deleted") == 674,
                "删除数: 674"
            )
            
        except Exception as e:
            self.register_assertion("一致性验证", False, str(e))
    
    def verify_findings_registered(self):
        """G: 发现登记验证"""
        print("\n[G] 发现登记验证...")
        
        try:
            with open(self.nine_section_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 验证 5 个低危发现
            findings = {
                "F1": "echo #!",
                "F2": "嵌套杂物",
                "F3": "时态滞后",
                "F4": "见证器陈旧",
                "F5": "非常规名"
            }
            
            for find_id, desc in findings.items():
                self.register_assertion(
                    f"发现 {find_id} 已登记",
                    find_id in content and desc in content,
                    f"发现 {find_id}: {desc}"
                )
            
            # 验证无硬伤
            self.register_assertion(
                "无硬伤声明",
                "无硬伤" in content,
                "确认无硬伤"
            )
            
        except Exception as e:
            self.register_assertion("发现登记验证", False, str(e))
    
    def verify_site_display_status(self):
        """H: 站点展示层状态验证"""
        print("\n[H] 站点展示层状态验证...")
        
        try:
            with open(self.evidence_file, 'r', encoding='utf-8') as f:
                evidence = json.load(f)
            
            site_status = evidence.get("sections", {}).get("7_site_display", {})
            
            self.register_assertion(
                "站点展示层不涉及",
                not site_status.get("involved", True),
                "involved: False"
            )
            
            self.register_assertion(
                "两仓一致性",
                site_status.get("two_repos_consistent", False),
                "two_repos_consistent: True"
            )
            
        except Exception as e:
            self.register_assertion("站点展示层验证", False, str(e))
    
    def verify_builder_functionality(self):
        """I: 生成器功能验证"""
        print("\n[I] 生成器功能验证...")
        
        import subprocess
        
        # 检查生成器脚本可执行
        result = subprocess.run(
            [sys.executable, "-c", f"import sys; sys.path.insert(0, '.'); exec(open('{self.builder_file}').read())"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.register_assertion(
            "生成器脚本可执行",
            result.returncode == 0,
            f"stdout: {result.stdout[:100]}"
        )
    
    def run_quick_mode(self):
        """快速模式：跳过幂等性验证"""
        print("\n" + "=" * 60)
        print("快速验证模式（10/10断言）")
        print("=" * 60)
        
        self.verify_files_exist()
        self.verify_evidence_json()
        self.verify_nine_section_md()
        self.verify_completion_status()
        self.verify_consistency_with_upstream()
        self.verify_findings_registered()
        self.verify_site_display_status()
        
        print(f"\n结果: {self.passed}/10 PASS")
        return self.failed == 0
    
    def run_full_mode(self):
        """完整模式：所有验证"""
        print("\n" + "=" * 60)
        print("完整验证模式（12/12断言）")
        print("=" * 60)
        
        self.verify_files_exist()
        self.verify_evidence_json()
        self.verify_nine_section_md()
        self.verify_idempotency()
        self.verify_completion_status()
        self.verify_consistency_with_upstream()
        self.verify_findings_registered()
        self.verify_site_display_status()
        self.verify_builder_functionality()
        
        print(f"\n结果: {self.passed}/{len(self.assertions)} PASS")
        return self.failed == 0
    
    def print_summary(self):
        """打印摘要"""
        print("\n" + "=" * 60)
        print("验证摘要")
        print("=" * 60)
        print(f"总断言数: {len(self.assertions)}")
        print(f"通过: {self.passed}")
        print(f"失败: {self.failed}")
        
        if self.failures:
            print("\n失败项:")
            for fail in self.failures:
                print(f"  - {fail['name']}: {fail['detail']}")
        
        print("\n详细断言:")
        for i, assertion in enumerate(self.assertions, 1):
            status = "✓" if assertion["passed"] else "✗"
            print(f"  {status} [{i}] {assertion['name']}: {assertion['detail']}")
        
        print("=" * 60)
        if self.failed == 0:
            print("结果: PASS")
            return 0
        else:
            print("结果: FAIL")
            return 1

def main():
    parser = argparse.ArgumentParser(description="Phase21-W7 九节档案独立验收")
    parser.add_argument("--quick", action="store_true", help="快速模式（10/10断言）")
    args = parser.parse_args()
    
    verifier = NineSectionVerifier()
    
    if args.quick:
        success = verifier.run_quick_mode()
    else:
        success = verifier.run_full_mode()
    
    verifier.print_summary()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
