# Drug-Related Problems (DRP) Classification Skill

**English** · [简体中文](README.zh-CN.md)

Analyze pharmacist case records against the Chinese Classification System for Drug-Related Problems (V1.0) and produce standardized P / E1 / E2 / C / I / A / O codes written to CSV.

Created by Tongren Hospital, Shanghai Jiao Tong University School of Medicine.

> **Language note.** `SKILL.md` and every interactive prompt, trigger phrase, and option card are written in Chinese. This README is provided so non-Chinese readers can evaluate the project; actually running the skill requires reading Chinese.

## Codes

| Code | Meaning |
|---|---|
| P | Problem type |
| E1 | Primary object involved |
| E2 | Whether the drug has already been given to the patient |
| C | Cause |
| I | Intervention |
| A | Whether the intervention was accepted |
| O | Problem status |

Each dimension carries its own confidence score. The CSV adds one overall confidence column.

## Install

Clone the repository into your skills directory. For OpenCode:

```bash
git clone https://github.com/ManfredZhu/drug-related-problems.git \
  ~/.config/opencode/skills/drug-related-problems
```

For Claude Code, use `~/.claude/skills/drug-related-problems`.

## Usage

Mention a Chinese trigger phrase in the conversation, such as 「分析药物相关问题」, 「DRP 分类」, or 「DRP 编码」.

The skill first checks whether the input is complete enough to encode:

- **Fast path**: the record already contains a full pharmacist work-up, so it encodes directly without interrupting you.
- **Guided path**: when information is missing, it collects the gaps module by module using option cards. Modules that are already complete are not asked again.

If a single case contains multiple DRPs, each one is encoded independently and the patient ID gets a numeric suffix (`P001-1`, `P001-2`).

## Output

A CSV file with a fixed 20-column header:

```
Patient_ID, Gender, Age, Diagnosis,
P_Code, E1_Code, E2_Code, C_Code, I_Code, A_Code, O_Code,
P_Confidence, E1_Confidence, E2_Confidence, C_Confidence,
I_Confidence, A_Confidence, O_Confidence, Overall_Confidence,
Analysis_Notes, Last_Updated
```

`scripts/generate_csv.py` has two modes; `--mode` defaults to `append`:

```bash
# Append a record (creates the file if it does not exist)
python3 scripts/generate_csv.py --input result.json --output drp.csv

# Update existing records matched by Patient_ID
python3 scripts/generate_csv.py --input result.json --output drp.csv --mode update
```

The input JSON schema is documented in the 「输入 JSON 格式」 section of `SKILL.md`.

## Layout

```
.
├── SKILL.md                       Workflow and decision rules
├── references/
│   ├── classification_system.md   Classification system reference
│   └── case_examples.md           Worked examples
└── scripts/
    └── generate_csv.py            CSV writer
```

## Version

v3.0.2
