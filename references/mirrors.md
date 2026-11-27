# GitHub 镜像源清单与用法

## 前缀式镜像（推荐，最省事）

把原始 GitHub 下载链接整体拼在镜像地址后面：

```
<镜像前缀> + https://github.com/owner/repo/releases/download/tag/file
```

可用前缀（按稳定性排序，主镜像不通时依次轮换）：

| 镜像 | 前缀 | 说明 |
|---|---|---|
| gh-proxy | `https://gh-proxy.com/` | 实测可用，下载 Release 速度与官方一致 |
| gh-proxy 备用 | `https://gh-proxy.net/` | 同项目备用域名 |
| gitclone | `https://ghfast.top/` | 社区镜像 |
| HubProxy | `https://hub.gitmirror.com/` | 社区镜像 |

示例（下载 Watt Toolkit v3.3.0）：

```
https://gh-proxy.com/https://github.com/BeyondDimension/SteamTools/releases/download/3.3.0/Steam%2B%2B_v3.3.0_win_x64_aot.exe
```

注意链接里的 `+` 需 URL 编码为 `%2B`，`#` 编码为 `%23`，空格编码为 `%20`。

## 专用镜像

- **Release 文件**：上述前缀式镜像即可。
- **raw 文件**：`https://raw.githubusercontent.com/...` 可尝试前缀 `https://gh-proxy.com/https://raw.githubusercontent.com/...`。
- **仓库 clone**：`git clone https://gh-proxy.com/https://github.com/owner/repo.git`。
- **国内代码托管镜像**：Gitee 上有部分热门仓库的镜像，但更新可能滞后，仅作兜底。

## 使用原则

1. **校验优先**：镜像只是传输通道，不保证内容可信。凡下载可执行文件，必须用官方 SHA256 校验（见 `scripts/check_github.py --verify`）。
2. **轮换容错**：某镜像返回 404 / 超时 / 文件大小与官方不符，换下一个；不要因为一个镜像失败就认为 GitHub 完全不可达。
3. **不要叠加代理**：镜像本身已解决访问问题，再开系统代理可能导致证书错误或速度下降。
4. **优先官方渠道**：Watt Toolkit 也可从微软商店获取，GitHub 打不开时这是更简单的官方途径。
