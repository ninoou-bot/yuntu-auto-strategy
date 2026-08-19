# -*- coding: utf-8 -*-
"""
巨量云图自动化心跳保活与智能补偿脚本 (Yuntu Heartbeat & Auto-Sliding Session)
- 核心功能：定期或唤醒后向云图发送轻量请求，刷新 SSO 登录态，并将新的 Set-Cookie 自动回写至 .env
- 补偿机制：若错过预定时间（电脑关机/休眠），开机或下次触发时自动检测并立即执行补偿保活
"""

import os
import sys
import json
import time
import datetime
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(BASE_DIR)
ENV_PATH = os.path.join(SKILL_DIR, ".env")
PROJECT_ROOT = os.path.abspath(os.path.join(SKILL_DIR, "../../.."))
PROJECT_ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
STATE_FILE = os.path.join(SKILL_DIR, ".heartbeat_state.json")

def load_env(env_path):
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip().strip("'").strip('"')
    return env_vars

def save_env(env_path, env_vars):
    lines = []
    lines.append("# 巨量云图汽车版 API 鉴权配置 (自动保活同步)")
    for k, v in env_vars.items():
        lines.append(f'{k}="{v}"')
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def update_cookie_str(old_cookie_str, new_cookie_dict):
    """将新返回的 Cookie 键值对增量合并到旧 Cookie 字符串中"""
    if not old_cookie_str:
        return "; ".join([f"{k}={v}" for k, v in new_cookie_dict.items()])
    
    cookies = {}
    for part in old_cookie_str.split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            cookies[k.strip()] = v.strip()
            
    cookies.update(new_cookie_dict)
    return "; ".join([f"{k}={v}" for k, v in cookies.items()])

def run_heartbeat(force=False):
    now = datetime.datetime.now()
    now_ts = int(now.timestamp())
    
    # 读取上次保活状态
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {}

    last_run_ts = state.get("last_success_ts", 0)
    days_since_last = (now_ts - last_run_ts) / 86400.0 if last_run_ts > 0 else 999.0

    # 如果非强制，且距离上次成功不足 5 天，则无需频繁重复
    if not force and days_since_last < 5.0 and last_run_ts > 0:
        return {
            "status": "skipped",
            "message": f"距离上次保活仅 {days_since_last:.1f} 天，会话状态健康 (上次: {state.get('last_success_date')})",
            "last_success": state.get("last_success_date")
        }

    # 加载当前凭证
    env_vars = load_env(ENV_PATH)
    if not env_vars.get("YUNTU_COOKIE") and os.path.exists(PROJECT_ENV_PATH):
        env_vars = load_env(PROJECT_ENV_PATH)

    cookie = env_vars.get("YUNTU_COOKIE", "")
    aadvid = env_vars.get("YUNTU_AADVID", "1637827271287884")

    if not cookie:
        return {"status": "error", "message": "未找到 YUNTU_COOKIE，无法执行保活"}

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'referer': f'https://yuntu.oceanengine.com/yuntu_brand/car/assets/crowd/distribution?aadvid={aadvid}',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'cookie': cookie
    }

    url = f'https://yuntu.oceanengine.com/yuntu_biz/api/car/audience_asset_profile?aadvid={aadvid}'
    probe_date = (now - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    body = {
        'brand_id': 7360,
        'industry_id': 10,
        'date': probe_date
    }
    
    try:
        resp = requests.post(url, headers=headers, json=body, timeout=12)
        res = resp.json()
        
        if res.get("status") == 0:
            # 捕获服务端新设置的 Cookies
            new_cookies = resp.cookies.get_dict()
            if new_cookies:
                updated_cookie_str = update_cookie_str(cookie, new_cookies)
                env_vars["YUNTU_COOKIE"] = updated_cookie_str
                save_env(ENV_PATH, env_vars)
                if os.path.exists(PROJECT_ENV_PATH):
                    save_env(PROJECT_ENV_PATH, env_vars)

            # 更新成功状态
            state["last_success_ts"] = now_ts
            state["last_success_date"] = now.strftime("%Y-%m-%d %H:%M:%S")
            state["probe_result"] = "ok"
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

            return {
                "status": "success",
                "message": "云图会话心跳保活成功，登录态已自动顺延！",
                "last_success": state["last_success_date"],
                "days_since_previous": f"{days_since_last:.1f}d"
            }
        else:
            return {
                "status": "auth_expired",
                "message": f"云图登录态已失效 (status={res.get('status')})，请重新登录获取 Cookie",
                "raw": res
            }
    except Exception as e:
        return {"status": "network_error", "message": f"网络探测失败: {str(e)}"}

if __name__ == '__main__':
    force_mode = "--force" in sys.argv or "-f" in sys.argv
    result = run_heartbeat(force=force_mode)
    print(json.dumps(result, indent=2, ensure_ascii=False))
