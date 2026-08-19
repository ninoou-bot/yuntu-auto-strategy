---
name: yuntu_auto_strategy
description: 巨量云图汽车版全域策略与人群资产诊断通用技能（Yuntu Auto Strategy Universal Skill）。支持所有主流 AI Agent（Antigravity, Claude Code, Cursor, Copilot, Roo Code）。提供 5A 数据自动化调取、触点流转系数诊断、星图达人 150 分加权考核、4L 价值体系 × TOP50 心智排名矩阵以及飞书原生画板高质感复盘报告生成。
---

# 巨量云图汽车版全域策略与资产诊断专家 (yuntu_auto_strategy)

> **定位**：本技能为汽车品牌数字营销专案的**巨量云图（OceanEngine Yuntu）高阶作战中枢**。  
> 兼容 **Antigravity、Claude Code、Cursor、GitHub Copilot、Roo Code** 等各类主流 AI Agent。

---

## 一、 技能触发与调度场景 (Triggers & Workflows)

当用户提出以下任一诉求时，自动激活本技能：
1. **车系 5A 资产诊断与走势拉取**：如“拉一下 M8 / S7 / E8 / GS8 近三个月的 5A 走势”、“分析当前 5A 流转瓶颈”。
2. **战役/节点营销复盘**：如“复盘新车上市前后云图 5A 表现”、“复盘星图达人投放效果”。
3. **星图达人优选与效果考核**：如“用 150 分模型考核这批车评达人”、“评估哪些是双爆文/质爆文”。
4. **品牌心智度量与卖点攻防**：如“分析插混/大空间在云图 TOP50 心智词的排名升降”。
5. **汽车新八大人群定位与内容规划**：如“针对生活精算师/温馨生活家制定 Q4 种草打法”。
6. **飞书全景画板复盘文档生成**：自动生成包含 5 大原生矢量画板（`<whiteboard>`）的高阶飞书云文档。

---

## 二、 四阶段标准化作业 SOP (Execution SOP)

```
[阶段一：API 自动化调数] ──➔ [阶段二：5A与流转系数诊断] ──➔ [阶段三：心智&达人150分考核] ──➔ [阶段四：飞书全景画板交付]
```

### 阶段一：API 自动化调数（秒级数据提取）
1. 确保 `.env` 或环境变量中已配置 `YUNTU_COOKIE` 与 `YUNTU_AADVID`。
2. 运行内置脚本 `python3 scripts/yuntu_client.py -d YYYY-MM-DD -t 车型名称` 或在代码中实例化 `YuntuAutoClient`。
3. 调取指定日期或多节点时间序列数据（同时获取抖音 `douyin_cdy` 与 懂车帝 `dongchedi_cdc` 双端 5A 分布）。

### 阶段二：5A 资产与触点流转系数诊断
1. **量化阈值对齐**：查阅 `references/5a_quant_thresholds.md`，对标曝光/点击/播放时长/看后搜底层判定规则。
2. **流转效率测算**：
   $$\text{流转系数} = \frac{\text{A1 人数} + \text{A2 人数}}{\text{A3 人数}}$$
   * 对标行业 TOP20 均值（**8.6**），判断当前是“A1 开口不足”还是“A2 弱相关充斥、未激发 A3 种草”。
3. **双端流转协同分析**：分析抖音端（广域 A3 种草蓄水）向懂车帝端（垂直 A4 留资转化）的流转递增效应。

### 阶段三：品牌心智 TOP50 映射与达人 150 分考核
1. **4L 价值体系映射**：查阅 `references/mind_top50_matrix.md`，将车系卖点与云图 TOP50 心智词排名升降及美誉度对比，排查未破圈盲点。
2. **星图达人分层与 150 分考核**：查阅 `references/kol_150_eval_model.md`，对标基础流量（100分）、完播率（10分）、看后搜（20分）、A3新增（20分）。
3. **爆文归因与话术定律**：
   * 判定双爆文（18% 全量投流）、质爆文（32% 品专承接）、量爆文（26% 混剪复用）；
   * 严格遵循“贴合生活场景 + 通俗化技术语言解读 ➔ 爆文率 100%”准则。

### 阶段四：飞书原生画板文档生成与双库同步
1. 引用 `templates/feishu_canvas_templates.xml` 中的 5 大原生画板模板，构建 XML 内容。
2. **必须使用绝对物理坐标**（严禁 `<g transform="...">` 相对嵌套），彻底防止文字重叠与空白卡片。
3. 执行 `lark-cli docs +create`（或在已有文档上 `+update --command overwrite`）生成在线云文档。

---

## 三、 知识模块索引

* 5A 触点判定底层规则：[`references/5a_quant_thresholds.md`](references/5a_quant_thresholds.md)
* 星图达人 150 分加权考核：[`references/kol_150_eval_model.md`](references/kol_150_eval_model.md)
* 4L 价值体系与心智映射：[`references/mind_top50_matrix.md`](references/mind_top50_matrix.md)
* 汽车新八大人群矩阵：[`references/audience_buy_personas.md`](references/audience_buy_personas.md)
* 飞书画板 XML 模板库：[`templates/feishu_canvas_templates.xml`](templates/feishu_canvas_templates.xml)
* Python API 客户端：[`scripts/yuntu_client.py`](scripts/yuntu_client.py)
