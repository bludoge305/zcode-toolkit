---
description: 向 ZCodium 客户端注入指定补丁（注入前需完全退出 ZCodium）
---

加载本插件自带的 `zcode-tokenspeed` 技能（`${CLAUDE_PLUGIN_ROOT}/skills/zcode-tokenspeed/SKILL.md`；若该变量未展开，就按插件安装目录下的同名路径读取），按用户点名的功能注入对应补丁：

| 用户说法 | 命令 |
|---|---|
| 用量页去截断 / 打开统计图 | `--usage-chart` |
| 模型弹窗加宽 | `--model-width` |
| TPS 状态栏 / 打开状态栏 | `--tps-footer` |
| 思考强度滑条 | `--thought-slider` |
| 增强提示词 / 润色输入框 | `--enhance-prompt` |
| 模型拉取按钮 | `--model-puller` |
| 改界面显示名 | 见 `/zcode-patch-setdisplayname`（不用本命令） |

要求：

1. **单功能单命令**——只打用户点名的那个，不要捆绑其他补丁；用户没点名就先问清楚要哪个。
2. 注入前先跑对应 `--check` 确认状态，并确认备份机制就绪（首次执行自动生成 `.bak` 与 sidecar）。
3. 重打包级补丁（TPS、滑条、增强提示词、拉取按钮）需要 ZCodium **完全退出**（运行中锁定 `app.asar`）；若用户不方便手动退出，可改用看护脚本 `scripts/apply_after_exit.py` 在退出后自动注入。
4. 把对应的 `--revert` 还原命令一并展示给用户保存，完成后提示重启 ZCodium 验证效果。
5. 脚本报告「锚点不唯一 / 表达式出现次数 ≠1」时，**报告即结论**，不要绕过或手工改写文件。
6. 不确定会改什么时先加 `--dry-run` 预演（不写盘）；脚本会预检 ZCodium / ZCode 进程，运行中会直接拒绝（退出码 2）。
7. **已移除的功能**：思考档位配置（`--reasoning-config`）、思考等级内核补丁（无参执行）、
   窗口 ID 缺陷修复（`--window-id-fix`）已从本 fork 删除，用户点名时说明已不可用。
