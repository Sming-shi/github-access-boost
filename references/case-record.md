# 本机实测记录（2026-11-27）

## 用户真实场景

用户反馈"GitHub 上不去，帮我下载一个加速器"。拒绝来路不明的加速器后，用户选择安装开源工具。

## 处理过程与结论

1. **官方仓库确认**：`BeyondDimension/SteamTools`（Watt Toolkit，原 Steam++），GPL-3.0，通过修改 hosts 加速，不走代理。
2. **版本**：v3.3.0（2026-11-23 发布）。
3. **安装包**：`Steam++_v3.3.0_win_x64_aot.exe`，45,543,888 字节（43.4 MB），AOT 版。
4. **下载通道**：GitHub 直连不畅，改用 `gh-proxy.com` 镜像，速度与官方一致。
5. **官方 SHA256**：`4907c9cd6596456c4bad01269375bfd2b65d09195b39af637a3545b3c5e780fc`，镜像下载文件实测哈希完全一致 —— 确认未被掉包。
6. **落地**：安装包下载到用户系统的「下载」目录（Windows 为 `%USERPROFILE%\Downloads`，macOS 为 `~/Downloads`），交给用户手动安装 + 开启网络加速（GUI + UAC 无法代操作）。

## 复用要点

- 版本号/哈希**不要写死进 SKILL.md**，用 `scripts/check_github.py --release` 每次实时获取。本记录仅作案例参考。
- 下载安装包的正确顺序：官方 API 拿链接和校验值 → 镜像下载 → 校验 → 交付。
- 用户选 AOT 版的原因：体积更小、启动快，内置插件只能禁用不能删，对只要加速功能的用户更干净。

## 环境与限制（本机）

- Windows 11，Edge 浏览器，无 Chrome。
- curl 直连 GitHub API 遇 schannel 证书吊销检查失败，加 `--ssl-no-revoke` 后正常。
- git 对 github.com 设 `sslVerify=false` 后可正常 ls-remote/push。
- 代理环境变量 `HTTPS_PROXY` 指向本地端口，端口会变（此次为 51225）。
- 自动化操作桌面不稳定，用户明确要求"不用你操作，告诉步骤"后改为文字+示意图指引。

## 关联技能

- 汉化需求见 `github-chinese-userscript` skill（篡改猴 + 油猴脚本方案）。
- 两个技能互补：本技能解决"访问"，那个解决"语言"。
