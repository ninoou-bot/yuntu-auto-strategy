# 🚗 巨量云图汽车版全域策略与资产诊断通用技能 (yuntu-auto-strategy)

[![Skill](https://img.shields.io/badge/Agent%20Skill-Ready-blue.svg)](SKILL.md)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

专为汽车品牌数字营销打造的**巨量云图（OceanEngine Yuntu）全域策略与人群资产诊断 AI Agent 技能库**。  
全量兼容主流 AI Agent（**Google Antigravity、Claude Code、Cursor、GitHub Copilot CLI、Roo Code、Amp** 等）。

---

## 🌟 核心功能特性

1. **⚡ 秒级 5A 数据自动化提取**：封装云图汽车版底层 API，支持任意汽车品牌与车系（已预设传祺全系 17+ 车型 ID），双端（抖音 cdy + 懂车帝 cdc）毫秒级取数。
2. **📊 5A 触点量化阈值与流转系数诊断**：内置官方底层的曝光/点击/播放时长/看后搜判定规则，独家引入 `(A1+A2)/A3` 流转系数对标模型（对标行业 TOP20 均值 8.6）。
3. **⭐ 星图达人 150 分加权考核模型**：从基础流量（100分）、完播互动（10分）、看后主动搜索（20分）到 A3 净增贡献（20分），科学筛选优质合作矩阵与爆文加热决策。
4. **🏷️ 4L 价值体系 × TOP50 心智排名矩阵**：将车系核心卖点（空间/底盘/续航/安全）与云图 TOP50 讨论词排名升降及美誉度定量打通，排查传播盲点。
5. **👥 汽车行业新八大人群 BUY 策略**：基于基础属性 × 汽车属性 × 心智属性聚类，精准输出各圈层（生活精算师、温馨生活家、摩登青年客等）定制化营销切角。
6. **🎨 飞书原生矢量画板（Canvas/SVG）高质感交付**：内置 5 大原生画板 XML 模板，采用绝对坐标防重叠体系，一键生成媲美咨询公司总监级的在线飞书复盘报告。

---

## 📂 项目目录结构

```
yuntu-auto-strategy/
├── SKILL.md                          # AI Agent 技能入口定义文件
├── README.md                         # 快速入门与完整使用文档
├── .env.example                      # 环境变量配置模板（脱敏）
├── requirements.txt                  # Python 依赖清单
├── scripts/
│   └── yuntu_client.py               # 巨量云图 API 自动化客户端 (CLI & Module)
├── references/
│   ├── 5a_quant_thresholds.md        # 5A 底层判定量化规则表与流转诊断模型
│   ├── kol_150_eval_model.md         # 星图达人 150 分考核评分卡与爆文定律
│   ├── mind_top50_matrix.md          # 4L 价值体系 × 云图 TOP50 心智映射矩阵
│   └── audience_buy_personas.md      # 汽车新八大人群画像与车系矩阵
└── templates/
    └── feishu_canvas_templates.xml   # 5 大飞书原生矢量画板 XML 模板
```

---

## 🚀 快速开始

### 1. 安装依赖
```bash
git clone https://github.com/ninoou-bot/yuntu-auto-strategy.git
cd yuntu-auto-strategy
pip install -r requirements.txt
```

### 2. 配置环境变量
复制 `.env.example` 并重命名为 `.env`：
```bash
cp .env.example .env
```
在 `.env` 中填入你的巨量云图登录 Cookie 与账户 aadvid：
```ini
YUNTU_COOKIE="sessionid=your_cookie_here; ..."
YUNTU_AADVID="1637827271287884"
```

### 3. CLI 命令行调用
```bash
# 查询指定日期和车型的 5A 数据概览
python3 scripts/yuntu_client.py -d 2026-08-17 -t "向往M8"

# 输出结构化 JSON
python3 scripts/yuntu_client.py -d 2026-08-17 -t "向往S7" --json
```

---

## 🤖 在各大 AI Agent 中加载本技能

### 1. Google Antigravity
将本仓库克隆至 `~/.gemini/config/skills/yuntu_auto_strategy/` 或项目下的 `.agents/skills/yuntu_auto_strategy/`，Antigravity 将在对话中自动按需触发。

### 2. Claude Code / Amp / Roo Code
在项目根目录或全局配置中引入 `SKILL.md`，Agent 会自动阅读 SOP 并执行分析。

### 3. Cursor / Copilot
在 Prompt 中直接 `@SKILL.md` 即可调用全部 5A 分析方法论与脚本。

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。欢迎 PR 与交流！
