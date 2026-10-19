---
description: 只读检查 ZCode 客户端各补丁的注入状态（不修改任何文件）
---

加载本插件自带的 `zcode-tokenspeed` 技能（`${CLAUDE_PLUGIN_ROOT}/skills/zcode-tokenspeed/SKILL.md`；若该变量未展开，就按插件安装目录下的同名路径读取），按其「只读核实」步骤对本机 ZCode 安装执行全部检查命令：

```bash
python "<skill目录>/scripts/zcode_patcher.py" --reasoning-config --check   # 3.14+ 档位配置状态
python "<skill目录>/scripts/zcode_patcher.py" --check                       # 内核补丁（3.14+ 会提示"不需要本补丁"）
python "<skill目录>/scripts/zcode_patcher.py" --usage-chart --check
python "<skill目录>/scripts/zcode_patcher.py" --model-width --check
python "<skill目录>/scripts/zcode_patcher.py" --tps-footer --check
python "<skill目录>/scripts/zcode_patcher.py" --thought-slider --check
python "<skill目录>/scripts/zcode_patcher.py" --enhance-prompt --check
python "<skill目录>/scripts/zcode_patcher.py" --model-puller --check
python "<skill目录>/scripts/zcode_patcher.py" --display-name --check        # 品牌名替换
python "<skill目录>/scripts/zcode_patcher.py" --window-id-fix --check       # 窗口 ID 缺陷修复
```

要求：

- **纯只读**，不要执行任何写入或 `--revert`。
- 先确认目标 ZCode 版本，并按 skill 里的「版本现状」表判断哪些补丁适用（3.14.x 下思考等级内核补丁已过时，档位改走 `optionSpecs`）。
- 本命令覆盖**全部 10 项**（8 项原有 + 品牌名替换 + 窗口 ID 缺陷修复），缺一不可；`--all --check` 可一次看全，但逐项命令的结果更便于定位。
- 用中文汇总成一张表：每个补丁「已打 / 未打 / 不适用 / 目标不存在」，失配时给出脚本报告的原因，不要绕过脚本的拒绝结论。
- 两个新补丁的**特殊状态**要如实转述，不要当成异常：
  - 品牌名替换：未指定目标名时输出「未指定目标名（--name），保持原样」——这是正常的「不托管」状态，不是失败。
  - 窗口 ID 修复：输出「目标不存在（已修复/无需处理）」表示当前客户端版本没有该缺陷（上游已修），同样是正常状态。
- 想知道品牌名当前实际改成了什么，可再用 `--display-name --name <待确认的名字>` 跑一次：输出「已是目标内容」说明当前就是该名字；输出待写入说明当前是别的名字。用户只想改名字时，引导他用 `/zcode-patch-setdisplayname <名字>`。
