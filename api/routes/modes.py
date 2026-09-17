# Protreptic Modes Routes
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List, Dict, Any

from ..database import get_db
from ..models import Figure
from ..schemas import ModeListResponse, ModeResponse

router = APIRouter()


# In-memory modes data (will be loaded from JSON)
MODES_DATA = {
    1: {"name_zh": "矛盾分析法", "name_en": "Contradiction Analysis", "description_zh": "抓主要矛盾，抓矛盾主要方面", "description_en": "Grasp the principal contradiction, grasp the principal aspect of the contradiction", "formula_zh": "主要矛盾 → 主要方面 → 集中力量 → 解决", "formula_en": "Principal contradiction → principal aspect → concentrate forces → resolve", "domain_zh": "战略", "domain_en": "Strategic"},
    2: {"name_zh": "群众路线法", "name_en": "Mass Line", "description_zh": "从群众中来，到群众中去", "description_en": "From the masses, to the masses", "formula_zh": "群众意见 → 集中提炼 → 返还群众 → 坚持到底", "formula_en": "Mass opinions → concentrate → return to masses → persist", "domain_zh": "战略", "domain_en": "Strategic"},
    3: {"name_zh": "持久战思维", "name_en": "Protracted War", "description_zh": "战略防御→相持→战略反攻", "description_en": "Strategic defense → stalemate → strategic counter-offensive", "formula_zh": "防御积累 → 相持消耗 → 反攻决胜", "formula_en": "Defense accumulation → stalemate attrition → counter-offensive victory", "domain_zh": "战略", "domain_en": "Strategic"},
    4: {"name_zh": "农村包围城市", "name_en": "Rural Encirclement of Cities", "description_zh": "避强击弱，积小胜为大胜", "description_en": "Avoid the strong, strike the weak; accumulate small victories into big victory", "formula_zh": "建立根据地 → 武装割据 → 逐步扩大 → 最后夺取城市", "formula_en": "Establish base areas → armed separatism → gradual expansion → final seizure of cities", "domain_zh": "战略", "domain_en": "Strategic"},
    5: {"name_zh": "实事求是法", "name_en": "Seeking Truth from Facts", "description_zh": "一切从实际出发，理论联系实际", "description_en": "Start from reality, link theory with practice", "formula_zh": "调查研究 → 理论建模 → 实证验证 → 迭代修正", "formula_en": "Investigation → modeling → empirical verification → iterative correction", "domain_zh": "分析", "domain_en": "Analytical"},
    6: {"name_zh": "统一战线法", "name_en": "United Front", "description_zh": "团结一切可以团结的力量", "description_en": "Unite all forces that can be united", "formula_zh": "共同敌人 × 利益绑定 × 信任机制 = 联盟稳固度", "formula_en": "Common threat × interest binding × trust = alliance stability", "domain_zh": "协作", "domain_en": "Collaborative"},
    7: {"name_zh": "战略预判法", "name_en": "Strategic Foresight", "description_zh": "预判趋势，先发制人", "description_en": "Anticipate trends, seize initiative", "formula_zh": "趋势研判 → 关键变量 → 先手布局 → 主动控制", "formula_en": "Trend analysis → key variables → preemptive layout → proactive control", "domain_zh": "战略", "domain_en": "Strategic"},
    8: {"name_zh": "渐进改革法", "name_en": "Gradual Reform", "description_zh": "摸石头过河，小步快跑", "description_en": "Cross the river by feeling the stones; small steps, fast pace", "formula_zh": "试点验证 → 经验总结 → 分阶段推广 → 标准化固化", "formula_en": "Pilot verification → experience summary → phased rollout → standardization", "domain_zh": "操作", "domain_en": "Operational"},
    9: {"name_zh": "独立自主法", "name_en": "Self-Reliance", "description_zh": "自力更生，掌握核心", "description_en": "Self-reliance, master the core", "formula_zh": "核心技术自主 × 供应链可控 = 战略安全", "formula_en": "Core tech autonomy × supply chain control = strategic security", "domain_zh": "操作", "domain_en": "Operational"},
    10: {"name_zh": "批评与自我批评", "name_en": "Criticism and Self-Criticism", "description_zh": "刮骨疗毒，治病救人", "description_en": "Cure the sickness to save the patient", "formula_zh": "公开复盘 × 自我剖析 × 相互监督 = 文化免疫力", "formula_en": "Public review × self-analysis × mutual supervision = cultural immunity", "domain_zh": "协作", "domain_en": "Collaborative"},
    11: {"name_zh": "灵活策略法", "name_en": "Flexible Strategy", "description_zh": "因时制宜，随机应变", "description_en": "Adapt to circumstances, respond flexibly", "formula_zh": "环境感知 × 快速决策 × 快速执行 = 适应性", "formula_en": "Environment sensing × rapid decision × rapid execution = adaptability", "domain_zh": "操作", "domain_en": "Operational"},
    12: {"name_zh": "系统思维法", "name_en": "Systems Thinking", "description_zh": "整体大于部分之和", "description_en": "The whole is greater than the sum of parts", "formula_zh": "要素 × 关系 × 环境 = 系统涌现", "formula_en": "Elements × relationships × environment = system emergence", "domain_zh": "系统", "domain_en": "Systems"},
    13: {"name_zh": "全胜思维法", "name_en": "Total Victory", "description_zh": "不战而屈人之兵", "description_en": "Subdue the enemy without fighting", "formula_zh": "威慑 × 合法性 × 叙事控制 = 无形胜利", "formula_en": "Deterrence × legitimacy × narrative control = invisible victory", "domain_zh": "战略", "domain_en": "Strategic"},
    14: {"name_zh": "战争重心法", "name_en": "Center of Gravity (Warfare)", "description_zh": "集中优势兵力，各个歼灭", "description_en": "Concentrate superior forces, annihilate piecemeal", "formula_zh": "重心识别 → 优势集中 → 歼灭打击 → 战果转化", "formula_en": "CoG identification → force concentration → annihilation → conversion", "domain_zh": "战略", "domain_en": "Strategic"},
    15: {"name_zh": "运动歼灭战", "name_en": "Maneuver Annihilation", "description_zh": "运动中歼灭，不以城地为得失", "description_en": "Annihilate in motion, not for cities", "formula_zh": "机动 × 集中 × 歼灭 = 敏捷优势", "formula_en": "Maneuver × concentration × annihilation = agile advantage", "domain_zh": "战略", "domain_en": "Strategic"},
    16: {"name_zh": "游击战十六字诀", "name_en": "Sixteen-Character Guerrilla Formula", "description_zh": "敌进我退，敌驻我扰，敌疲我打，敌退我追", "description_en": "Enemy advances, we retreat; enemy halts, we harass; enemy tires, we attack; enemy retreats, we pursue", "formula_zh": "避实击虚 × 消耗耐心 × 反击致胜", "formula_en": "Avoid strength strike weakness × exhaust patience × counter-attack victory", "domain_zh": "战略", "domain_en": "Strategic"},
    17: {"name_zh": "多元思维模型", "name_en": "Multiple Mental Models", "description_zh": "多模型思考，避免单一模型陷阱", "description_en": "Multi-model thinking, avoid single-model trap", "formula_zh": "模型集合 × 权重分配 = 综合判断", "formula_en": "Model ensemble × weight allocation = composite judgment", "domain_zh": "分析", "domain_en": "Analytical"},
    18: {"name_zh": "目标管理法", "name_en": "Management by Objectives", "description_zh": "目标对齐，结果导向", "description_en": "Goal alignment, results-oriented", "formula_zh": "目标清晰度 × 关键结果可衡量 × 复盘频次 = 执行力", "formula_en": "Goal clarity × KR measurability × review frequency = execution", "domain_zh": "协作", "domain_en": "Collaborative"},
    19: {"name_zh": "边际思维法", "name_en": "Marginal Thinking", "description_zh": "边际收益递减，边际决策", "description_en": "Diminishing marginal returns, marginal decision", "formula_zh": "最优点 = 边际收益 = 边际成本", "formula_en": "Optimum = marginal benefit = marginal cost", "domain_zh": "分析", "domain_en": "Analytical"},
    20: {"name_zh": "博弈论思维", "name_en": "Game Theory", "description_zh": "纳什均衡，互动策略", "description_en": "Nash equilibrium, interactive strategy", "formula_zh": "最优策略 = argmax Σ(收益 × 概率)", "formula_en": "Optimal strategy = argmax Σ(payoff × probability)", "domain_zh": "分析", "domain_en": "Analytical"},
    21: {"name_zh": "损失厌恶法", "name_en": "Loss Aversion", "description_zh": "避免损失重于追求收益", "description_en": "Avoiding loss outweighs pursuing gain", "formula_zh": "风险决策 = max(收益概率×收益) - λ×(损失概率×损失) λ≈2.25", "formula_en": "Risk decision = max(gain_prob×gain) - λ×(loss_prob×loss) λ≈2.25", "domain_zh": "个人", "domain_en": "Personal"},
    22: {"name_zh": "总体性思维", "name_en": "Holistic Thinking", "description_zh": "整体大于部分之和", "description_en": "The whole is greater than the sum of parts", "formula_zh": "整体价值 = Σ部分价值 + 结构耦合增值 - 耦合成本", "formula_en": "Whole value = Σpart values + structural coupling gain - coupling cost", "domain_zh": "系统", "domain_en": "Systems"},
    23: {"name_zh": "自然选择法", "name_en": "Natural Selection", "description_zh": "适者生存，优胜劣汰", "description_en": "Survival of the fittest", "formula_zh": "变异 × 选择 × 保留 = 适应性进化", "formula_en": "Variation × selection × retention = adaptive evolution", "domain_zh": "创新", "domain_en": "Creative"},
    24: {"name_zh": "间断均衡法", "name_en": "Punctuated Equilibrium", "description_zh": "长期稳定，短期突变", "description_en": "Long-term stability, short-term disruption", "formula_zh": "突破 = 长期积累 × 关键触发 × 爆发力度", "formula_en": "Breakthrough = long accumulation × trigger × explosion force", "domain_zh": "分析", "domain_en": "Analytical"},
    25: {"name_zh": "抽象归纳法", "name_en": "Abstraction and Induction", "description_zh": "从具体到抽象，建立模型", "description_en": "From concrete to abstract, build models", "formula_zh": "观察 → 模式识别 → 抽象建模 → 验证", "formula_en": "Observation → pattern recognition → abstraction → verification", "domain_zh": "分析", "domain_en": "Analytical"},
    26: {"name_zh": "知行合一法", "name_en": "Unity of Knowledge and Action", "description_zh": "知是行之始，行是知之成", "description_en": "Knowledge is the beginning of action; action is the completion of knowledge", "formula_zh": "知 = 行之始，行 = 知之成", "formula_en": "Knowing = action's beginning, action = knowing's completion", "domain_zh": "个人", "domain_en": "Personal"},
    27: {"name_zh": "双系统思维", "name_en": "Dual-System Thinking", "description_zh": "系统1快/系统2慢", "description_en": "System 1 fast / System 2 slow", "formula_zh": "最优决策 = 系统1(直觉) × 权重1 + 系统2(分析) × 权重2", "formula_en": "Optimal decision = System1(intuition) × w1 + System2(analysis) × w2", "domain_zh": "系统", "domain_en": "Systems"},
    28: {"name_zh": "摸石头过河", "name_en": "Crossing River by Feeling Stones", "description_zh": "试错学习，渐进迭代", "description_en": "Trial and error, iterative progress", "formula_zh": "试错 × 反馈 × 修正 × 固化 = 可复制路径", "formula_en": "Trial × feedback × correction × solidification = replicable path", "domain_zh": "操作", "domain_en": "Operational"},
    29: {"name_zh": "反馈回路法", "name_en": "Feedback Loop", "description_zh": "负反馈稳定，正反馈放大", "description_en": "Negative feedback stabilizes, positive feedback amplifies", "formula_zh": "系统稳定性 = 负反馈强度 / 正反馈强度", "formula_en": "System stability = negative feedback strength / positive feedback strength", "domain_zh": "分析", "domain_en": "Analytical"},
    30: {"name_zh": "框架效应法", "name_en": "Framing Effect", "description_zh": "重构框架，改变决策", "description_en": "Reframe to change decisions", "formula_zh": "决策改变 = 新框架认知差异 × 决策敏感度", "formula_en": "Decision change = new frame cognitive diff × decision sensitivity", "domain_zh": "分析", "domain_en": "Analytical"},
    31: {"name_zh": "制度化制衡法", "name_en": "Institutional Checks and Balances", "description_zh": "权力制衡，制度保障", "description_en": "Power checks, institutional guarantees", "formula_zh": "治理稳定性 = (制衡完备度 × 执行力度) / 权力集中度", "formula_en": "Governance stability = (checks completeness × enforcement) / power concentration", "domain_zh": "系统", "domain_en": "Systems"},
    32: {"name_zh": "三衙分兵法", "name_en": "Three-Agency Military Separation", "description_zh": "权力分立，相互制衡", "description_en": "Power separation, mutual checks", "formula_zh": "治理效率 = 职责清晰度 × 制衡有效性 / 协调成本", "formula_en": "Governance efficiency = responsibility clarity × check effectiveness / coordination cost", "domain_zh": "系统", "domain_en": "Systems"},
    33: {"name_zh": "制度化制衡法", "name_en": "Institutional Checks and Balances", "description_zh": "三权分立，相互制衡", "description_en": "Separation of powers, mutual checks", "formula_zh": "三权分立 × 相互制约 = 治理稳定性", "formula_en": "Power separation × mutual restraint = governance stability", "domain_zh": "战略", "domain_en": "Strategic"},
    34: {"name_zh": "鸟笼经济法", "name_en": "Birdcage Economy", "description_zh": "计划为笼，市场为鸟", "description_en": "Plan as cage, market as bird", "formula_zh": "经济效率 = 计划约束强度 × 市场配置效率 / 扭曲成本", "formula_en": "Economic efficiency = plan constraint × market efficiency / distortion cost", "domain_zh": "操作", "domain_en": "Operational"},
    35: {"name_zh": "知行合一法", "name_en": "Unity of Knowledge and Action", "description_zh": "知是行之始，行是知之成", "description_en": "Knowledge begins action; action completes knowledge", "formula_zh": "执行力 = 认知深度 × 行动力度 × 反馈频次 × 迭代次数", "formula_en": "Execution = cognitive depth × action force × feedback freq × iterations", "domain_zh": "操作", "domain_en": "Operational"},
    36: {"name_zh": "三省吾身法", "name_en": "Threefold Self-Examination", "description_zh": "日三省吾身", "description_en": "Examine myself three times daily", "formula_zh": "成长率 = Σ(反思深度 × 反思频次 × 落地转化) / 时间", "formula_en": "Growth rate = Σ(reflection depth × frequency × conversion) / time", "domain_zh": "个人", "domain_en": "Personal"},
    37: {"name_zh": "童心说法", "name_en": "Childlike Heart", "description_zh": "童心无妄，良知即童心", "description_en": "Childlike heart is pure, conscience is childlike heart", "formula_zh": "创新力 = 童心纯度 × 知识广度 × 行动力度 / 世俗杂质", "formula_en": "Innovation = heart purity × knowledge breadth × action force / impurities", "domain_zh": "个人", "domain_en": "Personal"},
    38: {"name_zh": "冗余备份法", "name_en": "Redundancy and Backup", "description_zh": "关键节点多重备份", "description_en": "Critical nodes with multiple backups", "formula_zh": "可用性 = 1 - (单点故障率)^冗余度", "formula_en": "Availability = 1 - (single point failure rate)^redundancy", "domain_zh": "操作", "domain_en": "Operational"},
    39: {"name_zh": "边际思维法", "name_en": "Marginal Thinking", "description_zh": "边际收益递减，边际决策", "description_en": "Diminishing marginal returns, marginal decision", "formula_zh": "边际决策 = 边际收益 = 边际成本", "formula_en": "Marginal decision = marginal benefit = marginal cost", "domain_zh": "战略", "domain_en": "Strategic"},
    40: {"name_zh": "边界思维法", "name_en": "Boundary Thinking", "description_zh": "明确边界，跨界创新", "description_en": "Clear boundaries, cross-boundary innovation", "formula_zh": "生态价值 = 内部聚焦度 × 外部连接数 × 连接质量", "formula_en": "Ecosystem value = internal focus × external connections × connection quality", "domain_zh": "操作", "domain_en": "Operational"},
    41: {"name_zh": "驿站制法", "name_en": "Relay Station System", "description_zh": "信息传递，接力传承", "description_en": "Information relay, generational transmission", "formula_zh": "传递效率 = (接力节点数 × 接口标准化度 × 信息完整性) / 传递延迟", "formula_en": "Relay efficiency = (nodes × interface standardization × info integrity) / latency", "domain_zh": "操作", "domain_en": "Operational"},
    42: {"name_zh": "三民主义法", "name_en": "Three Principles of the People", "description_zh": "民族、民权、民生", "description_en": "Nationalism, Democracy, People's Livelihood", "formula_zh": "治理合法性 = 民族认同 × 民权保障 × 民生改善 / 执行成本", "formula_en": "Governance legitimacy = national identity × democracy × livelihood / cost", "domain_zh": "个人", "domain_en": "Personal"},
}


@router.get("", response_model=ModeListResponse)
async def list_modes(lang: str = Query("zh", pattern="^(zh|en)$")):
    """List all thinking modes."""
    items = []
    for mode_id, data in MODES_DATA.items():
        items.append(
            ModeResponse(
                id=mode_id,
                name=data[f"name_{lang}"],
                name_en=data["name_en"],
                description=data[f"description_{lang}"],
                description_en=data["description_en"],
                formula=data[f"formula_{lang}"],
                formula_en=data["formula_en"],
                domain=data[f"domain_{lang}"],
                domain_en=data["domain_en"],
            )
        )
    return ModeListResponse(data=sorted(items, key=lambda x: x.id))


@router.get("/{mode_id}", response_model=ModeResponse)
async def get_mode(mode_id: int, lang: str = Query("zh", pattern="^(zh|en)$")):
    """Get a specific thinking mode."""
    if mode_id not in MODES_DATA:
        raise HTTPException(status_code=404, detail="Mode not found")
    data = MODES_DATA[mode_id]
    return ModeResponse(
        id=mode_id,
        name=data[f"name_{lang}"],
        name_en=data["name_en"],
        description=data[f"description_{lang}"],
        description_en=data["description_en"],
        formula=data[f"formula_{lang}"],
        formula_en=data["formula_en"],
        domain=data[f"domain_{lang}"],
        domain_en=data["domain_en"],
    )