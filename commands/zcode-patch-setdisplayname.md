---
description: 设置 ZCodium 界面左下角显示的名称；不带参数则还原为 ZCodium
---

加载本插件自带的 `zcode-tokenspeed` 技能（`${CLAUDE_PLUGIN_ROOT}/skills/zcode-tokenspeed/SKILL.md`；若该变量未展开，就按插件安装目录下的同名路径读取），然后按下述流程修改界面显示名称。

**用法**

| 命令 | 效果 |
|---|---|
| `/zcode-patch-setdisplayname Bludoge` | 把显示名改成 `Bludoge` |
| `/zcode-patch-setdisplayname` | **还原为 `ZCodium`**（撤掉已改的名字，恢复客户端原样） |

> 无参 = 还原，不是「什么都不做」。用户改过名字后再无参执行，期望看到的就是恢复 ZCodium。

---

## 最短路径（默认走这条，别绕远）

名字存进**插件配置**，剩下的交给现有的 `sync.py` → `apply_after_exit.py` 链路，
**不要自己写看护脚本、不要手动排期**。

### 第 1 步：只读确认（一条命令）

**带名字时**：

```bash
python "<skill目录>/scripts/zcode_patcher.py" --display-name --name "<名字>" --check
```

- 「已是目标内容」→ 已是该名字，**直接回复用户，结束**。
- 「待写入」→ 继续第 2 步。

**不带参数（还原）时**：

```bash
python "<skill目录>/scripts/zcode_patcher.py" --display-name --check
```

- 「待还原 N 个文件」→ 当前是改过的名字，需要还原，继续第 2 步。
- 「没有可用的 sidecar 备份，跳过」→ 从未改过名，已经是 ZCodium，**直接回复用户，结束**。

任一路径出现「未定位到目标（结构可能已变）」→ 报告即结论，不要手工改 asar。

### 第 2 步：写入配置（一条命令）

目标是 `~/.zcode/cli/config.json`（ZCodium 是 `~/.zcodium/cli/config.json`）里的
`plugins.options["zcode-tokenspeed@<市场名>"]`：

**改名**：

```json
{
  "plugins": {
    "options": {
      "zcode-tokenspeed@zcode-toolkit": {
        "display_name": "Bludoge"
      }
    }
  }
}
```

**还原**：把该键设为空串（或直接删掉这个键）：

```json
{
  "plugins": {
    "options": {
      "zcode-tokenspeed@zcode-toolkit": {
        "display_name": ""
      }
    }
  }
}
```

**操作要点**：

- **整份读入 → 只改 `display_name` 这一个键 → 写回**，保留其余键与缩进。
- 值就是名字本身（字符串），不要包成 `{"value": ...}`。
- 写前先把原文件复制一份 `config.json.bak`。
- 还原时**不要**手工删 sidecar：原始品牌名就存在 `app.asar.name-patch.json` 里，
  由脚本自己还原并清理。

### 第 3 步：同步一次，让它排进队列

```bash
python "<skill目录>/scripts/sync.py"
```

- ZCode **已完全退出** → 当场写入 app.asar（改名或还原），完成后按第 4 步提示重启。
- ZCode **正在运行** → sync 会打印「ZCode 退出时写入」，并自动拉起看护；
  告诉用户「已排期，下次完全退出 ZCode 时自动写入并重启」，**不要说「已完成」**。

### 第 4 步：回复用户

一条消息说清三件事：

1. **当前状态**：已改名 / 已还原 / 已排期（下次退出时生效）/ 本来就是 ZCodium。
2. **还原命令**（改名时务必给）：
   ```bash
   python "<skill目录>/scripts/zcode_patcher.py" --display-name --revert
   ```
   等价于无参执行本命令。执行前需完全退出 ZCode。
3. **名字限制**：1–40 字符，不能含引号、反引号、反斜杠、换行。

---

## 规则

- **无参 = 还原为 ZCodium**：清空配置里的 `display_name` 并同步，不要只打印「保持原样」。
- **参数校验**（写配置前做）：去首尾空白；长度 1–40；不含 `` ` `` `"` `'` `\` 与换行。
  不合法就直接说明原因，不要写入。
- **不要自己发明命令**：`--display-name` 不带 `--name` 是**还原**语义，不是空操作。
- **不要写一次性看护脚本**：配置写入后 `sync.py` 会自动排期，这是既有机制。
- **不要重复启动看护**：`sync.py` 内部有单例锁，重复启动会直接退出，属正常。
- 路径坑：Git Bash 的 `/c/Users/...` 传给原生 python 时会被改写，**统一用 `C:\...` 绝对路径**。
