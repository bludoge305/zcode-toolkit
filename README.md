# zcode-tokenspeed · ZCode 客户端一站式原生增强套件

<p align="left">
  <a href="https://github.com/c80361619/zcode-toolkit/releases"><img src="https://img.shields.io/badge/version-0.6.35-blue.svg?style=flat-square" alt="Version"></a>
  <img src="https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/dependencies-0%20(std%20only)-success.svg?style=flat-square" alt="Dependencies">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=flat-square" alt="Platform">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg?style=flat-square" alt="License"></a>
</p>

为 ZCode 桌面客户端补齐极致原生体验与生产力增强：
- 📊 **实时 TPS 与性能状态栏**：首 Token 延迟、tok/s 生成速度、Token 统计与会话命中率常驻展示。
- 🎚️ **思考强度悬浮滑条**：免去繁琐配置，直接在界面流畅拖拽调节 Reasoning Effort，原生即时生效。
- ✨ **提示词智能增强**：输入框旁一键重写润色草稿；**右键自由选择**润色所用模型，支持一键恢复。
- 📈 **用量图表全量展开**：破除官方 Top 5/6 截断限制，全量展示所有模型的调用趋势与占比。
- 🔍 **模型选择浮窗加宽**：选择框 192px 扩大至 320px，长模型名完整展示不再被省略号截断。
- ⚡ **一键模型同步**：设置页一键获取供应商 `/models` 模型列表，勾选即刻自动建条目并写入。
- 🛡️ **无感自愈看护（0.6.11 新特性）**：自动感知客户端与插件升级，后台单例看护静默守护，**彻底解决“客户端一升级补丁就失效”！**

> **纯 Python 标准库驱动**：零第三方依赖、免编译；改动仅作用于**本地客户端文件**；  
> 全量操作严格幂等，支持状态核查与逐项/全量精确还原。
>
> ⚠️ **声明**：非官方开源套件，与 ZCode 官方团队无关联。第三方声明见 [NOTICE.md](NOTICE.md)。  
> （仓库名 `zcode-toolkit` ≠ 插件名 **`zcode-tokenspeed`**，二者保持独立设计以保障配置兼容性）。

---

## ⚡ 三分钟极速上手（推荐，全程零命令）

适合所有使用 ZCode 桌面端的用户，安装过程**完全无需打开命令行**：

| 步骤 | 操作说明 |
|:---:|---|
| **1. 环境确认** | 确认电脑已安装 **Python 3.10+**（系统自带或环境变量已配置）及 **ZCode 客户端**（实测支持 3.11.2 ~ 3.15.1） |
| **2. 添加市场** | 打开 ZCode **设置 → 插件 → 右上角「创建」→「添加插件市场」**，来源填：<br>`c80361619/zcode-toolkit` |
| **3. 安装插件** | 在「个人」分段找到 **ZCode 原生体验增强**（`ZCode Patcher`），点 **安装**（装好默认启用） |
| **4. 自动激活** | **完全退出并重启 ZCode**（托盘右键退出），在新会话中发任意一条消息，后台看护进程将自动完成注入并在下次启动后展现全部增强功能！ |

> 💡 **全自动开箱即用**：插件清单内所有功能默认全开，无需打开配置页。如需关闭某项，在插件配置页拨成关并保存即可。

---

## 🧩 核心功能矩阵

| 特性 | 功能名称 | 核心效果 | 改动范围 |
|:---:|:---|:---|:---|
| 🛡️ | **升级自动自愈** | 动态监控客户端与插件版本，升级后自动感知并调度看护静默修复 | 状态监控器 |
| 📊 | **实时 TPS 状态栏** | 输入框常驻：本轮指标（首 token / tok/s / out）+ 会话累计，右键自由切换位置 | `app.asar` 注入脚本 |
| 🎚️ | **思考强度滑条** | 工具栏「思考 · 档名」入口，悬浮拖拽条吸附微调，主题自适应，原生链路即时生效 | `app.asar` 注入脚本 |
| ✨ | **提示词增强润色** | 输入框旁「增强提示词」按钮，右键支持按供应商自选润色模型，持久化且免重启 | `app.asar` 注入脚本 + IPC |
| 📈 | **用量图表去截断** | 「设置 → 用量」趋势图与饼图不再被 Top 5 / Top 6 截断，全量展示所有模型 | `app.asar` 渲染层 |
| 🔍 | **模型弹窗加宽** | 模型下拉列表宽度由 192px 扩展至 320px，超长模型名完整展示 | `app.asar` 主 bundle |
| ⚡ | **设置页模型拉取** | 设置页新增「⚡ 自动拉取模型」按钮，自动从供应商同步可用模型并批量写入 | `app.asar` 注入脚本 + IPC |
| 🧠 | **思考档位原生配置** | 为各模型配置 `provider_config.json` 档位（3.14+ 原生 optionSpecs，无需内核改动） | 用户配置 JSON |
| 🏷️ | **品牌名替换** | 把界面显示名的兜底字面量换自定义名字（按表达式上下文定位、跨版本稳定） | `app.asar` 重打包级 |
| 🐞 | **窗口 ID 缺陷修复** | 修 ZCodium 1.0.2 的 `disposeWindow(browserWindowId)` 未定义变量（关窗抛 ReferenceError） | `app.asar` 重打包级 |
| ⚙️ | **思考内核补丁（旧版）** | ≤3.11 旧版内核专用兜底方案（3.14+ 自动识别并跳过，安全无侵入） | `zcode.cjs` |

---

## 🛠️ 故障排查与一键自愈

> 💡 **0.6.11 自愈机制**：客户端升级会覆盖官方原版文件导致补丁失效。本插件在检测到升级后会自动重新排期看护，**通常只需在会话中收到提示后，完全退出并重启一次 ZCode 即可自动恢复！**

若遇到特殊情况（如杀毒软件拦截、网络断开等）导致功能未生效，请按以下方式排查与一键修复：

### 方案 A：客户端内一键修复（推荐，无需打开终端）
在 ZCode 任意对话窗口直接输入内置斜杠命令，AI 助手将自动帮您检测或打补丁：
- 输入 `/zcode-patch-doctor`：一键诊断健康状态与卡点；
- 输入 `/zcode-patch-apply`：一键自动重新应用所有增强补丁。

### 方案 B：全电脑通用单行自愈命令（适配所有电脑，任何路径直接粘贴）
无论您是否克隆过本仓库，也不管您在哪个路径打开终端，**直接复制并运行以下命令**（脚本会自动在系统插件缓存中搜寻并执行自愈，纠正启用状态并自动补齐所有补丁）：

```powershell
# Windows (CMD 或 PowerShell 任意路径直接运行)
python -c "import pathlib,subprocess,sys; p=next(pathlib.Path.home().glob('.zcode/**/doctor.py'),None); subprocess.run([sys.executable,str(p),'--fix']) if p else print('未找到已安装的 ZCode 插件，请先在客户端内安装')"
```

```bash
# macOS / Linux (任意终端直接运行)
python3 -c "import pathlib,subprocess,sys; p=next(pathlib.Path.home().glob('.zcode/**/doctor.py'),None); subprocess.run([sys.executable,str(p),'--fix']) if p else print('未找到已安装的 ZCode 插件，请先在客户端内安装')"
```

---

## 🎯 常用特性使用技巧

### 1. 增强提示词（右键自由指定模型）
- **左键点击**：根据当前选定模型一键润色重写草稿，支持一键「恢复原文」；
- **右键点击**：弹出供应商模型列表，可自由指定轻量、快速或专用模型（如 Claude 3.5 Haiku、GPT-4o-mini）专门用于润色，选择后**持久化保存且立即生效**。

### 2. 思考强度悬浮滑条
- 点击输入框下方工具栏的「思考 · 档位」文字，会弹出平滑拖动条；
- 拖拽至所需强度（关闭 / 低 / 中 / 高）释放即刻生效，原生联动客户端配置。

---

## 🔄 卸载与还原

若您想完全停用增强补丁并恢复官方纯净状态：
1. 打开终端运行全域还原命令：
   ```powershell
   python -c "import pathlib,subprocess,sys; p=next(pathlib.Path.home().glob('.zcode/**/zcode_patcher.py'),None); subprocess.run([sys.executable,str(p),'--all','--revert']) if p else None"
   ```
2. 在 ZCode **设置 → 插件 → 管理已安装** 中，点击本插件的「卸载」即可。

---

## 📚 进阶文档与技术档案

<details>
<summary><b>🛠️ 开发者指南：本地离线安装、纯 CLI 与自动化构建</b></summary>

### 方式 B：本地源码离线安装
适合内网、GitHub 网络受限或本地二次开发的场景：
```bash
git clone https://github.com/c80361619/zcode-toolkit.git
```
在 ZCode「设置 → 插件 → 创建 → 添加插件市场」中选择该仓库目录，校验通过后即可安装。

### 方式 C：纯命令行模式（不装插件）
克隆仓库后，直接通过主脚本打补丁：
```bash
# 只读体检（自动探测 ZCode 安装位置）
python skills/zcode-tokenspeed/scripts/zcode_patcher.py --all --check

# 先完全退出 ZCode，然后一次性注入全部补丁
python skills/zcode-tokenspeed/scripts/zcode_patcher.py --all

# 单独还原某项（例如还原 TPS 状态栏）
python skills/zcode-tokenspeed/scripts/zcode_patcher.py --tps-footer --revert
```

### 方式 D：一键引导脚本（开发者专用）
```bash
python bootstrap.py            # macOS/Linux 使用 python3 bootstrap.py
```
自动执行平台环境校验、标准库检查、语法构建与 280+ 项回归测试。

### 方式 E：全自动流水线
```bash
./run.sh                       # Linux / macOS
run.cmd                        # Windows
```

</details>

<details>
<summary><b>🔬 自动注入机制与 ASAR 安全设计</b></summary>

### 1. 为什么补丁需要退出后写入？
`zcode_patcher.py` 具有严格的运行预检机制：只要系统中存在 `ZCode.exe` 进程便拒绝写盘。这是因为客户端运行时 `app.asar` 文件会被底层文件系统锁定，强行改写会导致文件损坏。因此本套件设计了看护单例（Watchdog）：在会话中记录期望状态，待客户端完全退出的一瞬间原子完成写入并自动重新拉起。

### 2. ASAR 重打包安全性
- **全域 Integrity 校验**：重打包时对所有 entry 的 SHA-256 与 offset 排布进行全局自洽检验，杜绝错位加载失败；
- **跨进程互斥锁**：写入全程施加文件锁，避免多进程并发争抢冲突。

</details>

<details>
<summary><b>📜 历史版本审计与故障排查记录</b></summary>

#### 0.6.16（解决思考档位关闭导致退出无限重启死循环，Issue #5）
- **语义修正为“不托管”**：3.14+ 思考档位配置目标为客户端自带的 `provider_config.json`；当开关关闭时语义明确为“停止托管与同步”，插件不再主动写入，且绝不主动还原该文件，彻底切断“退出还原 → 客户端重启写回 → 再次检测冲突 → 再次看护还原”的无限死循环；
- **看护空任务守卫**：`apply_after_exit.py` 严格过滤 `reasoning_config=off` 任务；若最终无待执行补丁任务，看护直接安全退出，杜绝空任务挂起等待与退出自动重启 ZCode。
- **全平台兼容吸收**：完整吸纳 PR #4 对 macOS 看护链路的跨平台支持与 crashpad 僵尸进程排除。

#### 0.6.35（修好「每次打完补丁都误报客户端升级」）
- **升级判定去掉 asar 大小判据**：原逻辑把 `size` 变化当成「客户端升级」，但本插件自己的
  补丁就会改变 asar 大小（改名改条目长度、注入脚本新增文件，每次重打包后 size 都不同）。
  结果是**打完补丁 → 下次会话启动必然误报「检测到客户端升级至 v1.0.2」**，
  用户被反复提示去退出重启，实际什么都没变；
- 现在只认**版本号**变化。同版本下 asar 大小变化视为「自己的补丁造成的」，不提示。

#### 0.6.34（修好还原成功后持续报「状态未知」）
- **`check_state()` 补上「没有可用的 sidecar 备份」→ `on`**：还原成功后 sidecar 会被清理，
  此时脚本输出「没有可用的 sidecar 备份，跳过」并返回成功——这是**已完成**状态。
  不识别会落到 `unknown`，`run_sync` 每轮都报「未处理: display_name(状态未知)」，
  在 `_sync.log` 里持续刷；
- 至此 `display_name` 的四种输出全部有确定映射：
  「待写入」/「待还原」→ `off`、「已是目标内容」/「没有可用的 sidecar 备份」→ `on`。

#### 0.6.33（修好改名请求被静默忽略）
- **`check_state()` 补上「待写入」→ `off`**：改名模式的输出是「待写入 N 个文件」，
  而它只认「已打 / 未打 / 待还原」。落到 `unknown` 后 `run_sync` 报「状态未知」，
  **补丁永远不会被排期**——表现为「执行了改名命令但毫无反应」。
  0.6.32 的还原模式（「待还原」）已修，这次补上改名方向；
- 测试钉死两个方向的状态映射（待写入 / 待还原 → `off`，已是目标 → `on`）。

#### 0.6.32（无参 = 还原为 ZCodium）
- **语义修正**：`/zcode-patch-setdisplayname` 不带参数时**还原成 `ZCodium`**。
  早期把「未指定名字」当成「保持原样」，导致改过名字后再无参执行毫无变化——
  与用户直觉相反（他期望看到的就是恢复原品牌名）；
- **`process_display_name(name=None)` = 还原**：走 sidecar 里的原始字面量，与 `--revert` 等价；
- **`--check` 只读保证**：还原分支原先没检查 `check_only`，导致「体检」会真的去重打包
  asar（运行中还会报 WinError 5）。现补上拦截，输出「待还原 N 个文件」；
- **`sync.check_state` 识别「待还原」→ `off`**：否则落到 `unknown`，被当成失败而不是
  「等退出后还原」；
- **`run_sync` 空名字走还原分支**：原逻辑在 `want` 为假且 `state=off` 时走「已一致」跳过，
  正好把还原需求吞掉；
- **心跳措辞**：`display_name→关` 改为 `display_name→还原`（前者会被误读成关闭功能）。

#### 0.6.31（改名走配置直通，不再需要自建看护）
- **根因**：`/zcode-patch-setdisplayname` 原先只跑 `--display-name`，而该参数**需要配合
  `--name`**；看护与 sync 的参数表里也都不带名字，于是排期到退出后只剩一句
  「未指定目标名，保持原样」的空操作。用户想改名时只能绕过框架、临时写一个一次性看护脚本，
  流程又长又易错；
- **`display_name` 改为字符串型开关**：值就是目标名字
  （`plugins.options[...].display_name = "Bludoge"`），空串表示「保持 ZCodium 原样」；
  插件配置页也变成可直接填名字的文本框。整条链路（`_coerce` → `resolve_wanted` →
  `patch_args` → `--want=` token → 看护 `_task_args`）都会原样透传这个名字；
- **防护**：布尔 `true` / 空串都不会被当成名字（避免把 `"True"` 写到界面上）；
  空名字按「不托管」处理，**不触发 revert**（否则会撤掉用户已写入的名字）；
- **命令重写**：`/zcode-patch-setdisplayname` 改为三行以内的最短路径——只读确认 →
  写配置 → `sync.py` 自动排期，并明确禁止「自己写看护脚本」。

#### 0.6.30（命令补齐新功能，新增 `/zcode-patch-setdisplayname`）
- **`/zcode-patch-status` 补上遗漏**：原先只检查 8 项，新增的品牌名替换与窗口 ID 修复
  完全没覆盖。现扩充到 **10 项**，并说明这两个补丁的特殊状态（「保持原样」「目标不存在」
  都是正常的非失败状态），不再让用户误以为漏检；
- **新增 `/zcode-patch-setdisplayname <名字>`**：改界面左下角显示名。不带参数 = 保持
  `ZCodium` 原样（不写入任何内容）。命令内置参数校验（1–40 字符、禁引号/反引号/反斜杠/换行）、
  只读预检、运行中自动排期看护、还原命令提示；
- **配套更新**：`/zcode-patch-apply` 补窗口 ID 修复并指向新命令；`/zcode-patch-toggle`
  补两个新开关；SKILL.md 的能力表、开关表与各处「8 项」表述统一改为 10 项。

#### 0.6.26（补上文本替换类补丁的状态识别）
- `sync.check_state()` 新增一条通用识别：文本替换类补丁（品牌名 / 窗口 ID 修复）用
  `[=]` 表达「目标状态已达成」，措辞是「保持原样」「已是目标内容」「目标不存在」，
  都不含「已打」。不识别会落到 `unknown`，而 `run_sync` 对 `unknown` 走失败分支——
  表现为每次同步都误报这两个开关失败。现按 `[=]` + 「失败 0」判定为 `on`。

#### 0.6.25（并入 ZCodium_username 的两个补丁：品牌名替换 + 窗口 ID 修复）
从同作者的 `ZCodium_username` 项目移植，改走本框架的 asar 探测 / 重打包 / 备份指纹 /
sidecar / 还原链路，不再需要独立脚本：
- **品牌名替换 `--display-name --name <名字>`**：把渲染层「显示名兜底」的字面量
  （`displayName?.trim() || username?.trim() || \`ZCodium\``）换成自定义名字。
  按**表达式上下文**定位而非固定偏移，并准备了四级兜底（正序 / 反向顺序 / 品牌名邻近 /
  全包唯一品牌字面量），压缩器重排或拆分表达式也能命中；头像首字母兜底
  （`\`Z\`)[0]?.toUpperCase()`）显式排除。长度变化时自动走整包重打包。
  **未传 `--name` 时不改动任何东西**，因此该开关可默认开启而不擅改品牌名；
- **窗口 ID 缺陷修复 `--window-id-fix`**：把 `disposeWindow(browserWindowId)` 改为
  `disposeWindow(n)`（同作用域内 `n = e.webContents.id`），修掉关窗时的 ReferenceError。
  上游已自行修复的版本会识别为「目标不存在（已修复/无需处理）」，**不报失败**；
- **还原修正**：这两个补丁会改变条目长度，重打包后 asar 总大小必然变化，
  因此 sidecar 还原**不再按 asar 大小做指纹过滤**（否则会出现「有备份却还原不了」），
  改为按路径是否仍存在于当前 header 判断。

#### 0.6.24（修好「每次重启都挂一个空看护」）
- **`reasoning_config` 状态误判**：`sync.check_state()` 只认「无需写入」为已完成，
  而 ZCodium 等不生成 `config.json` 的发行版打印的是「**无需迁移**」（脚本返回成功），
  于是被判成 `off` → 每轮同步都当成待办 → **反复拉起一个只含该项、退出后什么也不做的空看护**。
  现把「无需迁移」也归入 `on`，重启后不再残留空看护。

#### 0.6.23（修好看护多实例互抢：补丁打一半、客户端不重启）
- **单例锁改为跨副本共享**：`_watchdog.pid` / `_watchdog.want` 原先挂在**脚本所在目录**，
  而本插件在机器上常同时存在多份副本（客户端 cache 安装副本 + 仓库/开发副本），
  两份副本的锁互不可见 → 客户端退出后**两个看护同时重打包同一个 app.asar**，
  互相顶掉对方的临时文件（`WinError 5`），并抢先删掉 pid 文件，
  后一个实例因此误判「客户端已再次运行」而**跳过重启** —— 表现为「补丁只打了一半、
  客户端没被拉起来」。现统一落到 `<数据目录>/_watchdog.{pid,want}`，全局只有一个看护能进入处理阶段；
- **重启判定修正**：把「检测到已再次运行就跳过重启」的日志与语义收窄为
  「可能由用户或其他实例拉起」，避免把本该由自己做的那次重启也跳过；
- **状态清理**：旧副本目录下遗留的 `_watchdog.pid` / `_watchdog.want` 不再参与判定。

#### 0.6.22（修好看护「等到退出却不重启客户端」）
- **安装路径持久化缓存**：新增 `_from_cached_install`，客户端成功探测后把安装根写进
  `<数据目录>/zcode_install_path.txt`。此前看护在**客户端退出后**调用 `zcode_patcher.py` 时，
  运行时进程探测已失效，而 ZCodium 既无卸载注册表项、又常装在 `D:\Apps` 这类非标准目录，
  于是报「未找到 app.asar」→ 找不到主程序 → 不重启，表现为「退出后什么也没发生」；
- **自定义安装目录浅扫**：新增 `_from_custom_dirs`，扫描 `C:–H:\Apps`、`Tools`、
  `Program Files` 等常见自定义根（只扫一层、只认精确目录名，不递归全盘）；
- **重启链路加固**：`apply_after_exit.resolve_install()` 依赖上述两条兜底，
  客户端退出后仍能定位 asar 与 `ZCodium.exe`，恢复「写入 → 自动拉起」的闭环。

#### 0.6.21（支持 ZCodium 发行版：修好「装了但完全没反应」）
- **客户端身份识别层**：新增 `DATA_DIR_NAMES = (".zcode", ".zcodium")` 与 `PROCESS_NAMES = ("ZCode.exe", "ZCodium.exe")`，安装探测、运行守卫、数据根解析全部改走统一的 `_is_client_name()`。此前三处都硬编码原版 ZCode 特征，而 `"zcode" in "zcodium"` 恰好不成立，导致三个探测器在 ZCodium 上全部命中 0 个候选目录，脚本直接报「未找到 app.asar」——界面上表现得就像什么都没装；
- **运行守卫补全**：`zcode_running()` 同时识别两个进程名。原先只查 `ZCode.exe` 会让 ZCodium 用户绕过预检、在客户端运行时重打包 asar；
- **注入代码运行时选目录**：四个 IPC handler（模型读写 / 增强润色 / 润色模型保存）不再写死 `~/.zcode/v2`，改为按实际存在的 `~/.zcode` 或 `~/.zcodium` 选择，并把 `setting.json` 的 `dataBaseDir` 一并纳入；
- **档位机制判定收紧**：`detect_reasoning_mechanism()` 改用「有无 `optionSpecs`」判定原生机制，不再依赖 `defaultVariant` 字符串（3.14+ 内核里它仍作为 zod schema 字段存在，会把新内核误判成 `unknown`）；
- **无 config.json 的发行版**：ZCodium 1.0.2 不生成 `config.json`，档位全由 `provider_config.json` 承载。仅在 `.zcodium` 数据根下按「无需迁移」跳过，原版 ZCode 缺该文件仍照常报错；
- **验证**：ZCodium 1.0.2 实测 8 项补丁锚点全部命中（`--all --check` 与 `--all --dry-run` 均 8/8），316 项回归测试全绿。

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

## 许可协议

本项目采用 [MIT License](LICENSE) 开源协议。第三方组件声明见 [NOTICE.md](NOTICE.md)。
