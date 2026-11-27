# 分类排查手册

## 一、诊断脚本输出怎么看

`python scripts/check_github.py` 逐个测 github.com / api.github.com / raw / codeload：

- **全部 `[OK]`**：网络没大问题。用户说的"打不开"可能是登录态、浏览器缓存或某个具体页面。先让用户给出报错截图。
- **DNS 解析失败或解析到明显异常 IP**：DNS 污染。走 Watt Toolkit hosts 加速。
- **`[HTTP] 403/404` 但能连上**：端点本身问题，`api.github.com/` 根路径返回 404 属正常（不是故障）。
- **大量 `[FAIL] 超时`**：连接层被阻断，走 hosts 加速或镜像。
- **`[FAIL] certificate verify failed`**：证书问题，看下一节。

## 二、Windows 证书 / schannel 问题（高频）

现象：curl 访问 `https://api.github.com` 直接失败，退出码 35，报：

```
schannel: next InitializeSecurityContext failed: CRYPT_E_NO_REVOCATION_CHECK
```

原因：Windows 证书吊销检查无法完成（常见于代理环境/企业网络）。

解决：

```bash
# curl 单次绕过
curl --ssl-no-revoke -I https://api.github.com

# git 永久绕过（只针对 github.com，不影响其他站点）
git config --global http.https://github.com/.sslVerify false
git config --global http.https://api.github.com/.sslVerify false
```

注意：`http.schannelCheckRevoke false` 在部分 git 版本上**不生效**，实测按域名设 `sslVerify=false` 才可靠。

## 三、git clone / push 卡住

1. 先测 `git ls-remote https://github.com/owner/repo.git HEAD`——能返回 commit 号说明 git 通道正常。
2. 超时：按第二节修 SSL；仍不行用镜像 clone：`git clone https://gh-proxy.com/https://github.com/owner/repo.git`。
3. 认证失败（403/401）：区分是 HTTPS 凭据问题还是.accesstoken 过期；不要把 token 硬编码进 remote URL 提交到仓库。
4. 代理环境：检查 `HTTPS_PROXY` 环境变量是否指向已失效的本地端口（如企业代理退出后残留），必要时清空。

## 四、Watt Toolkit 加速后仍不行

1. 确认勾选了 GitHub 相关项，并点了「一键加速」（不是只勾选）。
2. 刷新 DNS：`ipconfig /flushdns`。
3. 软件里「还原 hosts」→ 重新勾选 → 再点「一键加速」。
4. 检查 hosts 文件（`C:\Windows\System32\drivers\etc\hosts`）是否被其他软件覆盖。
5. Edge/Chrome 若开了DoH（安全 DNS），可能绕过 hosts——在浏览器设置里关闭「使用安全 DNS」。

## 五、安全与合规红线

- 用户说"加速器"时，先问清是"下载文件慢"还是"网页打不开"，前者根本不需要装软件。
- 拒绝来源不明的加速器/VPN 类软件：可能捆绑、劫持流量或违反单位网络规定。
- 只推 Watt Toolkit 这类开源、改 hosts、不全局代理的工具；若用户坚持要代理类工具，说明风险并让其自行决定。
- 安装包必须校验 SHA256 后再交付。

## 六、本机环境限制（实测）

- 自动化操作浏览器界面不稳定：进程被回收、窗口抓不到焦点、截图总切回主窗口。用户要步骤就给步骤，别反复折腾自动化。
- 桌面 DPI 缩放会让截图与点击坐标错位（本机物理 1463x914，早期误按虚拟 2560x1600 点击导致全部点空）。
- `reg.exe`、PowerShell `Add-Type` 可能被安全策略拦截；优先 Python 标准库。
- 代理端口会变化（如 58981 → 51225），每次诊断时重新读取 `HTTPS_PROXY`，不要假设固定值。
