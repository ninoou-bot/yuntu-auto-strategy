# 🔑 巨量云图数据连接与鉴权配置指南 (Auth & Connect Guide)

> 本指南用于指导使用者如何在 1 分钟内从浏览器获取云图凭证，并配置或直接喂给 AI Agent（Antigravity、Claude Code、Cursor、Copilot 等），实现自动化抓取与 5A 心智分析。

---

## 一、 核心工作原理

巨量云图汽车版采用微前端 API 架构。你只需要在浏览器正常登录云图后台后，将**登录会话 Cookie** 与 **账户 aadvid** 提供给 AI，AI 即可通过内置的 API 客户端实现：
1. 秒级多线程抓取任意车型在抖音（cdy）与懂车帝（cdc）的双端 5A 资产数据；
2. 调取讨论热词与心智反射；
3. 执行卖点交叉检证并生成飞书画板报告。

---

## 二、 浏览器 3 步获取凭证 SOP (耗时约 30 秒)

> 推荐使用 Chrome、Edge 或 Safari 浏览器。

### 第一步：登录巨量云图后台
1. 打开浏览器，访问并登录 [巨量云图](https://yuntu.oceanengine.com)；
2. 切换到你的品牌/服务商账户，进入 **「汽车版 ➔ 人群资产 ➔ 5A人群资产」**（或任意 5A 概览页面）。

---

### 第二步：打开开发者工具 (F12)
1. 在页面任意位置按键盘 **`F12`**（Mac 用户按 **`Cmd + Option + I`**），或鼠标右键点击 **“检查 (Inspect)”**；
2. 点击顶部标签栏中的 **`Network`（网络）**；
3. 在下方的筛选栏选择 **`Fetch/XHR`**。

---

### 第三步：抓取 `aadvid` 与 `Cookie`
1. 刷新一下页面，或在页面上随意切换一下车型；
2. 在左侧请求列表中，找到以 **`audience_asset_profile`**（或任意包含 `yuntu_biz`）的接口请求并点击它；
3. **获取 `aadvid`**：
   * 查看右侧面板的 **`Headers` ➔ `Request URL`**；
   * 链接末尾形如 `...api/car/audience_asset_profile?aadvid=1637827271287884`；
   * 这一串数字（如 `1637827271287884`）即为你的 **`YUNTU_AADVID`**。
4. **获取 `YUNTU_COOKIE`**：
   * 在右侧面板向下滚动到 **`Request Headers`（请求标头）**；
   * 找到 **`cookie`** 这一行；
   * 鼠标右键点击该内容，选择 **“复制值 (Copy value)”** 即可。

```
[浏览器 F12 抓包示意]
Request URL: https://yuntu.oceanengine.com/yuntu_biz/api/car/audience_asset_profile?aadvid=1637827271287884  <── 这是 aadvid
Request Headers:
  accept: application/json...
  cookie: sessionid=xxxxxx; advertiser_id=xxxxxx; passport_csrf_token=xxxxxx; ...  <── 这是 Cookie
```

---

## 三、 喂给 AI Agent 的两种使用方式

### 方式 A：本地文件配置（最推荐·一次配置持续生效）
在你的项目或技能目录下创建 `.env` 文件（可直接复制 `.env.example` 并重命名）：

```ini
# 粘贴你刚复制的完整 Cookie
YUNTU_COOKIE="sessionid=你的sessionid; advertiser_id=你的adv_id; ..."

# 填入你抓到的 aadvid
YUNTU_AADVID="1637827271287884"

# 行业 ID (汽车行业固定为 10)
YUNTU_INDUSTRY_ID="10"
```

配置完成后，直接在对话框向 AI 发出指令即可：
> *“帮我拉取传祺向往 S7 上市近 30 天的 5A 资产，并根据我们输入的产品卖点体系做心智反射检证。”*

---

### 方式 B：直接在对话框喂给 AI Agent（零文件修改）
如果你不想创建 `.env` 文件，你可以直接将刚抓到的凭证作为 Context 发送给 AI：

> **你的输入 Prompt 示例**：
> ```markdown
> 我已经登录好巨量云图，这是我的连接凭证：
> Cookie: sessionid=xxxxxx; advertiser_id=xxxxxx; ...
> aadvid: 1637827271287884
> 
> 请帮我分析【传祺向往 S7】，主推卖点为：
> 1. 空间：2.9米大轴距、同级最大后备箱
> 2. 舒适：双阀SDC电磁悬架、全感官智能防晕车系统
> 3. 动力：全新插混系统、CLTC 248km纯电续航、电四驱
> 
> 请自动连接云图抓取数据，执行卖点 vs 真实心智反射交叉检证，并输出飞书画板报告。
> ```

AI Agent 会自动加载凭证、调用内置客户端完成抓取并交付结构化报告！

---

## 四、 常见问题与排查 (FAQ)

1. **Q：Cookie 的有效期是多久？**  
   * **A**：通常浏览器的登录 Cookie 有效期为 **15 ~ 30 天**。如果超过期限，AI 提示 `API Error` 或鉴权失效，只需重新按上述 3 步复制一次最新的 Cookie 替换即可。
2. **Q：为什么抓取不到数据或提示 status != 0？**  
   * **A**：请检查你的云图账号是否有该品牌的查看权限，或者确认传入的 `date` 是否在当前日期的 90 天数据回溯范围内。
3. **Q：安全性保障？**  
   * **A**：请勿将包含真实 Cookie 的 `.env` 文件提交到 GitHub 等公共代码仓库。本 Skill 代码已配置 `.gitignore` 保护。
