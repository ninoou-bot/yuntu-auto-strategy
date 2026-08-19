---
name: yuntu_auto_strategy
description: 巨量云图汽车版全域策略与卖点心智检证通用技能（Yuntu Auto Strategy & Mind Validation Universal Skill）。支持输入任意车型的产品卖点价值体系，自动调取云图 5A 与 TOP50 真实心智反射数据，进行五维交叉验证（强占领/突围攀升/盲点哑炮/口碑风险/自发破圈），并输出达人 150 分考核与飞书原生画板复盘报告。适用于 Antigravity, Claude Code, Cursor, Copilot, Roo Code 等各类 AI Agent。
---

# 巨量云图汽车版全域策略与卖点心智检证专家 (yuntu_auto_strategy)

> **定位**：全车型通用的**「产品卖点体系输入 ➔ 云图数据自动调取 ➔ 真实心智反射交叉检证 ➔ 策略修正与画板输出」**作战中枢。  
> 兼容 **Antigravity、Claude Code、Cursor、GitHub Copilot、Roo Code** 等各类主流 AI Agent。

---

## 一、 核心功能与交互模式 (Core Workflows)

### 🌟 核心模式：【产品卖点体系 vs 云图心智反射交叉检证 SOP】
这是本技能最核心的通用分析工作流。用户只需输入**任意车型**及其**规划的主推卖点价值体系**，AI 自动完成数据提取与五维交叉检证：

```
┌────────────────────────────────────────────────────────────────────────┐
│ 【输入端】用户输入：车型名称 + 自定义卖点价值体系 (3S/4L/5大维度/清单) │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 【数据端】AI 调取：云图 5A 漏斗 + TOP50 讨论心智词 + 排名升降 + 美誉度  │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 【检证端】五维矩阵：🌟强占领区 / 📈突围区 / ⚠️盲点哑炮 / 🚨风险区 / 💡自发区│
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 【交付端】输出：卖点有效性体检表 + 预算加码/止损建议 + 飞书原生画板报告 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 二、 四阶段标准化作业 SOP (Execution SOP)

### 阶段一：API 自动化调数（秒级数据提取）
1. 读取 `.env` 或环境变量中的 `YUNTU_COOKIE` 与 `YUNTU_AADVID`。
2. 运行脚本 `python3 scripts/yuntu_client.py -d YYYY-MM-DD -t 车型名称` 或实例化 `YuntuAutoClient`。
3. 调取指定日期或多节点时间序列数据（获取抖音 `douyin_cdy` 与 懂车帝 `dongchedi_cdc` 双端 5A 资产）。

### 阶段二：5A 资产与触点流转系数诊断
1. **量化阈值对齐**：查阅 `references/5a_quant_thresholds.md`，对标曝光/点击/播放时长/看后搜底层判定规则。
2. **流转效率测算**：
   $$\text{流转系数} = \frac{\text{A1 人数} + \text{A2 人数}}{\text{A3 人数}}$$
   * 对标行业 TOP20 均值（**8.6**），判断当前是“A1 开口不足”还是“A2 弱相关充斥、未激发 A3 种草”。
3. **双端流转协同分析**：分析抖音端（广域 A3 种草蓄水）向懂车帝端（垂直 A4 留资转化）的流转递增效应。

### 阶段三：卖点体系 vs 云图真实心智反射交叉检证
查阅 `references/selling_points_validation_sop.md`，将用户输入的各项主推卖点，与云图 TOP50 讨论词进行交叉比对，归入五大象限：
1. **🌟 强占领区 (Validated)**：官方主推 + 稳居 TOP 1~10 + 美誉度 ≥20% ➔ **保持第一沟通锚点**；
2. **📈 突围攀升区 (Rising)**：官方主推 + 新进榜 (New) 或排名上升 ≥10 ➔ **追加种草通与达人投流**；
3. **⚠️ 心智盲点区 (Blindspots)**：官方主推但 **未进 TOP50** ➔ **判定为低效/自嗨卖点，立即止损或重构场景化话术**；
4. **🚨 口碑风险区 (Risk)**：进入 TOP50 但美誉度 ≤0% ➔ **安排硬核测评打消三电/续航/质量顾虑**；
5. **💡 自发破圈区 (Unprompted)**：官方未主推但用户自发讨论冲进 TOP30 ➔ **反哺纳入官方后续宣发**。

### 阶段四：星图达人 150 分考核与飞书画板交付
1. **星图达人考核**：查阅 `references/kol_150_eval_model.md`，执行 150 分模型考核与爆文四象限加热建议。
2. **飞书画板生成**：引用 `templates/feishu_canvas_templates.xml`，采用绝对物理坐标构建包含 5 大矢量画板的飞书文档并更新交付。

---

## 三、 知识模块索引

* 🌟 卖点 vs 心智反射验证 SOP：[`references/selling_points_validation_sop.md`](references/selling_points_validation_sop.md)
* 📊 5A 触点判定底层规则与流转系数：[`references/5a_quant_thresholds.md`](references/5a_quant_thresholds.md)
* ⭐ 星图达人 150 分加权考核模型：[`references/kol_150_eval_model.md`](references/kol_150_eval_model.md)
* 👥 汽车新八大人群 BUY 策略矩阵：[`references/audience_buy_personas.md`](references/audience_buy_personas.md)
* 🎨 飞书原生矢量画板 XML 模板库：[`templates/feishu_canvas_templates.xml`](templates/feishu_canvas_templates.xml)
* 🚀 Python API 客户端：[`scripts/yuntu_client.py`](scripts/yuntu_client.py)
