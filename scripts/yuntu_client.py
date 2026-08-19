# -*- coding: utf-8 -*-
"""
巨量云图汽车版 5A 数据自动化客户端 (Yuntu Auto Strategy Client - Universal Version)
- 支持环境变量配置 (YUNTU_COOKIE, YUNTU_AADVID) 或 .env 文件
- 支持任意汽车品牌与车系 Series ID 枚举与多线程数据提取
- 完全脱敏，安全无任何硬编码 Token
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Optional, Union
from concurrent.futures import ThreadPoolExecutor

try:
    import requests
except ImportError:
    print("Error: 'requests' module not found. Run 'pip install requests' to install.", file=sys.stderr)
    sys.exit(1)


def load_env_file(dotenv_path: str = ".env"):
    """轻量级读取 .env 文件，免第三方依赖"""
    if os.path.exists(dotenv_path):
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'").strip('"')
                if k not in os.environ:
                    os.environ[k] = v


class YuntuAutoClient:
    """巨量云图汽车版 5A API 客户端"""

    # 预设常见车系 Series ID 映射（可动态扩展）
    DEFAULT_SERIES_MAP = {
        "传祺全品牌": 7360,
        "广汽传祺": 7360,
        "传祺M8": 10115069,
        "传祺向往M8": 11873835,
        "M8 PHEV L": 11873835,
        "向往M8": 11873835,
        "传祺E8": 11824923,
        "传祺E8 PHEV": 11575515,
        "E8 PHEV": 11575515,
        "传祺向往S7": 11906241,
        "向往S7": 11906241,
        "传祺GS8": 11716,
        "GS8": 11716,
        "传祺GS4": 11714,
        "传祺GS4 PLUS": 10752997,
        "传祺GS4 MAX": 11714,
        "传祺GS3": 11712,
        "GS3影速": 11712,
        "传祺越7": 12328761,
        "越7": 12328761,
        "传祺M6": 10077860,
        "M6": 10077860,
        "影豹": 10565814,
        "传祺ES9 PHEV": 11575518,
        "传祺E9 PHEV": 11471417,
        "传祺向往S9": 12035051
    }

    def __init__(self, cookie: Optional[str] = None, aadvid: Optional[Union[str, int]] = None, custom_series_map: Optional[Dict[str, int]] = None):
        # 尝试加载当前目录或父目录下的 .env
        load_env_file()
        load_env_file(os.path.join(os.path.dirname(__file__), "..", ".env"))

        self.cookie = cookie or os.environ.get("YUNTU_COOKIE", "")
        self.aadvid = aadvid or os.environ.get("YUNTU_AADVID", "")
        self.brand_id = int(os.environ.get("YUNTU_DEFAULT_BRAND_ID", "7360"))
        self.industry_id = int(os.environ.get("YUNTU_INDUSTRY_ID", "10"))  # 10 代表汽车行业

        self.series_map = self.DEFAULT_SERIES_MAP.copy()
        if custom_series_map:
            self.series_map.update(custom_series_map)

        if not self.cookie:
            print("⚠️ 警告：未检测到 YUNTU_COOKIE。请通过环境变量、.env 文件或构造参数提供登录 Cookie。", file=sys.stderr)

    @property
    def headers(self) -> Dict[str, str]:
        return {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'referer': f'https://yuntu.oceanengine.com/yuntu_brand/car/assets/crowd/distribution?aadvid={self.aadvid}',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
            'cookie': self.cookie
        }

    def resolve_brand_id(self, target: Union[str, int]) -> int:
        """根据名称或数字解析对应 Brand/Series ID"""
        if isinstance(target, int):
            return target
        if target.isdigit():
            return int(target)
        if target in self.series_map:
            return self.series_map[target]
        for k, v in self.series_map.items():
            if target.lower() in k.lower() or k.lower() in target.lower():
                return v
        return self.brand_id

    def get_5a_profile(self, date_str: str, target: Union[str, int] = 7360) -> Dict:
        """拉取指定车型在指定日期的 5A 人群数据快照（双端）"""
        if not self.cookie:
            return {"error": "Missing YUNTU_COOKIE", "status": -1}

        brand_id = self.resolve_brand_id(target)
        url = f'https://yuntu.oceanengine.com/yuntu_biz/api/car/audience_asset_profile?aadvid={self.aadvid}'
        body = {
            'brand_id': brand_id,
            'industry_id': self.industry_id,
            'date': date_str
        }
        try:
            resp = requests.post(url, headers=self.headers, json=body, timeout=15)
            res = resp.json()
            if res.get("status") != 0:
                return {"error": res.get("msg", "API Error"), "status": res.get("status")}
            
            data = res.get("data", {})
            cdy = {int(x["audience_asset_ax_type"]): int(x.get("cover_num", 0)) for x in data.get("cdy", [])}
            cdc = {int(x["audience_asset_ax_type"]): int(x.get("cover_num", 0)) for x in data.get("cdc", [])}
            
            return {
                "status": 0,
                "date": date_str,
                "target": str(target),
                "brand_id": brand_id,
                "douyin_cdy": {
                    "total_5a": cdy.get(0, 0),
                    "a1_aware": cdy.get(1, 0),
                    "a2_appeal": cdy.get(2, 0),
                    "a3_ask": cdy.get(3, 0),
                    "a4_act": cdy.get(4, 0),
                    "a5_advocate": cdy.get(5, 0)
                },
                "dongchedi_cdc": {
                    "total_5a": cdc.get(0, 0),
                    "a1_aware": cdc.get(1, 0),
                    "a2_appeal": cdc.get(2, 0),
                    "a3_ask": cdc.get(3, 0),
                    "a4_act": cdc.get(4, 0),
                    "a5_advocate": cdc.get(5, 0)
                }
            }
        except Exception as e:
            return {"error": str(e), "status": -1}

    def get_time_series(self, target: Union[str, int], dates: List[str], max_workers: int = 5) -> Dict[str, Dict]:
        """并发拉取多时间节点的时间序列数据"""
        results = {}
        def _fetch(d):
            return d, self.get_5a_profile(d, target)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for d, data in executor.map(_fetch, dates):
                results[d] = data
        return dict(sorted(results.items()))


def main():
    parser = argparse.ArgumentParser(description="巨量云图 5A 数据自动化拉取工具")
    parser.add_argument("--date", "-d", type=str, required=True, help="查询日期 (格式: YYYY-MM-DD)")
    parser.add_argument("--target", "-t", type=str, default="7360", help="车型名称或 Series ID (如: 向往M8, S7, GS8)")
    parser.add_argument("--json", action="store_true", help="以格式化 JSON 输出")
    args = parser.parse_args()

    client = YuntuAutoClient()
    res = client.get_5a_profile(args.date, args.target)
    
    if args.json or "error" in res:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        cdy = res.get("douyin_cdy", {})
        cdc = res.get("dongchedi_cdc", {})
        print(f"[{res.get('date')}] {args.target} (ID: {res.get('brand_id')}) 5A 人群资产概览：")
        print(f"  • 抖音生态 (cdy)：5A={cdy.get('total_5a'):,} | A1={cdy.get('a1_aware'):,} | A2={cdy.get('a2_appeal'):,} | A3={cdy.get('a3_ask'):,} | A4={cdy.get('a4_act'):,} | A5={cdy.get('a5_advocate'):,}")
        print(f"  • 懂车帝 (cdc)  ：5A={cdc.get('total_5a'):,} | A1={cdc.get('a1_aware'):,} | A2={cdc.get('a2_appeal'):,} | A3={cdc.get('a3_ask'):,} | A4={cdc.get('a4_act'):,} | A5={cdc.get('a5_advocate'):,}")


if __name__ == '__main__':
    main()
