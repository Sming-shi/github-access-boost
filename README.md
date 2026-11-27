# GitHub 访问加速（WorkBuddy Skill）

诊断并解决 GitHub 打不开、访问慢、登录失败、git clone 卡住等问题，按需提供安全的高速下载方式。

## 核心原则

- **先诊断，后开药**：用 `scripts/check_github.py` 判断卡在 DNS、连接、证书还是下载环节
- **能不装软件就不装**：只是下载 Release 文件？用 gh-proxy 镜像前缀即可
- **安全兜底**：只从官方仓库下载，可执行文件必须校验 SHA256

## 方案一览

| 场景 | 方案 |
|---|---|
| 下载 Release / raw 文件慢 | `https://gh-proxy.com/` 镜像前缀，免安装 |
| 网页打不开、全站慢 | Watt Toolkit（原 Steam++）改 hosts 加速 |
| git clone/push 卡住 | 修本机 SSL/git 配置 |
| 证书错误 | curl 加 `--ssl-no-revoke` |

## 快速开始

```bash
python scripts/check_github.py            # 诊断端点连通性
python scripts/check_github.py --release  # 查 Watt Toolkit 最新版与官方哈希
python scripts/check_github.py --verify <文件> <SHA256>  # 校验下载文件
```

## 作为 WorkBuddy Skill 使用

把整个文件夹放到 `~/.workbuddy/skills/` 下，提到"GitHub 打不开""下载加速器""clone 超时"等需求时自动触发。

## 文件结构

- `SKILL.md` — 主流程、场景判断、安全底线
- `references/mirrors.md` — 镜像源清单
- `references/troubleshooting.md` — 分类排查手册
- `references/case-record.md` — 实测案例
- `scripts/check_github.py` — 诊断与校验工具
