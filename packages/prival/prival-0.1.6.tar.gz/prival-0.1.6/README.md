# PRIVAL 项目文档

## 一、项目简介

PRIVAL（Prompt Input VALidation）是一个轻量级的 Prompt 质量检测框架，提供多维度自动化评分和建议，帮助用户优化输入给大模型的 Prompt，提升模型执行效果。

### 核心特点

- **多维度评分**：自定义清晰度、歧义性、注入风险等 12+ 维度检测，支持启用/禁用及权重配置。
- **插件化设计**：每个维度由独立 detector 模块实现，方便扩展和替换。
- **低代码接口**：一行 `evaluate_prompt(prompt)` 即可获取详细评分和改进建议。
- **报告输出**：支持 JSON、Markdown、HTML 报告，便于可视化和分享。

## 二、安装和使用

```bash
pip install prival
```

```python
from prival import evaluate_prompt

prompt = "请帮我写一封求职邮件，针对 AI 工程师岗位。"
result = evaluate_prompt(prompt)
# result = {
#   "total_score": 0.78,
#   "details": {
#     "clarity": {"score": 0.9, "suggestions": [...]},
#     ...
#   }
# }
```

或在命令行中使用 CLI：

```bash
prival-cli evaluate "你的 prompt 文本"
```

## 三、项目结构

```text
prival/
├── config.yaml               # 全局配置：维度开关、权重、阈值等
├── __init__.py               # 包初始化，导出 evaluate_prompt 接口
├── detectors/                # 独立维度检测器模块
│   ├ clarity.py              # 清晰度检测
│   ├ ambiguity.py            # 歧义性检测
│   ├ step_guidance.py        # 步骤指引检测
│   ├ verbosity.py            # 冗余度检测
│   ├ injection_risk.py       # Injection 风险检测
│   ├ context_completeness.py # 上下文完整性检测
│   ├ ethic_compliance.py     # 伦理合规检测
│   ├ structural_cleanness.py # 结构简洁度检测
│   ├ relevance.py            # 关联度检测
│   ├ feasibility.py          # 可行性检测
│   ├ grammar_spelling.py     # 语法拼写检测
│   ├ length_appropriateness.py # 长度适宜性检测
│   └ diversity.py            # 多样性检测
├── utils/                    # 通用 NLP 辅助工具
│   └ nlp_helpers.py          # 句法解析、关键词抽取、相似度计算等
├── core.py                   # 核心流程：加载配置，调度 detectors 并发执行
├── scoring.py                # 总分计算与格式化输出
├── report.py                 # 报告生成：HTML/Markdown
└── tests/                    # 单元测试和基准 prompt 样本
```

## 四、配置示例（config.yaml）

```yaml
# 启用和权重配置
enabled_dimensions:
  - clarity
  - ambiguity
  - step_guidance
  - verbosity
  - injection_risk
  - context_completeness
  - ethic_compliance
  - structural_cleanness
  - relevance
  - feasibility
  - grammar_spelling
  - length_appropriateness
  - diversity
# politeness 可选，默认关闭
#  - politeness

# 各维度权重（加权得分用）
weights:
  clarity: 0.15
  ambiguity: 0.10
  step_guidance: 0.10
  verbosity: 0.10
  injection_risk: 0.15
  context_completeness: 0.10
  ethic_compliance: 0.10
  structural_cleanness: 0.05
  relevance: 0.05
  feasibility: 0.05
  grammar_spelling: 0.05
  length_appropriateness: 0.05
  diversity: 0.05

# 各维度阈值设置（可选）
thresholds:
  clarity: 0.6
  injection_risk: 0.5
  # 等...
```

## 五、测试和报告

- **单元测试**：在 `tests/` 目录下编写 `pytest` 测试用例，确保各 detector 规则正确。
- **报告生成**：调用 `prival.report.generate_html(result, "report.html")` 一键输出可分享的 HTML 报告，支持图表和建议列表。

---

Happy prompting!  欢迎提交 issue 或 PR，共同完善 PRIVAL。

