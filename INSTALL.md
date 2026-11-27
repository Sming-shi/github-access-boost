# 给朋友：GitHub 加速 + 中文化 安装说明

这份说明配合两个 WorkBuddy skill 使用，装好后能解决两件事：**GitHub 打不开/很慢**、**GitHub 界面是英文看不懂**。

---

## 一、你需要做什么（3 步）

### 第 1 步：拿到两个 skill 包

二选一：

- **方式 A（推荐，最简单）**：直接跟我要两个 zip 文件
  - `github-access-boost.zip` —— 解决访问慢/打不开
  - `github-chinese-userscript.zip` —— 解决界面英文

- **方式 B**：从 GitHub 下载
  - https://github.com/Sming-shi/github-access-boost
  - https://github.com/Sming-shi/github-chinese-userscript
  - 点右侧 `Code` → `Download ZIP`

### 第 2 步：装进 WorkBuddy

解压后，把**整个文件夹**放到 WorkBuddy 的 skill 目录下：

- Windows：`C:\Users\<你的用户名>\.workbuddy\skills\`
- macOS：`~/.workbuddy/skills/`

放好后目录长这样：

```
~/.workbuddy/skills/
├── github-access-boost/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
└── github-chinese-userscript/
    ├── SKILL.md
    └── references/
```

> 如果你的 WorkBuddy 有 skill 管理界面，也可以直接从界面导入 zip。

### 第 3 步：跟 WorkBuddy 说一句话

装好后不用特别配置，直接说需求即可触发：

- 「GitHub 打不开，帮我加速」 → 触发 `github-access-boost`
- 「GitHub 界面是英文，帮我汉化」 → 触发 `github-chinese-userscript`

---

## 二、装好之后会发生什么

### 加速（github-access-boost）

WorkBuddy 会：

1. **先诊断**你的网络问题（DNS 污染？连接超时？证书问题？）
2. 如果只是要下载某个文件 → 直接用镜像，**不用装任何软件**
3. 如果全站打不开 → 帮你下载官方 Watt Toolkit 安装包，并**校验哈希确保没被掉包**
4. 剩下安装和点「一键加速」要你自己做（UAC 授权 AI 代不了）

### 汉化（github-chinese-userscript）

WorkBuddy 会带你走这条已验证成功的路：

1. 官方商店装 **篡改猴**（Tampermonkey）
2. 开「允许用户脚本」开关（最容易漏的一步）
3. 装汉化脚本
4. 关掉旧标签页重新打开（脚本只在页面加载时注入）

**它不会让你去试那些失败的方案**（开发者模式扩展、本地 CRX、注册表伪装——都会在重启后失效）。

---

## 三、几个重要提醒

1. **不是全自动**。skill 是"经验+流程"，不是一键脚本。安装软件、点浏览器按钮、UAC 授权这些，还需要你本人操作。但 AI 会一步步告诉你点哪里，不会让你瞎试。

2. **汉化只翻界面，不翻内容**。导航、按钮、菜单会变中文；代码、README 正文、评论保持原样，这是正常设计。

3. **重启浏览器后应该还是中文**。如果变回英文，让 WorkBuddy 看 `troubleshooting.md` 排查——多半是「允许用户脚本」开关被关了。

4. **加速器的边界**。推荐的是 Watt Toolkit（开源、只改 hosts、不走代理）。如果有人给你推别的"加速器"，注意甄别来源，不要装来路不明的软件。

---

## 四、遇到问题

把报错截图发给 WorkBuddy，说「我 GitHub 加速/汉化卡在某某步骤」，它会读 skill 里的排障手册帮你定位。

两个 skill 的 `references/troubleshooting.md` 都记录了常见坑位和排查方法。
