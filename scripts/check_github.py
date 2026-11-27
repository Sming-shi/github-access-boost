#!/usr/bin/env python3
"""GitHub 访问诊断 + 官方最新 release 查询。

用法:
    python check_github.py            # 诊断各端点连通性
    python check_github.py --release  # 查询 Watt Toolkit 官方最新 Windows 安装包与 SHA256
    python check_github.py --verify <文件> <期望SHA256>  # 校验本地文件哈希

仅用 Python 标准库，Windows/macOS/Linux 均可运行。
"""
import sys
import ssl
import json
import socket
import hashlib
import urllib.request
import urllib.error

ENDPOINTS = [
    ("github.com 网页", "https://github.com/"),
    ("GitHub API", "https://api.github.com/"),
    ("raw 文件", "https://raw.githubusercontent.com/"),
    ("codeload 压缩包", "https://codeload.github.com/"),
]

REPO_API = "https://api.github.com/repos/BeyondDimension/SteamTools/releases/latest"


def _opener():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # 绕开 Windows schannel 吊销检查问题
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))


def diagnose():
    print("=== GitHub 端点诊断 ===")
    try:
        ip = socket.gethostbyname("github.com")
        print(f"DNS 解析 github.com -> {ip}")
    except Exception as e:
        print(f"DNS 解析失败: {e}")

    opener = _opener()
    for name, url in ENDPOINTS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "github-access-boost"})
            with opener.open(req, timeout=12) as r:
                print(f"[OK]   {name}: HTTP {r.status}")
        except urllib.error.HTTPError as e:
            print(f"[HTTP] {name}: {e.code} {e.reason}")
        except urllib.error.URLError as e:
            print(f"[FAIL] {name}: {e.reason}")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")


def latest_release():
    print("=== Watt Toolkit 官方最新 release ===")
    opener = _opener()
    try:
        req = urllib.request.Request(REPO_API, headers={"User-Agent": "github-access-boost"})
        with opener.open(req, timeout=20) as r:
            data = json.load(r)
    except Exception as e:
        print(f"查询失败: {e}")
        return
    print(f"版本: {data.get('tag_name')}  发布: {data.get('published_at')}")
    print(f"官方页: {data.get('html_url')}")
    print("Windows 安装包:")
    for a in data.get("assets", []):
        n = a.get("name", "")
        if n.lower().endswith(".exe") and ("x64" in n.lower() or "win" in n.lower()):
            print(f"  名称: {n}")
            print(f"  大小: {a.get('size')} bytes")
            print(f"  链接: {a.get('browser_download_url')}")
            print(f"  SHA256(API): {a.get('digest', '(API 未提供 digest)')}")
            print(f"  镜像: https://gh-proxy.com/{a.get('browser_download_url')}")
            print()
    print("提示: 若 API 的 digest 字段为空，用 --verify 对下载文件算哈希后人工比对官方 release 页面公布的校验值。")


def verify(path, expected):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    actual = h.hexdigest()
    want = expected.strip().lower().replace("sha256:", "")
    print(f"实际: {actual}")
    print(f"期望: {want}")
    print("结果: " + ("一致 OK" if actual == want else "不一致 —— 删除文件，换镜像重下"))


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--verify":
        verify(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 2 and sys.argv[1] == "--release":
        latest_release()
    else:
        diagnose()
