# Fork 维护说明

本文件说明 **ZCodium-toolkit** 与上游 [c80361619/zcode-toolkit](https://github.com/c80361619/zcode-toolkit)
的关系、分支模型、上游同步流程与发布规则。面向维护者，不面向普通安装用户。

普通用户看 [README.md](README.md) 即可。

---

## 1. 这是什么关系

- 上游项目：`c80361619/zcode-toolkit`，MIT License。
- 本仓库：`bludoge305/zcode-toolkit`，GitHub fork。
- 对外品牌：**ZCodium-toolkit**。
- 插件 id：**`zcode-tokenspeed`**（与上游一致）。
- 市场 id：**`zcode-toolkit`**（与上游一致）。
- 默认分支：**`zcodium-toolkit`**，承载 ZCodium 兼容线与本 fork 的发布。

上游 `main` 当前停留在 0.6.20；本 fork 从 0.6.20 的 ZCodium 支持工作开始独立演进，
当前版本 0.6.37。两者不是简单的「上游领先 / fork 落后」关系：本 fork 有自己的
ZCodium 身份识别层、看护修复、改名链路和 10 项补丁命令覆盖。

### 为什么保留插件 id 和市场 id

已安装用户的配置键形如：

```text
plugins.options["zcode-tokenspeed@zcode-toolkit"]
```

如果把插件 id 改成 `zcodium-toolkit` 或把市场名改成 `zcodium-toolkit`：

- 旧配置键失效，用户的 10 个开关会退回默认值；
- 已安装插件可能被当成另一个插件，出现重复安装；
- 文档、命令、缓存目录和排障路径全部要跟着迁移。

因此：**对外品牌可以叫 ZCodium-toolkit，内部标识保持不变。** 这是有意的兼容设计，
不是命名遗漏。

---

## 2. 分支模型

| 分支 | 角色 | 说明 |
|---|---|---|
| `zcodium-toolkit` | **默认分支 / 发布线** | 所有 ZCodium 修复、文档、版本发布都在这里 |
| `main` | 历史基线 | fork 早期的提交线，保留作为对照与合并来源；不再作为安装来源 |
| `upstream/main` | 上游镜像 | 只读 remote，用于评估和吸收上游改动 |
| `sync/*` | 临时同步分支 | 每次同步上游时新建，验证通过后合并回发布线 |

约定：

- 不对已发布的 `zcodium-toolkit` 做 `rebase` 或强制推送。
- 上游同步使用 `merge --no-ff`，保留「哪次合并吸收了什么」的历史。
- 功能分支从 `zcodium-toolkit` 拉出，合并回 `zcodium-toolkit`；不要直接往上推。
- `main` 不删除、不改写。它记录了 fork 早期 0.6.20–0.6.37 的原始提交。

---

## 3. 初次配置 remote

如果本地还没有 `upstream`：

```bash
git remote add upstream https://github.com/c80361619/zcode-toolkit.git
git fetch upstream
```

确认：

```bash
git remote -v
# origin    https://github.com/bludoge305/zcode-toolkit.git
# upstream  https://github.com/c80361619/zcode-toolkit.git
```

---

## 4. 同步上游

不要直接在发布分支上 merge。先建临时分支评估：

```bash
git fetch upstream
git checkout -b sync/upstream-$(date +%Y%m%d) zcodium-toolkit
git merge --no-ff upstream/main
```

冲突处理原则：

1. **ZCodium 身份层不能丢**：`DATA_DIR_NAMES`、`PROCESS_NAMES`、`_is_client_name()`、
   自定义安装目录扫描、安装路径缓存这些是本 fork 的核心，冲突时保留双方语义再合并。
2. **上游的通用改进优先吸收**：DOM 锚点、TPS 指标、增强提示词解析、asar 完整性校验等
   与发行版无关的改动，尽量以上游实现为准，减少后续冲突。
3. **插件 id / 市场 id 不改**：冲突中如果上游/工具建议改名，拒绝。
4. **状态机语义要对齐**：`on` / `off` / `na` / `stale` / `unknown` 的映射不能因为合并
   回退；`display_name` 的空串语义必须保持「强制写回 ZCodium」。
5. **测试必须全绿**：合并后至少跑 `python -m unittest discover -s tests -v`。

验证通过后合并回发布线：

```bash
git checkout zcodium-toolkit
git merge --no-ff sync/upstream-$(date +%Y%m%d)
git push origin zcodium-toolkit
```

如果上游改动与 ZCodium 修复冲突很大，可以先把上游拆成多个小提交逐段合并，
不要一次性解决所有冲突。合并提交信息写清楚吸收了哪些上游版本/提交。

---

## 5. 版本规则

本项目当前处于 `0.x`：

| 变更类型 | 版本递增 | 例子 |
|---|---|---|
| Bug 修复、状态判定、看护稳定性 | patch | 0.6.37 → 0.6.38 |
| 新补丁、新命令、新开关 | minor | 0.6.37 → 0.7.0 |
| 配置语义变化、安装方式变化 | minor + 迁移说明 | 0.6.x → 0.7.0 |
| 仅文档 / README | 不改版本，或随下一次 patch | — |

每次改版本必须同步更新：

1. `.zcode-plugin/plugin.json` 的 `version`；
2. `marketplace.json` 里插件条目的 `version`；
3. `README.md` 的版本徽章；
4. `CHANGELOG.md` 增加对应条目。

两个清单的版本必须一致，否则市场更新与缓存目录会出现不一致。

---

## 6. 发布检查清单

### 发布前

- [ ] `git status` 干净，`zcodium-toolkit` 与 `origin` 同步；
- [ ] 版本号已在两份清单中同步；
- [ ] `CHANGELOG.md` 写好本次变更（用户能看懂的现象 → 原因 → 修复）；
- [ ] `README.md` 的功能表、兼容性、命令示例没有过时；
- [ ] `python -m unittest discover -s tests -v` 全绿；
- [ ] `python autopilot.py --no-deploy --unattended --report ci-report.md --log logs/ci.log` 通过；
- [ ] 在真实客户端上跑过 `--all --check` 和至少一次 `--all --dry-run`；
- [ ] 没有把 `_sync.log`、`_watchdog.*`、`*.bak`、`tap-capture*.jsonl` 等运行产物提交进去。

### 发布

```bash
# 1. 提交
git add README.md CHANGELOG.md UPSTREAM.md \
        .zcode-plugin/plugin.json marketplace.json \
        commands skills tests
git commit -m "release: 0.6.38 ..."

# 2. 打 tag
git tag -a v0.6.38 -m "ZCodium-toolkit 0.6.38"
git push origin zcodium-toolkit
git push origin v0.6.38

# 3. 在 GitHub 创建 Release，正文取 CHANGELOG 对应段落
gh release create v0.6.38 --title "ZCodium-toolkit 0.6.38" --notes-file <(sed -n '/### 0.6.38/,/### 0.6.37/p' CHANGELOG.md)
```

Windows PowerShell 没有进程替换时，先手动把 Release 正文复制到临时文件，
或直接使用 GitHub 网页发布。

### 发布后

- [ ] 在 ZCodium 里刷新市场，确认插件显示新版本；
- [ ] 全新安装路径（cache 为空）走一遍：添加市场 → 安装 → 重启两次 → `/zcode-patch-status`；
- [ ] 升级路径走一遍：旧版本已装 → 市场更新 → 退出重启 → 状态检查；
- [ ] 确认 `doctor.py --where` 报出的版本与清单一致；
- [ ] 如果发布说明里提到迁移，README 的迁移段落同步更新。

---

## 7. 什么改动应该回到上游

本 fork 存在的目的是让 ZCodium 可用，不是把上游整体私有化。以下类型建议同时向上游提 PR：

- 与发行版无关的 bug 修复（asar 完整性、状态机、看护并发、测试）；
- 通用功能改进（TPS 指标、增强提示词解析、模型拉取）；
- 文档修正与更清晰的排障说明。

以下类型通常保留在本 fork：

- `ZCodium.exe` / `~/.zcodium` 身份识别；
- ZCodium 1.0.2 的窗口 ID 缺陷修复；
- ZCodium 品牌名替换的默认语义（无参 = 写回 ZCodium）；
- 面向 ZCodium 安装路径的探测兜底。

向上游提 PR 时，尽量把 ZCodium 特定逻辑做成可选/可探测分支，不要把 `ZCodium` 硬编码
进通用路径；这样上游更容易接受，本 fork 也更容易同步。

---

## 8. 提交与代码约定

- 提交信息使用 conventional commits，例如：
  - `fix: 状态命令按配置的目标名检查品牌名 (0.6.37)`
  - `feat: 无参强制写回 ZCodium (0.6.36)`
  - `docs: 重写 ZCodium-toolkit README`
- 一个提交只做一件事；修复与版本号可以分开提交，发布提交再统一改版本。
- Python 只使用标准库，保持 3.10 兼容。
- 新增补丁必须同时提供 `--check`、`--dry-run`、`--revert` 与回归测试。
- 不提交运行产物、密钥、请求捕获文件；`.gitignore` 已覆盖常见路径。
- 修改 asar 相关逻辑时，优先复用 `_repack_asar` / `_asar_sync_integrity` / sidecar 链路，
  不要另写一套读写。

---

## 9. 归属与许可

- 上游代码版权归 `c80361619`，按 MIT License 使用；`LICENSE` 原文保留。
- 本 fork 的 ZCodium 兼容修改、稳定性修复与文档由 `bludoge305` 维护。
- 第三方组件与设计参考见 [NOTICE.md](NOTICE.md)。
- 发布 Release 时不要移除上游版权声明、LICENSE 或 NOTICE。

---

## 10. 相关文档

- [README.md](README.md)：安装、功能、CLI、排障。
- [CHANGELOG.md](CHANGELOG.md)：版本历史与 fork 修复明细。
- [NOTICE.md](NOTICE.md)：第三方代码与设计参考。
- `skills/zcode-tokenspeed/SKILL.md`：给 AI / 维护者的完整操作手册与内核实测记录。
