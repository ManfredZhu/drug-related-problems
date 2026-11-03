# 药物相关问题分类（DRP）Skill

按《中国药物相关问题分类系统（V1.0）》分析药师工作记录，输出 P / E1 / E2 / C / I / A / O 七类标准化编码，并写入 CSV。

由上海交通大学医学院附属同仁医院制作，反馈渠道见 `SKILL.md` 文首。

## 编码维度

| 维度 | 含义 |
|---|---|
| P | 问题类型 |
| E1 | 涉及的主要对象 |
| E2 | 药品是否已用于患者 |
| C | 原因 |
| I | 介入方案 |
| A | 介入接受情况 |
| O | 问题状态 |

每个维度都附带置信度评分，CSV 中另有一列总体置信度。

## 安装

把整个目录放到你的 skill 目录下，例如：

```bash
git clone https://github.com/ManfredZhu/drug-related-problems.git \
  ~/.config/opencode/skills/drug-related-problems
```

Claude Code 用户放到 `~/.claude/skills/drug-related-problems`。

## 使用

在对话里提到相关短语即可触发，比如「分析药物相关问题」「DRP 分类」「DRP 编码」。

skill 会先判断你给的输入够不够完整：

- **快路径**：材料已包含完整药师工作记录，直接编码，不打断你
- **引导路径**：信息缺失时，按缺失的模块用选项卡片逐项采集，已齐备的模块不重复问

一份材料里如果有多个 DRP，会逐个独立编码，患者 ID 自动加序号（`P001-1`、`P001-2`）。

## 输出

CSV，表头固定 20 列：

```
Patient_ID, Gender, Age, Diagnosis,
P_Code, E1_Code, E2_Code, C_Code, I_Code, A_Code, O_Code,
P_Confidence, E1_Confidence, E2_Confidence, C_Confidence,
I_Confidence, A_Confidence, O_Confidence, Overall_Confidence,
Analysis_Notes, Last_Updated
```

脚本有两种模式，`--mode` 默认为 `append`：

```bash
# 追加记录（文件不存在时自动创建）
python3 scripts/generate_csv.py --input result.json --output drp.csv

# 按 Patient_ID 更新已有记录
python3 scripts/generate_csv.py --input result.json --output drp.csv --mode update
```

输入的 JSON 格式见 `SKILL.md` 的「输入 JSON 格式」一节。

## 目录结构

```
.
├── SKILL.md                       主流程与判定规则
├── references/
│   ├── classification_system.md   分类系统说明
│   └── case_examples.md           案例示例
└── scripts/
    └── generate_csv.py            CSV 生成脚本
```

## 版本

当前 v3.0.2
