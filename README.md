# ZCodium-toolkit

<p align="left">
  <a href="https://github.com/bludoge305/zcode-toolkit/tree/zcodium-toolkit"><img src="https://img.shields.io/badge/branch-zcodium--toolkit-2ea44f?style=flat-square" alt="Branch"></a>
  <a href="https://github.com/bludoge305/zcode-toolkit/blob/zcodium-toolkit/CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.6.39-blue.svg?style=flat-square" alt="Version"></a>
  <img src="https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/dependencies-0%20(std%20only)-success.svg?style=flat-square" alt="Dependencies">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=flat-square" alt="Platform">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg?style=flat-square" alt="License"></a>
</p>

> **面向 ZCodium 桌面客户端的本地原生增强套件**
>
> 本仓库是 [c80361619/zcode-toolkit](https://github.com/c80361619/zcode-toolkit) 的 fork。
> 上游 `main` 当前停留在 0.6.20；本 fork 从 0.6.20 起独立维护 ZCodium 兼容线与稳定性修复，
> 当前版本 **0.6.37**，默认分支 `zcodium-toolkit` 即本维护线。

为 ZCodium 补齐原生客户端没有提供、但日常高频使用的体验：

- 📊 **TPS 状态栏**：首 Token 延迟、生成速度、会话 Token 与缓存命中率常驻输入框下方。
- 🎚️ **思考强度滑条**：点开「思考 · 档位」直接拖拽，吸附档位并即时生效。
- ✨ **增强提示词**：一键润色输入框草稿；右键可按供应商自选润色模型，随时恢复原文。
- 📈 **用量图表全量展开**：去掉官方 Top 6 / Top 5 截断，所有模型都出现在趋势图与饼图里。
- 🔍 **模型弹窗加宽**：扁平模型列表从 192px 扩到 320px，长模型名不再被省略。
- ⚡ **设置页模型拉取**：从供应商 `/models` 拉取列表，勾选后自动写入模型配置。
- 🏷️ **界面显示名替换**：把左下角显示名改成任意 1–40 字符的名字；无参执行则写回 `ZCodium`。
- 🐞 **窗口 ID 缺陷修复**：修 ZCodium 1.0.2 关窗时的 `ReferenceError`。
- 🛡️ **升级无感自愈**：感知客户端升级，退出时由单例看护批量重打补丁并自动拉起客户端。

> [!IMPORTANT]
> - 本项目是**非官方**本地补丁集，与 ZCodium / ZCode 官方团队无关联；使用前请先阅读 [免责声明](#免责声明)。
> - 所有改动只作用于**本机客户端文件**，不修改服务端、不拦截账号数据、不上报遥测。
> - 插件 id 仍为 **`zcode-tokenspeed`**，市场 id 仍为 **`zcode-toolkit`**。
>   这是有意保留的兼容标识：已安装用户的配置键是 `zcode-tokenspeed@zcode-toolkit`，
>   改名会让开关和历史配置断链。项目对外品牌叫 **ZCodium-toolkit**，内部标识不变。
> - **安装来源请填 `bludoge305/zcode-toolkit`**，不要填上游 `c80361619/zcode-toolkit`；
>   后者不含 ZCodium 兼容修复，装上去会表现为「装了但完全没反应」。

---

## 目录

- [为什么有这个 fork](#为什么有这个-fork)
- [三分钟安装](#三分钟安装)
- [装完怎么确认](#装完怎么确认)
- [功能总览](#功能总览)
- [功能详解](#功能详解)
- [斜杠命令](#斜杠命令)
- [插件开关](#插件开关)
- [命令行模式](#命令行模式)
- [工作原理与安全设计](#工作原理与安全设计)
- [故障排查](#故障排查)
- [还原与卸载](#还原与卸载)
- [兼容性](#兼容性)
- [开发与测试](#开发与测试)
- [维护这个 fork](#维护这个-fork)
- [更新日志](#更新日志)
- [致谢与许可](#致谢与许可)

---

## 为什么有这个 fork

上游项目原本只识别原版 ZCode 的进程名与数据目录。ZCodium 的进程是 `ZCodium.exe`，
数据目录是 `~/.zcodium`，而旧代码里的判断 `"zcode" in "zcodium"` 恰好为 `False`。
结果是安装探测、运行守卫、配置根解析全部命中 0 个候选，插件看起来装好了，
实际一个补丁都没打上。

本 fork 先补齐这层客户端身份识别，再沿着「看护、改名、状态判定」把 ZCodium 上暴露的问题逐个修完：

| 问题 | 本 fork 的处理 | 版本 |
|---|---|---|
| ZCodium 上「装了但完全没反应」 | 统一识别 `ZCodium.exe` / `~/.zcodium`；安装探测、运行守卫、IPC 数据根、档位机制全部适配 | 0.6.20 / 0.6.21 |
| 退出后看护找不到安装路径，客户端不被拉起 | 持久化安装路径缓存，并浅扫 `C:–H:\Apps` 等自定义安装根 | 0.6.22 |
| 多份插件副本的看护互相抢锁，补丁打一半 | 单例锁迁到数据目录，全局共享同一个 `_watchdog` | 0.6.23 |
| 每次重启都挂一个空看护 | 识别「无需迁移」为已完成，不再反复排期 | 0.6.24 |
| 缺少品牌名替换与窗口 ID 修复 | 从同作者 `ZCodium_username` 移植，并入统一的 asar 备份/还原链路 | 0.6.25 |
| 文本替换类补丁状态被判成 `unknown` | 识别 `[=]` + `失败 0`，不再每轮误报失败 | 0.6.26 |
| 改名命令没有覆盖新补丁，且容易写成一次性脚本 | 命令补齐 10 项；新增 `/zcode-patch-setdisplayname`，名字走配置直通看护 | 0.6.27 / 0.6.30 / 0.6.31 |
| 无参改名的语义反直觉 | 无参 = **强制写回 `ZCodium`**；`--revert` 才走 sidecar 精确撤销 | 0.6.32 / 0.6.36 |
| 执行改名命令后毫无反应 | 补上「待写入 → off」状态映射，改名请求能被正常排期 | 0.6.33 |
| 还原成功后持续报「状态未知」 | 补上「没有可用的 sidecar 备份 → on」映射 | 0.6.34 |
| 打完补丁后每次启动都误报「客户端升级」 | 升级判定只认版本号，不再把 asar 大小变化当成升级 | 0.6.35 |
| 状态命令在配置目标名不是 `ZCodium` 时误报待写入 | 状态命令先读配置里的 `display_name`，再按目标名检查 | 0.6.37 |

完整逐版本说明见 [CHANGELOG.md](CHANGELOG.md)；fork 的分支模型与上游同步流程见 [UPSTREAM.md](UPSTREAM.md)。

---

## 三分钟安装

### 前置条件

| 项目 | 要求 |
|---|---|
| 客户端 | ZCodium（实测 1.0.2）或原版 ZCode（实测 3.11.2 ~ 3.15.1） |
| Python | **3.10+**，`python` / `python3` 能在终端直接运行 |
| 系统 | Windows 为主；macOS / Linux 的脚本链路与 CI 同样覆盖 |
| 网络 | 首次添加插件市场需要能访问 GitHub |

### 步骤

| 步骤 | 操作 |
|:---:|---|
| **1** | 打开 ZCodium **设置 → 插件 → 右上角「创建」→「添加插件市场」** |
| **2** | 来源填：<br>`bludoge305/zcode-toolkit`<br>（默认分支已经是 `zcodium-toolkit`，不需要额外指定分支） |
| **3** | 在「个人」分段找到 **ZCodium 原生体验增强**（内部名 `zcode-tokenspeed`），点 **安装** |
| **4** | **完全退出 ZCodium**（托盘图标右键 → 退出），再启动客户端 |
| **5** | 打开任意会话发一条消息，让 `SessionStart` 钩子登记期望状态；随后再次完全退出 |
| **6** | 看护会在退出后写入补丁并自动拉起客户端；启动后即可看到效果 |

> **为什么看起来要「重启两次」？**
> 第一次启动只是让钩子把「要打哪些补丁」登记下来；真正写 `app.asar` 必须等客户端完全退出，
> 因为运行中的客户端会锁定文件、并在退出时回写配置。第二次启动读取的是已经打完补丁的 `app.asar`。
> 这是客户端生命周期决定的，不是安装步骤写错了。

### 从上游市场迁移

如果你之前添加过 `c80361619/zcode-toolkit`：

1. 先在插件管理里卸载旧插件；
2. 移除旧市场（避免两个同名插件同时出现）；
3. 按上面的步骤添加 `bludoge305/zcode-toolkit`；
4. 重新安装并重启两次。

已保存的开关通常仍可用，因为插件 id 和市场 id 都保持不变；如果配置页显示的是旧值，
重新拨一次并保存即可。

---

## 装完怎么确认

在客户端里直接输入：

```text
/zcode-patch-status
```

它会只读检查全部 10 项，并用中文表格给出「已打 / 未打 / 不适用 / 目标不存在」。

也可以从命令行做一次完整自检：

```bash
# 先定位插件实际安装目录（不要站在 cache/<市场名> 这一层找 scripts）
python "<skill目录>/scripts/doctor.py" --where

# 只读体检：安装位置、插件启用、配置、心跳、10 项补丁状态
python "<skill目录>/scripts/doctor.py"

# 一条命令检查全部补丁
python "<skill目录>/scripts/zcode_patcher.py" --all --check
```

正常结果应包含：

```text
合计 10 项：成功 10，失败 0
```

> `成功 10` 表示 10 项都**检查出了确定状态**，不等于 10 项都已经写入。
> 例如品牌名替换会显示「待写入（当前值：Bludoge）」，这是配置目标与当前 asar 不一致，
> 退出客户端后看护会把它改成目标值。

找不到 `<skill目录>` 时，直接运行：

```powershell
# Windows：列出所有候选 doctor.py
Get-ChildItem "$env:USERPROFILE\.zcodium\cli\plugins", "$env:USERPROFILE\.zcode\cli\plugins" `
  -Recurse -Filter doctor.py -ErrorAction SilentlyContinue |
  Select-Object -ExpandProperty FullName
```

```bash
# macOS / Linux
find ~/.zcodium/cli/plugins ~/.zcode/cli/plugins -name doctor.py 2>/dev/null
```

GitHub 来源的市场通常落在：

```text
<数据目录>/cli/plugins/cache/<市场名>/<插件名>/<版本>/
```

目录来源（本地仓库 / directory source）则落在：

```text
<数据目录>/cli/plugins/marketplaces/<市场名>/
```

插件根在版本目录或市场目录**里面**，`skills/` 不在 `cache/<市场名>` 这一层。

---

## 功能总览

| 功能 | 开关键 | 默认 | 写入对象 | 说明 |
|---|---|:---:|---|---|
| TPS 状态栏 | `tps_footer` | 开 | `app.asar` | 输入框下方统计条：本轮 + 会话累计，右键切换位置 |
| 思考强度滑条 | `thought_slider` | 开 | `app.asar` | 「思考 · 档名」入口，拖拽吸附，原生回调即时生效 |
| 增强提示词 | `enhance_prompt` | 开 | `app.asar` + IPC | 一键润色；右键自选模型；支持恢复原文 |
| 用量页去截断 | `usage_chart` | 开 | `app.asar` | 趋势图 / 饼图全量展示，不再只画 Top 6 / Top 5 |
| 模型弹窗加宽 | `model_width` | 开 | `app.asar` | 扁平模型列表 192px → 320px |
| 设置页模型拉取 | `model_puller` | 开 | `app.asar` + IPC | 从供应商 `/models` 拉取并批量写入 |
| 思考档位配置（3.14+） | `reasoning_config` | 开 | `provider_config.json` | 原生 `optionSpecs`，不需要内核补丁 |
| 界面显示名称 | `display_name` | 空串 | `app.asar` | 空串 = 强制写回 `ZCodium`；非空 = 改成该名字 |
| 窗口 ID 缺陷修复 | `window_id_fix` | 开 | `app.asar` | 修 ZCodium 1.0.2 关窗 `ReferenceError` |
| 思考档位内核补丁（旧版） | `core_patch` | 开 | `zcode.cjs` | 仅 ≤ 3.11.2 需要；3.14+ 自动识别为「不适用」 |

> 前 9 项是当前主功能；最后一项是旧版内核的兜底补丁。3.14+ 客户端会自动跳过它，
> 不会误报失败，也不会改写内核。

---

## 功能详解

### 1. TPS 状态栏

- 只在**主对话输入框**下方显示；侧边栏辅助对话不会重复挂载。
- 本轮指标：首 Token 延迟、生成速度、输出 Token；会话累计：输入 / 输出 / 总量 / 思考 Token。
- 缓存命中率按两位小数显示。
- **右键统计条**可切换显示位置。
- 数据来自客户端自身的事件流与 `usage.delta`，不额外发请求。

### 2. 思考强度滑条

- 点击输入框工具栏的「思考 · 档名」文字，弹出吸附式拖拽条。
- 拖到目标档位释放即刻生效；主题、禁用态、`prefers-reduced-motion` 都做了适配。
- 走客户端原生档位回调，不逆向协议、不改请求体格式。

### 3. 增强提示词

- **左键**：用当前选中的模型润色输入框草稿；可一键「恢复原文」。
- **右键**：按供应商分组列出可用模型，选中后持久化到 `enhance_config.json`，下次点击直接使用。
- 菜单关闭策略：点外部、按 `Esc`、再次右键收起；滚动或高频事件不会误关。
- 如果润色请求报 `Model is unavailable`，通常是供应商被禁用、模型配置不在
  `provider_config.json`，或界面选择解析失败。用只读诊断：

  ```bash
  python "<skill目录>/scripts/enhance_doctor.py" --model-value "<providerId>/<modelId>"
  ```

  看输出里的 `how=`：只有 `explicit` / `config` / `ref` 才代表真的用上了你指定的模型。

### 4. 用量页去截断

- 「设置 → 用量」的趋势图与饼图改为全量展示。
- 趋势图不再只画 Top 6，饼图不再把剩余模型合并成「其他」。
- 使用弹性正则匹配混淆后的变量名；客户端小版本升级后仍会自动重试匹配。

### 5. 模型弹窗加宽

- 无子菜单的扁平模型列表：`192px → 320px`，长模型名完整显示。
- 渠道子菜单在新版上游已改为自适应宽度（`w-max min-w-48`）。脚本识别到后
  会报「无需补丁」，这是正常的，不是失败。

### 6. 设置页模型拉取

- 设置页新增「⚡ 自动拉取模型」按钮。
- 从当前供应商的 `/models` 接口读取模型列表，勾选后写入：
  - `config.json` 的供应商模型条目；
  - `provider_config.json` 的 `providerModelRules` / `optionSpecs`（3.14+ 界面实际读取的位置）。
- 新模型默认按服务端元数据写 `context_length` / `max_output_tokens` / 思考档位；
  服务端没给元数据时退回 `1M / 128k + off/high/max` 模板。
- 已有条目默认保留；`--refresh` 会按服务端元数据刷新已有条目的 limit 与档位，其余键不动。
- API Key 复用你已配置的供应商凭据，不需要额外填写。

### 7. 思考档位配置（3.14+ 原生）

- 3.14+ 客户端不再需要改内核，档位由配置侧的 `optionSpecs.reasoningLevel` 下发。
- 本功能把 `config.json` 里的档位迁移进 `provider_config.json`：
  - `values`：界面档位列表，末位为默认档；
  - `map`：CEL 映射，请求前求值并合并进请求体；
  - 支持 `maxOutputTokens` 上限。
- 已在界面手动配置过的模型（`manualProviderModelRules`）会自动跳过，避免同一模型出现在
  两个规则列表里导致整份供应商配置降级为空。
- 关闭该开关的语义是**不托管**：停止自动同步，但不会主动还原 `provider_config.json`，
  避免和客户端退出时的回写互相打架。

**旧版内核补丁（≤ 3.11.2）**：3.14+ 客户端会自动识别为「本补丁不适用」，不需要手动关闭。
只有 3.11.2 及更早版本才需要 `core_patch`。

### 8. 界面显示名称

在客户端里执行：

```text
/zcode-patch-setdisplayname Bludoge
```

或直接编辑插件配置里的「界面显示名称」文本框。规则：

| 输入 | 结果 |
|---|---|
| `Bludoge` | 界面左下角显示 `Bludoge` |
| 留空 / `/zcode-patch-setdisplayname` 不带参数 | **强制写回 `ZCodium`** |
| `--display-name --revert` | 从 sidecar 精确撤销到打补丁前的原始字节 |

- 名字长度 1–40 字符，不能含引号、反引号、反斜杠或换行。
- 长度变化时会自动整包重打包 `app.asar`；同长度则走字节级原地替换。
- 「无参 = 写回 ZCodium」是 0.6.36 起的固定语义。不要把它理解成「恢复发行版原值」：
  ZCodium 1.0.2 的 asar 原值可能是 `Bludoge`，按原值还原并不能得到 `ZCodium`。
- `/zcode-patch-status` 会先读配置里的目标名再检查；配置目标不是 `ZCodium` 时不会再误报。

### 9. 窗口 ID 缺陷修复

ZCodium 1.0.2 的渲染层里有：

```js
.disposeWindow(browserWindowId)
```

但同作用域内实际可用的变量是 `n = e.webContents.id`，导致关闭窗口时抛 `ReferenceError`。
补丁将其改为 `.disposeWindow(n)`。如果上游版本已经自行修复，脚本会报
「目标不存在（已修复/无需处理）」，这是正常结果，不是失败。

### 10. 升级无感自愈

- `SessionStart` 钩子调用 `sync.py --detach`，先登记期望状态，再尝试立即写入。
- 客户端运行中写入会被拒绝，任务自动转交 `apply_after_exit.py` 看护。
- 看护是**跨副本单例**：无论机器上有几份插件副本，只有一个进程能在客户端退出后写 `app.asar`。
- 多项补丁按方向合并成一次批量重打包，2~3 秒完成，减少快速重启造成的文件争抢。
- 客户端升级检测只认**版本号**。同版本下 asar 大小变化（包括本插件自己改的）不再误报升级。
- 写入完成后自动拉起客户端；如果客户端已经被其他实例拉起，看护不会重复启动。

---

## 斜杠命令

| 命令 | 作用 | 说明 |
|---|---|---|
| `/zcode-patch-status` | 只读检查全部 10 项 | 不写盘；品牌名按配置目标检查 |
| `/zcode-patch-apply` | 注入指定补丁 | 单功能单命令；重打包级补丁需先退出客户端 |
| `/zcode-patch-revert` | 从备份精确还原 | 支持单项或全量；不会把旧版内核盖回新客户端 |
| `/zcode-patch-doctor` | 诊断 / 一键自愈 | 默认只读；`--fix` 会启用插件并排期补齐 |
| `/zcode-patch-toggle` | 查看 / 切换插件开关 | 读取配置值 + 实际注入状态，两列对照 |
| `/zcode-patch-setdisplayname` | 修改 / 还原界面显示名 | 不带参数 = 强制写回 `ZCodium` |

命令会加载插件自带的 `zcode-tokenspeed` 技能，按技能里的标准流程执行；
不需要你手动拼脚本路径。

---

## 插件开关

开关保存在客户端配置的 `plugins.options["zcode-tokenspeed@zcode-toolkit"]`：

- 原版 ZCode：`~/.zcode/cli/config.json`
- ZCodium：`~/.zcodium/cli/config.json`

| 键 | 类型 | 默认 | 行为 |
|---|---|:---:|---|
| `reasoning_config` | 布尔 | `true` | 3.14+ 档位配置；关闭 = 不托管，不主动还原 |
| `usage_chart` | 布尔 | `true` | 用量图表全量 |
| `model_width` | 布尔 | `true` | 模型弹窗加宽 |
| `tps_footer` | 布尔 | `true` | TPS 状态栏 |
| `thought_slider` | 布尔 | `true` | 思考强度滑条 |
| `enhance_prompt` | 布尔 | `true` | 增强提示词按钮 |
| `model_puller` | 布尔 | `true` | 设置页模型拉取按钮 |
| `core_patch` | 布尔 | `true` | ≤ 3.11.2 内核补丁；3.14+ 自动跳过 |
| `display_name` | 字符串 | `""` | 目标显示名；空串 = 强制写回 `ZCodium` |
| `window_id_fix` | 布尔 | `true` | 窗口 ID 缺陷修复 |

**零配置自动注入**：从没保存过配置时，`sync.py` 会读取 `.zcode-plugin/plugin.json`
里 `userConfig.*.default` 的默认值（全开），所以装完不需要先打开配置页。
保存过一部分时，保存值优先、缺失键补默认值；显式关掉的开关会被正常还原。

**生效时机**：所有补丁都要等客户端**完全退出**后由看护写入，再启动才生效。
会话钩子必然在客户端运行中触发，所以「会话内立即生效」这条路走不通；
纯 CLI 场景（客户端没在运行）可以即时写入。

---

## 命令行模式

以下命令均只依赖 Python 标准库。`<skill目录>` 指
`.../skills/zcode-tokenspeed`，可用上一节的 `doctor.py --where` 定位。

### 全量体检 / 预演 / 应用 / 还原

```bash
# 只读体检全部 10 项
python "<skill目录>/scripts/zcode_patcher.py" --all --check

# 预演：只报告会改哪些文件，不写盘
python "<skill目录>/scripts/zcode_patcher.py" --all --dry-run

# 应用全部补丁（先完全退出 ZCodium）
python "<skill目录>/scripts/zcode_patcher.py" --all

# 全量精确还原
python "<skill目录>/scripts/zcode_patcher.py" --all --revert
```

> `--all` 对「界面显示名称」使用无参语义：**目标是 `ZCodium`**。
> 如果你在配置里设过自定义名字，`--all` 会把显示名写回 `ZCodium`；
> 想保留自定义名字时，请用单项参数执行其他补丁，或先单独确认
> `--display-name --name "<你的名字>" --check`。

### 单项操作

```bash
# 用量页去截断
python "<skill目录>/scripts/zcode_patcher.py" --usage-chart --check
python "<skill目录>/scripts/zcode_patcher.py" --usage-chart

# 模型弹窗加宽
python "<skill目录>/scripts/zcode_patcher.py" --model-width --check

# TPS 状态栏
python "<skill目录>/scripts/zcode_patcher.py" --tps-footer --check

# 思考强度滑条
python "<skill目录>/scripts/zcode_patcher.py" --thought-slider --check

# 增强提示词
python "<skill目录>/scripts/zcode_patcher.py" --enhance-prompt --check

# 模型拉取按钮
python "<skill目录>/scripts/zcode_patcher.py" --model-puller --check

# 窗口 ID 缺陷修复
python "<skill目录>/scripts/zcode_patcher.py" --window-id-fix --check

# 3.14+ 档位配置
python "<skill目录>/scripts/zcode_patcher.py" --reasoning-config --check
python "<skill目录>/scripts/zcode_patcher.py" --reasoning-config --dry-run
python "<skill目录>/scripts/zcode_patcher.py" --reasoning-config
python "<skill目录>/scripts/zcode_patcher.py" --reasoning-config --revert
```

### 显示名称

```bash
# 只读确认：当前值 + 目标值
python "<skill目录>/scripts/zcode_patcher.py" --display-name --name "Bludoge" --check

# 改成 Bludoge
python "<skill目录>/scripts/zcode_patcher.py" --display-name --name "Bludoge"

# 不带 --name：强制写回 ZCodium
python "<skill目录>/scripts/zcode_patcher.py" --display-name

# 精确撤销到打补丁前（走 sidecar）
python "<skill目录>/scripts/zcode_patcher.py" --display-name --revert
```

### 诊断与恢复

```bash
# 安装自检（只读）
python "<skill目录>/scripts/doctor.py"
python "<skill目录>/scripts/doctor.py" --json
python "<skill目录>/scripts/doctor.py" --where

# 一键自愈：启用插件、重打补丁或排期看护
python "<skill目录>/scripts/doctor.py" --fix

# 增强提示词链路诊断
python "<skill目录>/scripts/enhance_doctor.py" --json

# 从供应商拉取模型（CLI 版，不动 asar）
python "<skill目录>/scripts/model_pull.py" --provider <关键字> --dry-run
python "<skill目录>/scripts/model_pull.py" --provider <关键字> --refresh

# 紧急整包还原：客户端打不开时用
python "<skill目录>/scripts/restore_clean.py" --latest
```

`restore_clean.py` 默认备份目录是 `~/.zcode/patcher-backups`；ZCodium 用户建议显式指定：

```bash
python "<skill目录>/scripts/restore_clean.py" --backup-dir "$HOME/.zcodium/patcher-backups" --latest
```

### 通用参数与退出码

| 参数 | 作用 |
|---|---|
| `--check` | 只读检查，不写盘 |
| `--dry-run` | 预演，报告将改什么 |
| `--revert` | 从备份 / sidecar 还原 |
| `--all` | 对所有功能生效，可和 `--check` / `--dry-run` / `--revert` 组合 |
| `--verbose` | 打印安装探测细节 |
| `--force` | 跳过备份指纹校验；可能把旧版文件盖回新客户端，**慎用** |
| `--prune` | 清理旧归档与临时文件；`--deep` 连当前备份一起清，清后无法 `--revert` |

退出码：

| 退出码 | 含义 |
|:---:|---|
| `0` | 成功 |
| `1` | 有补丁执行失败 |
| `2` | 检测到客户端正在运行，拒绝写入 |

`--check` / `--dry-run` 不受运行守卫限制；写入与还原必须先完全退出客户端。

### 一键自愈单行命令

不想先找脚本路径时，可以直接在终端运行（同时覆盖 `.zcodium` 与 `.zcode`）：

```powershell
# Windows（CMD / PowerShell 均可）
python -c "import pathlib,subprocess,sys; roots=[pathlib.Path.home()/'.zcodium',pathlib.Path.home()/'.zcode']; p=next((x for r in roots for x in r.glob('**/doctor.py')),None); subprocess.run([sys.executable,str(p),'--fix']) if p else print('未找到已安装的插件，请先在客户端内安装')"
```

```bash
# macOS / Linux
python3 -c "import pathlib,subprocess,sys; roots=[pathlib.Path.home()/'.zcodium',pathlib.Path.home()/'.zcode']; p=next((x for r in roots for x in r.glob('**/doctor.py')),None); subprocess.run([sys.executable,str(p),'--fix']) if p else print('未找到已安装的插件，请先在客户端内安装')"
```

全量还原单行命令：

```powershell
python -c "import pathlib,subprocess,sys; roots=[pathlib.Path.home()/'.zcodium',pathlib.Path.home()/'.zcode']; p=next((x for r in roots for x in r.glob('**/zcode_patcher.py')),None); subprocess.run([sys.executable,str(p),'--all','--revert']) if p else None"
```

---

## 工作原理与安全设计

### 组件

| 组件 | 职责 |
|---|---|
| `hooks/hooks.json` | 在 `SessionStart` 调用 `sync.py --detach` |
| `sync.py` | 合并配置默认值、检查实际状态、尝试立即写入、必要时排期看护 |
| `apply_after_exit.py` | 单例看护：等客户端退出 → 批量应用/还原 → 原子重打包 → 拉起客户端 |
| `zcode_patcher.py` | 安装探测、asar 解析/重打包、补丁实现、状态检查、备份与还原 |
| `doctor.py` | 安装位置、启用状态、心跳、配置与补丁状态的只读诊断 |
| `commands/*.md` | 客户端内的斜杠命令入口 |

### 一次同步的流程

```text
SessionStart
  └─ sync.py --detach
       ├─ 读取 ~/.zcodium/cli/config.json（或 ~/.zcode/cli/config.json）
       ├─ 缺失键补 plugin.json 默认值
       ├─ 对每项跑 --check
       ├─ 客户端没运行 → 立即写入
       └─ 客户端在运行 → 写入 _watchdog.want，启动单例看护
                              └─ 等 ZCodium.exe / ZCode.exe 全部退出
                                   ├─ 按应用/还原方向合并任务
                                   ├─ 一次批量重打包 app.asar
                                   ├─ 校验 SHA-256 / offset / integrity
                                   └─ 自动拉起客户端
```

### 补丁类型

| 类型 | 代表功能 | 写入方式 |
|---|---|---|
| 字节级原地覆盖 | 用量图表、模型加宽 | 同长度替换，不改 offset，更新条目 integrity |
| ASAR 重打包 | TPS、滑条、增强提示词、模型拉取、显示名、窗口 ID | 增删/改条目后重排 offset 并校验全量 integrity |
| 配置侧 | 思考档位（3.14+） | 写 `provider_config.json`，不动 asar |
| 旧版内核 | `core_patch`（≤ 3.11.2） | 改 `glm/zcode.cjs` |

### 安全设计

- **运行守卫**：同时识别 `ZCodium.exe` 与 `ZCode.exe`；运行中拒绝写入 asar / 配置，
  只允许 `--check` / `--dry-run`。
- **备份与 sidecar**：首次写入前生成 `.bak` 与补丁 sidecar；支持按补丁精确撤销，
  多个补丁共存时互不误伤。
- **版本指纹**：备份带客户端版本指纹；客户端升级后旧备份自动归档，还原时拒绝跨版本覆盖。
- **完整性校验**：重打包后校验每个条目的 SHA-256、offset 与 integrity 记录，
  防止布局错位导致客户端打不开。
- **并发保护**：写入全程有文件锁；看护使用跨副本共享的单例锁，避免多进程同时重打包。
- **幂等**：重复执行同一补丁会识别「已打 / 已是目标内容」并跳过，不会反复叠加。
- **无遥测**：不向任何服务器上报使用数据；只有「模型拉取」和「增强提示词」会请求你配置的
  供应商接口，行为与客户端自身的模型请求一致。

### 文件位置

| 内容 | 位置 |
|---|---|
| 客户端安装 | 自动探测；ZCodium 常见于 `D:\Apps\ZCodium` 等自定义目录 |
| ASAR | `<安装根>/resources/app.asar` |
| 旧版内核 | `<安装根>/resources/glm/zcode.cjs` |
| 数据目录 | `~/.zcodium`（ZCodium）或 `~/.zcode`（原版） |
| 看护状态 | `<数据目录>/_watchdog.pid`、`_watchdog.want` |
| 安装路径缓存 | `<数据目录>/zcode_install_path.txt` |
| 同步日志 / 心跳 | 插件 `scripts/_sync.log`、`scripts/_sync.last` |
| 紧急还原备份 | `~/.zcode/patcher-backups`（可用 `--backup-dir` 覆盖） |

---

## 故障排查

### 装了但完全没反应

按顺序排查：

1. **插件是否启用**：设置 → 插件 → 已安装，确认开关是开。
2. **是否真的触发过钩子**：看 `scripts/_sync.last` 是否存在；不存在说明 `SessionStart`
   从未执行。重启客户端后必须**真的打开一个会话**。
3. **插件装在哪**：运行 `doctor.py --where`。GitHub 来源的脚本在
   `cache/<市场名>/<插件名>/<版本>/skills/...`，不要站在 `cache/<市场名>` 这一层。
4. **看完整诊断**：`doctor.py` 会直接给出卡点结论；贴给别人时用 `doctor.py --json`。
5. **环境**：确认 `python --version` 是 3.10+，且客户端能继承到 `PATH` 里的 Python。

### 客户端升级后补丁失效

这是预期行为：升级会整体覆盖 `app.asar`。本插件会感知版本变化并重新排期看护。
通常只需要：

1. 完全退出客户端；
2. 重新启动，打开一个会话；
3. 再完全退出一次，让看护写入；
4. 再次启动验证。

如果仍不生效，运行：

```bash
python "<skill目录>/scripts/doctor.py" --fix
```

### 每次启动都提示「客户端升级」

0.6.35 起已修：升级判定只认版本号，不再把 asar 大小变化当成升级。
如果你仍看到该提示，先确认插件版本 ≥ 0.6.35，并检查是否有旧副本在运行：

```bash
python "<skill目录>/scripts/doctor.py" --where
```

### 改名没反应 / 状态未知

- 确认配置里的 `display_name` 是目标名字，而不是 `true` / 空串。
- `/zcode-patch-status` 会按配置目标检查；如果显示「待写入」，退出客户端让看护执行。
- 执行 `/zcode-patch-setdisplayname <名字>` 后不要自己写一次性看护脚本；名字会走配置直通现有看护链路。
- 想看当前实际值：`--display-name --check` 会打印「当前值：X」。

### 状态显示「待写入」但界面已经是目标名

这通常不是故障，而是 asar 里存在多个品牌字面量，或检查目标与配置目标不一致。
0.6.37 起状态命令会先读配置里的 `display_name` 再检查；如果仍有疑问，跑：

```bash
python "<skill目录>/scripts/zcode_patcher.py" --display-name --name "<配置里的名字>" --check
```

### 写入失败 / `WinError 5` / 文件被占用

客户端还在运行。完全退出（托盘右键 → 退出），确认任务管理器里没有
`ZCodium.exe` / `ZCode.exe` / crashpad 残留，再重试。看护会自动处理正常的退出流程。

### 模型拉取按钮不出现

- 确认插件版本与客户端版本匹配；3.15.x 使用 `model-provider-add-model-button` 契约。
- 设置页如果不是弹窗形态，早期版本可能把按钮挂到不可见区域；0.6.19 起已对齐。
- 运行 `--model-puller --check` 看四个组件是否齐全：
  `renderer 脚本 / index.html 挂载 / preload 桥 / main handler`。

### 增强提示词失败 / `Model is unavailable`

1. 右键按钮，明确选择一个当前供应商下可用的模型；
2. 确认该供应商没有被 `systemDisabledReason` 禁用；
3. 确认模型在 `provider_config.json` 里而不仅在 `config.json` 里；
4. 用 `enhance_doctor.py --model-value "<providerId>/<modelId>"` 看 `how=`。

### 客户端打不开 / 启动异常

先完全退出客户端，再运行紧急还原：

```bash
python "<skill目录>/scripts/restore_clean.py" --latest
```

如果备份目录不是默认位置：

```bash
python "<skill目录>/scripts/restore_clean.py" --backup-dir "$HOME/.zcodium/patcher-backups" --latest
```

还原前可以先保存当前安装：

```bash
python "<skill目录>/scripts/restore_clean.py" --backup
```

### 日志在哪

| 文件 | 内容 |
|---|---|
| `scripts/_sync.log` | 每次同步做了什么、失败原因 |
| `scripts/_sync.last` | 最近一次心跳，证明钩子跑过 |
| `scripts/_apply_after_exit.log` | 看护写入、重打包、重启过程 |
| `logs/autopilot-*.log` / `.jsonl` | 开发流水线的文本 / 结构化日志 |

---

## 还原与卸载

### 只还原补丁，保留插件

```text
/zcode-patch-revert
```

或命令行：

```bash
python "<skill目录>/scripts/zcode_patcher.py" --all --revert
```

也可以只还原某一项，例如：

```bash
python "<skill目录>/scripts/zcode_patcher.py" --tps-footer --revert
```

### 完全卸载

**先还原，再卸载。** 直接卸载插件不会自动撤销已经写进 `app.asar` 的补丁。

1. 完全退出客户端；
2. 运行 `--all --revert`，或 `/zcode-patch-revert`；
3. 启动客户端确认界面恢复原状；
4. 在插件管理中卸载 `ZCodium 原生体验增强`；
5. 如不再使用，移除 `bludoge305/zcode-toolkit` 市场。

如果客户端已经异常到无法启动，改用 `restore_clean.py --latest`。

<details>
<summary><b>📜 历史版本审计与故障排查记录</b></summary>

> 以下为**上游原版 ZCode** 的历史记录（0.6.5 – 0.6.16）。本 fork 自 0.6.20 起独立演进，
> ZCodium 适配与后续变更见 [CHANGELOG.md](CHANGELOG.md)。

#### 0.6.16（解决思考档位关闭导致退出无限重启死循环，Issue #5）
- **语义修正为“不托管”**：3.14+ 思考档位配置目标为客户端自带的 `provider_config.json`；当开关关闭时语义明确为“停止托管与同步”，插件不再主动写入，且绝不主动还原该文件，彻底切断“退出还原 → 客户端重启写回 → 再次检测冲突 → 再次看护还原”的无限死循环；
- **看护空任务守卫**：`apply_after_exit.py` 严格过滤 `reasoning_config=off` 任务；若最终无待执行补丁任务，看护直接安全退出，杜绝空任务挂起等待与退出自动重启 ZCode。
- **全平台兼容吸收**：完整吸纳 PR #4 对 macOS 看护链路的跨平台支持与 crashpad 僵尸进程排除。

#### 0.6.20（彻底修复提示词润色失败与“显示已完成但不出现文案”问题）
- **根治会话隔离误杀（不出现润色文案）**：重构跨会话防护判定，当当前输入框依然处于聚焦/就绪状态且文本未被篡改时，直接写入润色结果；改进草稿会话临时键生成机制，杜绝 DOM 重绘导致的虚假跨会话切换误杀（不再提示“原会话提示词润色已完成未写入当前会话”）；
- **深度思考（Reasoning）与空内容兜底**：适配 DeepSeek-R1、GLM-5.3 等带深度思考的模型，当 `content` 处于空字符串时自动从 `reasoning_content` 提取润色文本，消除“模型返回了空内容”误报；
- **智能故障转移（Fallback Recovery）**：当当前所选模型遭遇余额不足（400/402）、上游超时、服务异常或返回空回复时，自动无缝尝试其他可用供应商的备用模型完成润色并给出友好提示，彻底避免润色中断；
- **补齐 Anthropic 必填协议头**：针对 `anthropic-messages` 协议自动补齐 `anthropic-version: 2023-06-01` 请求头，解决部分中转站与官方端点 400 Bad Request 拒绝问题。

#### 0.6.19（对齐官方开源代码仓库规范与深度全方位优化）
- **DOM 锚点全面对齐官方 `test-ids` 契约**：根据上游官方开源代码规范（`v3.15.1`，commit `aac4755`），重构模型拉取按钮挂载点（对齐 `[data-testid="model-provider-add-model-button"]`）、提示词增强与思考强度滑条探针（优先对接官方 `[data-testid="v4-model-config"]`），彻底根除基于脆弱文案或坐标扫描的失效隐患；
- **TPS 状态栏深度遥测与校准**：捕获官方下发的 `turnHeader.modelDurationMs`，扣除网络排队与流式波动，精准校准整轮纯模型生成速度；捕获 `usage.delta` 原生 `reasoningTokens` 与 `cacheWriteTokens`，实时与会话累计段新增思考 Token 消耗指标（`思考 xx` / `累思 xx`）；
- **Composer 工具栏双态按钮追踪**：升级支持 `[data-testid='v4-composer-send'], [data-testid='v4-stop']`，在流式生成期间精准锁定工具栏位置，彻底消除回退漂移；
- **用量图表补丁自适应正则匹配**：用量图表去截断补丁升级为弹性正则嗅探引擎，免受版本混淆压缩变量名变更影响；
- **配置侧原生支持 `maxOutputTokens`**：`--reasoning-config` 同步引擎深度支持 `maxOutputTokens` CEL map 映射及上限写入，完美适配新版 OptionSpecs 规范；
- **官方版本认证**：全量通过 316+ 项单元与集成测试，实测认证覆盖 3.11.2 ~ 3.15.1。

#### 0.6.15（彻底根治会话生成中润色模型漂移与失败问题）
- **会话粘性记忆与侧边栏隔离**：`zcode-enhance-prompt.js` 引入 `lastKnownModel` 会话粘性记忆，流式生成中当原生工具栏处于禁用/重绘瞬态时无缝沿用该会话最新选中的模型；全局搜索强制排除侧边栏，杜绝抓取辅助对话的模型；
- **跨脚本实时事件信源联动**：`zcode-tps.js` 捕获 ServicePort 事件流的底层实时 `ev.modelId` 并暴露全局，形成模型定位双保险；
- **主进程坚守当前供应商**：`zcode_patcher.py` 优化解析引擎，中转站与自定义模型只要所属供应商有效即坚守在该供应商发请求，彻底杜绝越界 Fallback 到系统其他无关供应商导致 400 失败的问题。

#### 0.6.14（TPS 状态栏优化：去除 out 替换为会话总用量）
- **即时指标精简**：彻底去除含义模糊的单轮 `out`，本轮指标聚焦于「首 Token 延迟」与「生成速率」，视觉更清爽；
- **会话总 Token 展示**：在会话累计组新增 `总用 xx` Token 消耗量统计（`累计输入 + 累计输出`），一目了然看清当前会话整体 Token 消耗。

#### 0.6.13（提示词增强侧边栏隔离、看护批处理重打包与 3.14.5 适配）
- **提示词增强侧边栏隔离**：`zcode-enhance-prompt.js` 补齐侧边栏边界判定（`isInsideSidePane`）与等高靠左优先保序，自愈分支杜绝误挂，彻底根治侧边栏辅助对话导致润色按钮飘移的竞态；
- **看护批处理极速重打包**：`apply_after_exit.py` 重构任务调度引擎，同方向（应用或还原）多项补丁合并为单次批量调用，ASAR 重打包耗时从 20s+ 缩短至 2~3s，消除用户快速重启造成的进程冲突隐患；
- **客户端版本认证**：完成最新客户端版本 `3.14.5` 实测认证，全量 250+ 项单元与集成测试全绿通过。

#### 0.6.12（修复侧边栏辅助对话双 Composer 竞态跳动）
- 修复当侧边栏开启「辅助对话」时双输入框在同一高度竞态导致 TPS 状态栏来回跳动的问题；
- 新增 `isInsideSidePane` 与 `isInsideMainConversation` 边界判断，严格限定只在主界面对话框下显示，彻底消除跳动与轮次数据串台。

#### 0.6.11（升级自愈与看护优化）
- `sync.py` 引入客户端指纹比对，自动识别客户端升级并重置通知标记，自动调度看护；
- `apply_after_exit.py` 补齐 7 项补丁，并实现 `_watchdog.pid` + `_watchdog.want` 单例互斥与需求合并；
- `doctor.py` 增加 `--fix` 一键自愈命令。

#### 0.6.10（旧脚本失效检测）
- 修复 `_process_script_inject` 的 check 分支仅检查结构未比对内容的缺陷，新增内容哈希比对并标记 stale。

#### 0.6.8 - 0.6.9（TPS 精度与菜单交互）
- 状态栏平均命中率改为精确到两位小数；
- 优化提示词右键菜单的关闭机制，消除滚动与多频事件误关问题。

#### 0.6.5（ASAR 布局错位保护）
- 引入 `_AsarWriteLock` 进程锁与文件锁；
- 全域逐条 integrity 校验，防范错位启动崩溃。

</details>

---

## 兼容性

| 客户端 | 版本 | 状态 |
|---|---|---|
| ZCodium | 1.0.2 | 实测；`--all --check` 10 项全部有结论 |
| ZCode 原版 | 3.11.2 | 支持；思考档位走旧版内核补丁 |
| ZCode 原版 | 3.14.x ~ 3.15.1 | 支持；思考档位走原生 `optionSpecs`，内核补丁自动跳过 |
| Python | 3.10 / 3.12 / 3.13 | CI 覆盖；低于 3.10 会拒绝运行 |
| Windows | 10 / 11 | 主要测试平台 |
| macOS / Linux | 当前 CI 覆盖 | 脚本链路与看护已跨平台；社区反馈欢迎 |

**Node.js** 只用于 CI 里的注入脚本语法检查（`node --check`）和少量浏览器冒烟测试，
不是运行时依赖。运行插件只需要 Python 标准库。

已知边界：

- 客户端大版本更新可能改变 asar 结构或 DOM 锚点。先用 `--check` / `--dry-run` 验证，
  失败时按脚本报告定位，不要手工改 asar。
- 模型弹窗加宽只处理扁平列表；渠道子菜单在新版上游已自适应，脚本会报「无需补丁」。
- 窗口 ID 修复在上游已修复的版本上是 no-op，不报失败。
- 显示名替换依赖品牌字面量存在；如果发行版改成完全不同的品牌表达式，脚本会报告
  「目标不存在」而不是猜测。
- macOS / Linux 的看护链路已有实现与 CI，但 ZCodium 主要在 Windows 上使用；
  跨平台问题请附 `doctor.py --json` 与 `--all --check` 输出。

---

## 开发与测试

### 目录结构

```text
.
├─ .zcode-plugin/plugin.json          # 插件清单、10 个 userConfig 开关
├─ marketplace.json                   # 市场清单（市场 id 保持 zcode-toolkit）
├─ hooks/hooks.json                   # SessionStart → sync.py --detach
├─ commands/                          # 6 个斜杠命令
├─ skills/zcode-tokenspeed/
│  ├─ SKILL.md                        # 给 AI / 维护者的完整操作手册
│  └─ scripts/
│     ├─ zcode_patcher.py             # 补丁核心（探测 / asar / 备份 / 还原）
│     ├─ sync.py                      # 开关合并、状态检查、看护排期
│     ├─ apply_after_exit.py          # 退出后单例看护
│     ├─ doctor.py                    # 安装与补丁诊断
│     ├─ enhance_doctor.py            # 增强提示词链路诊断
│     ├─ model_pull.py                # CLI 模型拉取
│     ├─ restore_clean.py             # 紧急整包还原
│     └─ zcode-*.js                   # 注入到渲染层 / 主进程的脚本
├─ tests/                             # 350 项 Python 回归 + JS 冒烟
├─ bootstrap.py                       # 面向人的交互式引导
├─ autopilot.py                       # 无人值守流水线
└─ .github/workflows/ci.yml           # 多平台 CI
```

### 常用命令

```bash
# 交互式自检：环境 → 依赖 → 语法 → 测试 → 状态
python bootstrap.py

# 无人值守流水线：不碰客户端
python autopilot.py --no-deploy --unattended --report ci-report.md --log logs/ci.log

# 只跑回归测试
python -m unittest discover -s tests -v
```

当前基线：**350 项测试全部通过，6 项按环境跳过**。CI 矩阵：

- Ubuntu：Python 3.10 / 3.12 / 3.13
- Windows：Python 3.12
- macOS：Python 3.12

### 新增补丁的检查清单

1. 在 `zcode_patcher.py` 增加 `--<feature>` 参数、`--check` 分支与 `--revert` 分支；
2. 写入前生成 sidecar / 备份，写入后校验 offset 与 integrity；
3. 在 `sync.py` 的 `PATCHES` 注册开关，声明是否属于重打包级；
4. 在 `plugin.json` 增加 `userConfig` 默认值，在 `marketplace.json` 同步描述；
5. 增加至少一个「应用 → 检查 → 还原」的回归测试；
6. 更新 `SKILL.md`、`CHANGELOG.md` 与本 README 的功能表。

### 设计约束

- 纯 Python 标准库；不引入 `requests`、`pyinstaller` 等运行时依赖。
- Python 下限 3.10；不要使用 3.11+ 才有的语法或标准库 API。
- 所有补丁必须幂等、可 `--check`、可 `--revert`。
- 任何写盘动作都要能被「完全退出客户端」这一前置条件保护。
- 不要把输出字符串当状态接口；状态至少区分 `on` / `off` / `na` / `stale` / `unknown`。

---

## 维护这个 fork

本仓库采用「下游分支 + 上游同步」的方式维护，详细流程见 [UPSTREAM.md](UPSTREAM.md)。

- **默认分支 `zcodium-toolkit`**：ZCodium 兼容线，所有发布、文档与安装都以它为准。
- **`main`**：fork 早期的历史分支，保留作为合并来源与对照；不再作为安装来源。
- **`upstream/main`**：上游 `c80361619/zcode-toolkit` 的只读镜像，用于评估和吸收上游改动。

同步上游时先建临时分支评估，不要在已发布分支上直接 `rebase`：

```bash
git fetch upstream
git checkout -b sync/upstream-$(date +%Y%m%d) zcodium-toolkit
git merge upstream/main
# 解决冲突 → 跑测试 → 合并回 zcodium-toolkit
python -m unittest discover -s tests -v
python autopilot.py --no-deploy --unattended
```

版本与标识规则：

- `.zcode-plugin/plugin.json` 的 `version` 与 `marketplace.json` 的插件 `version` 必须一致。
- `plugin.json` 的 `name` 固定为 `zcode-tokenspeed`；`marketplace.json` 的 `name` 固定为
  `zcode-toolkit`。不要为了品牌统一改这两个 id。
- 修 bug 递增 patch；新增功能递增 minor；改变配置语义或安装方式时递增 minor 并在
  CHANGELOG 里写明迁移方式。
- 发布前更新 README 徽章、CHANGELOG、两份清单版本，跑完 350 项测试，再打 tag / 发布 Release。
- 保留上游 `LICENSE` 与 `NOTICE.md`；fork 的修改与维护者信息写在 NOTICE 的 fork 章节。

---

## 更新日志

完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。本 fork 最近的版本：

| 版本 | 内容 |
|---|---|
| 0.6.37 | 状态命令按配置目标名检查品牌名，消除误报 |
| 0.6.36 | 无参改名强制写回 `ZCodium`；`--check` 报告当前值 |
| 0.6.35 | 升级判定只认版本号，修好打完补丁后的误报 |
| 0.6.34 | 还原成功后不再持续报「状态未知」 |
| 0.6.33 | 修好改名请求被静默忽略 |
| 0.6.32 | 无参语义修正；`--check` 纯只读 |
| 0.6.31 | 改名走配置直通，不再需要自建看护脚本 |
| 0.6.30 | 命令补齐 10 项，新增 `/zcode-patch-setdisplayname` |
| 0.6.26 | 补上文本替换类补丁的状态识别 |
| 0.6.25 | 并入品牌名替换与窗口 ID 修复 |
| 0.6.24 | 修好每次重启都挂一个空看护 |
| 0.6.23 | 看护单例锁跨副本共享，修好补丁打一半 |
| 0.6.22 | 安装路径缓存与自定义目录扫描，修好退出后不重启 |
| 0.6.21 | ZCodium 发行版支持，修好「装了但完全没反应」 |
| 0.6.20 | 客户端身份识别层：`ZCodium.exe` / `~/.zcodium` |

---

## 致谢与许可

本项目的上游是 [c80361619/zcode-toolkit](https://github.com/c80361619/zcode-toolkit)。
原始代码、补丁设计与文档版权归上游作者所有，按 MIT License 使用。
本 fork 的 ZCodium 兼容修改、稳定性修复与文档由 [bludoge305](https://github.com/bludoge305) 维护。

特别感谢：

- [c80361619](https://github.com/c80361619)：上游项目与完整的补丁框架；
- `ZCodium_username`：品牌名替换与窗口 ID 修复的原始实现（同作者）；
- [HHQ-666](https://github.com/HHQ-666)：模型拉取前端脚本；
- `dsh-reasoning-effort`：思考滑条的视觉设计参考；
- WorkBuddy `input.enhance`：增强提示词的交互参考。

第三方代码与设计参考的完整许可见 [NOTICE.md](NOTICE.md)。
本项目采用 [MIT License](LICENSE)。

### 免责声明

本项目是非官方开源工具，与 ZCodium / ZCode 官方团队无关联。它会在你本机的客户端安装目录中
修改 `app.asar`、`zcode.cjs` 与配置文件；虽然所有补丁都提供检查、备份与还原机制，
但仍建议：

1. 使用前确认你接受本地文件被修改；
2. 保留一份可用的客户端安装包或干净备份；
3. 客户端大版本升级后先跑 `--check` / `--dry-run`；
4. 出现异常时优先使用 `restore_clean.py --latest` 恢复，而不是手工改 asar。

使用本工具即表示你理解并自行承担上述风险。
