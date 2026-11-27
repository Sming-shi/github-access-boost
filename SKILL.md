---
name: github-access-boost
description: 解决 GitHub 打不开、访问慢、登录失败、git clone 卡住等网络访问问题，并按需提供安全的高速下载方式。先诊断根因（DNS 污染 / 连接超时 / 证书问题 / 只是需要下载 Release 文件），再选择最轻量的解法：gh-proxy 镜像直下、Watt Toolkit（原 Steam++）改 hosts 加速、或修复本机 git/curl 配置。当用户提出"GitHub 上不去/打不开/登不进去/很慢""帮我下载一个加速器""git clone 超时""下载 GitHub Release 文件慢"等需求时使用本技能。适用于 Windows / macOS / Linux，重点覆盖国内网络环境。
agent_created: true
---

# GitHub 访问加速（诊断优先，安全兜底）

## Overview

让 GitHub 网页、git clone、Release 下载恢复正常。核心原则：**先诊断、后开药；能不用加速器就不用；任何下载都必须校验来源与哈希**。

避免两个常见错误：

1. 用户一说"GitHub 上不去"就直接去网上抓一个来路不明的"加速器"——这类软件很多是 VPN 或带捆绑，有安全和合规风险。
2. 一概推荐装软件——如果只是要下载某个 Release 文件，用镜像前缀即可，无需安装任何东西。

代码、README、评论内容不在本技能处理范围内（那是"汉化"技能的事）。

## When to use

- 用户说 GitHub 打不开、很慢、登录不了、转圈、超时
- 用户要求"下载一个加速器""GitHub 加速"
- `git clone` / `git push` 卡住或超时
- 下载 GitHub Release / raw 文件速度慢

## 关键原则：先判断场景，再动手

按用户真实需求选择起点，不要一上来就下载安装器：

| 用户诉求 | 处理方式 |
|---|---|
| 只是下载某个 Release / 仓库文件 | 直接走镜像前缀（Step 2A），免安装 |
| 网页打不开、登录不了、全站慢 | 诊断后走 Watt Toolkit hosts 加速（Step 2B） |
| git clone/push 卡住但网页能开 | 优先修 git 配置（见 `references/troubleshooting.md` 的 SSL 一节），不必装加速器 |
| 明确要"加速器"软件 | 走 Step 2B，只选开源、改 hosts 的 Watt Toolkit |
| 用户不懂技术、一步步要引导 | 只输出可照做的分步文字 + 示意图，不做桌面自动化 |

## Workflow

### Step 1：诊断（2 分钟，先做）

用 `scripts/check_github.py` 一次性测多个端点，判断卡在哪一层：

```bash
python scripts/check_github.py
```

输出区分：DNS 解析失败、TCP 连接超时、TLS/证书错误、HTTP 状态码异常。据此选择：

- 只是 Release 下载慢 → 跳到 Step 2A
- 网页/全站不通、DNS 被污染 → 走 Step 2B（Watt Toolkit 改 hosts）
- TLS/证书报错（常见于 Windows schannel）→ 先按 `references/troubleshooting.md` 修本机配置
- 完全无网络 → 上述都无效，先解决基础网络

### Step 2A：镜像直下（免安装，优先）

适用于"下载文件"类需求。把 GitHub 下载链接前面加镜像前缀：

```
https://gh-proxy.com/https://github.com/<owner>/<repo>/releases/download/<tag>/<file>
```

- 其他可用镜像见 `references/mirrors.md`，主镜像不通时轮换。
- 下载后**必须校验**：从 GitHub API 取官方 SHA256，与本地 `sha256sum` 比对，确认镜像没掉包。
- 涉及安装包、可执行文件时，校验是强制步骤，不可省略。

### Step 2B：Watt Toolkit 加速器（需要装软件时）

只在确认需要全站加速时使用。Watt Toolkit（原 Steam++，GPL-3.0 开源，开发者 BeyondDimension）通过**修改 hosts** 加速，**不走代理、不捆绑、不劫持流量**。

1. **拿官方最新信息与校验值**（不要写死版本号，每次实时取）：

   ```bash
   python scripts/check_github.py --release
   ```

   该命令读取官方仓库 `BeyondDimension/SteamTools` 的最新 release，输出 Windows x64 安装包文件名、下载链接、官方 SHA256。

2. **通过镜像下载**安装包到用户下载目录（GitHub 直连不畅时）：

   ```bash
   curl -L --fail --retry 3 -o "<下载路径>/<文件名>" "<镜像前缀><官方下载链接>"
   ```

3. **校验 SHA256**，与第 1 步官方值比对。不一致就删除文件、换镜像重下，绝不安装未校验的安装包。

4. **交付给用户安装**：安装包需要图形界面 + UAC 授权，交给用户手动操作，不要尝试桌面自动化。给出清晰步骤：
   - 双击安装 → 打开 Watt Toolkit → 左侧「网络加速」
   - 勾选 GitHub 相关项（github.com、raw.githubusercontent.com 等）→ 点「一键加速」
   - 首次会请求管理员权限，允许即可

5. **收尾说明**：加速后若 DNS 未刷新，执行 `ipconfig /flushdns`；在软件里「还原 hosts」再重新加速也可。选 AOT 版更干净（体积更小，内置插件只能禁用）。

### Step 3：验证

- 网页类：让用户打开 github.com 确认能加载/登录
- 下载类：确认文件校验通过、能正常打开
- git 类：让用户执行 `git ls-remote https://github.com/<owner>/<repo>.git HEAD` 确认

## 安全底线（强制）

- **只从官方仓库 / 官方渠道下载**：Watt Toolkit 官方仓库是 `BeyondDimension/SteamTools`；不要下载第三方改包、汉化包、"绿色版"。
- **不走代理类"加速器"**：用户要的是解决 GitHub 访问，不是全局翻墙。优先 hosts 方案；若某软件要求开启系统代理或导入证书，先停下询问用户。
- **强制 SHA256 校验**：凡下载可执行文件，必须用官方值校验。
- **不碰系统敏感配置**：改 hosts 通过 Watt Toolkit 完成；不要自行写 hosts、改注册表、装证书，除非用户明确授权。

## 环境与操作约束

- Windows 上 curl 直连 GitHub API 常遇 `schannel` 证书吊销检查失败（`CRYPT_E_NO_REVOCATION_CHECK`）：curl 加 `--ssl-no-revoke`；git 可对域名设 `http.https://github.com/.sslVerify=false`。详见 `references/troubleshooting.md`。
- 部分 Windows 环境 `reg.exe`、PowerShell `Add-Type` 被安全策略禁用；优先用 Python 标准库 / 官方工具。
- 自动化操作浏览器界面（截图、点击）常因窗口焦点、DPI 缩放失败。用户说"不懂"或"不用你操作"时，直接给分步文字指引 + 示意图，不折腾桌面自动化。
- 交付安装包后提醒用户：Watt Toolkit 是开源工具，GitHub 打不开时也可用其官网/微软商店渠道获取。

## References

- `references/mirrors.md`：可用镜像源清单、前缀用法、轮换策略
- `references/troubleshooting.md`：DNS / 证书 / git 配置等分类排查
- `references/case-record.md`：本机实测记录（版本、哈希、环境限制）
- `scripts/check_github.py`：一键诊断端点 + 查询官方最新 release 与校验值
