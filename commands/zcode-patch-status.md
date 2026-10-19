---
description: 只读检查 ZCodium / ZCode 客户端各补丁的注入状态（不修改任何文件）
---

加载本插件自带的 `zcode-tokenspeed` 技能（`${CLAUDE_PLUGIN_ROOT}/skills/zcode-tokenspeed/SKILL.md`；若该变量未展开，就按插件安装目录下的同名路径读取），按其「只读核实」步骤对本机 ZCodium / ZCode 安装执行全部检查命令：

```bash
python "<skill目录>/scripts/zcode_patcher.py" --reasoning-config --check   # 3.14+ 档位配置状态
python "<skill目录>/scripts/zcode_patcher.py" --check                       # 内核补丁（3.14+ 会提示"不需要本补丁"）
python "<skill目录>/scripts/zcode_patcher.py" --usage-chart --check
python "<skill目录>/scripts/zcode_patcher.py" --model-width --check
python "<skill目录>/scripts/zcode_patcher.py" --tps-footer --check
python "<skill目录>/scripts/zcode_patcher.py" --thought-slider --check
python "<skill目录>/scripts/zcode_patcher.py" --enhance-prompt --check
python "<skill目录>/scripts/zcode_patcher.py" --model-puller --check
python "<skill目录>/scripts/zcode_patcher.py" --window-id-fix --check       # 窗口 ID 缺陷修复
# 品牌名替换：**必须先读配置里的目标名**，见下方「品牌名替换」一节
```

要求：

- **纯只读**，不要执行任何写入或 `--revert`。
- 先确认目标客户端版本，并按 skill 里的「版本现状」表判断哪些补丁适用（3.14.x 下思考等级内核补丁已过时，档位改走 `optionSpecs`）。
- 本命令覆盖**全部 10 项**（8 项原有 + 品牌名替换 + 窗口 ID 缺陷修复），缺一不可。
- 用中文汇总成一张表：每个补丁「已打 / 未打 / 不适用 / 目标不存在」，失配时给出脚本报告的原因，不要绕过脚本的拒绝结论。

## 品牌名替换（必须按配置检查，不要跑裸 `--check`）

`--display-name` 不带 `--name` 的语义是**目标 ZCodium**，不是「不托管」。所以裸跑
`--display-name --check` 在「配置目标是别的名字」时会报「待写入（当前值：X）」——
那不是真的有待办，只是比较错了目标。

正确做法：

1. 读配置里的目标名：
   `~/.zcode/cli/config.json`（ZCodium 是 `~/.zcodium/cli/config.json`）→
   `plugins.options["zcode-tokenspeed@<实际市场名>"].display_name`
2. 按值选择检查命令：
   - **非空**（如 `"Bludoge"`）→
     `python "<skill目录>/scripts/zcode_patcher.py" --display-name --name "<该值>" --check`
   - **空串 / 不存在** → `python "<skill目录>/scripts/zcode_patcher.py" --display-name --check`
     （空值 = 无参语义，目标固定 `ZCodium`）
3. 结果解读：
   - 「已是目标内容（当前值：X）」→ **已生效**，配置与 asar 一致；
   - 「待写入（当前值：Y）」→ **未生效**，配置要 X、当前是 Y（等下次退出写入）；
   - 「没有可用的 sidecar 备份」不再作为状态判据（无参不再依赖 sidecar）。

其余 9 项的两个特殊状态照旧如实转述，不要当成异常：

- 窗口 ID 修复输出「目标不存在（已修复/无需处理）」→ 当前版本没有该缺陷（上游已修），正常；
- `core_patch` 输出「本补丁不适用」→ 3.14+ 原生档位机制，正常。
