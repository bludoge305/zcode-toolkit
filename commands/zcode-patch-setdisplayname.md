---
description: 设置 ZCodium 界面左下角显示的名称（默认保持 ZCodium 原样）
---

加载本插件自带的 `zcode-tokenspeed` 技能（`${CLAUDE_PLUGIN_ROOT}/skills/zcode-tokenspeed/SKILL.md`；若该变量未展开，就按插件安装目录下的同名路径读取），按下述流程修改界面显示名称。

**用法**

| 命令 | 效果 |
|---|---|
| `/zcode-patch-setdisplayname 我的名字` | 把显示名改成「我的名字」 |
| `/zcode-patch-setdisplayname` | **不带参数 = 保持 `ZCodium`**（不修改，等价于不启用该补丁） |

**原理**：替换渲染层里「显示名兜底」的字符串字面量，典型形态是
`e?.displayName?.trim() || e?.username?.trim() || \`ZCodium\``。
脚本按**表达式上下文**定位（不依赖固定偏移与版本），所以客户端升级后仍能命中；
新名字与原名字长度不同时会自动整包重建 asar。头像首字母兜底（`\`Z\`)[0]?.toUpperCase()`）不会被误改。

**流程**

1. **解析参数**：从用户消息里取出名字（`/zcode-patch-setdisplayname <名字>` 的 `<名字>` 部分）。
   - 用户**没给名字** → 视为「保持 ZCodium 原样」，**不要**执行任何写入；回复说明：
     当前显示名已是 `ZCodium`，无需改动；若想改，给出 `/zcode-patch-setdisplayname <你的名字>`。
   - 去掉首尾空白；名字必须是 1–40 个字符、不含引号/反引号/反斜杠/换行
     （这些字符会破坏被替换的 JS 字符串字面量）。不合法时直接告知原因，不要写入。
2. **只读确认现状**（不写盘）：
   ```bash
   python "<skill目录>/scripts/zcode_patcher.py" --display-name --name "<名字>" --check
   ```
   - 输出「已是目标内容」→ 已经是该名字，无需改动，直接回复用户。
   - 输出「待写入」→ 需要写入，继续第 3 步。
   - 输出「未指定目标名」→ 说明 `--name` 没传进去，检查参数拼接。
3. **告知生效条件并执行**：这是重打包级补丁，需要 ZCode **完全退出**。
   - ZCode 正在运行 → `zcode_patcher.py` 会预检拒绝（退出码 2）。此时**不要强写**，
     改为排期看护（`apply_after_exit.py` 会等客户端退出后自动写入并重新拉起），
     并明确告诉用户「已排期，下次完全退出 ZCode 时自动生效」。
   - ZCode 已退出 → 直接执行：
     ```bash
     python "<skill目录>/scripts/zcode_patcher.py" --display-name --name "<名字>"
     ```
4. **展示还原命令**（务必让用户保存）：
   ```bash
   python "<skill目录>/scripts/zcode_patcher.py" --display-name --revert
   ```
   还原不需要 `--name`，sidecar 里存的是原文。
5. **提示重启验证**：完全退出并重启 ZCode，看界面左下角是否显示新名字。

**注意**

- 这是**你本机的个性化改动**，不影响其他用户；插件默认配置里 `display_name` 开关虽为开，
  但不指定名字时不会改动任何内容（保持客户端原品牌名）。
- 脚本报「未定位到目标（结构可能已变）」时，**报告即结论**：说明该客户端版本的显示名表达式
  结构变了（四级兜底都没命中），不要手工改 asar，把脚本输出原样反馈给用户。
- `--check` 与 `--dry-run` 不受客户端运行限制，可随时安全跑。
