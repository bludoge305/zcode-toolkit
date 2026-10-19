---
description: 设置 ZCodium 界面左下角显示的名称（不带参数则保持 ZCodium 原样）
---

加载本插件自带的 `zcode-tokenspeed` 技能（`${CLAUDE_PLUGIN_ROOT}/skills/zcode-tokenspeed/SKILL.md`；若该变量未展开，就按插件安装目录下的同名路径读取），然后按下述流程修改界面显示名称。

**用法**

| 命令 | 效果 |
|---|---|
| `/zcode-patch-setdisplayname Bludoge` | 把显示名改成 `Bludoge` |
| `/zcode-patch-setdisplayname` | **保持 `ZCodium` 原样**（不写入任何内容） |

---

## 最短路径（默认走这条，别绕远）

名字存进**插件配置**即可，剩下的交给现有的 `sync.py` → `apply_after_exit.py` 链路，
**不要自己写看护脚本、不要手动排期**。

### 第 1 步：只读确认（一条命令）

```bash
python "<skill目录>/scripts/zcode_patcher.py" --display-name --name "<名字>" --check
```

- 输出「已是目标内容」→ 已是该名字，**直接回复用户，结束**。
- 输出「待写入」→ 继续第 2 步。
- 输出「未定位到目标（结构可能已变）」→ 报告即结论，不要手工改 asar。

### 第 2 步：写入配置（一条命令）

用 `doctor.py --where` 拿到**已安装副本**的绝对路径，然后写
`~/.zcode/cli/config.json`（ZCodium 是 `~/.zcodium/cli/config.json`）的
`plugins.options["zcode-tokenspeed@<市场名>"]`：

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

**操作要点**：

- **整份读入 → 只改 `display_name` 这一个键 → 写回**，保留其余键与缩进。
- `plugins` / `options` / 插件 id 那一层不存在时按需创建；**不要动 `enabledPlugins`**。
- 写前先把原文件复制一份 `config.json.bak`。
- 值就是名字本身（字符串），不要再包成 `{"value": ...}`。

### 第 3 步：立即生效（可选，但这是最快路径）

配置写好后，**同步一次**即可让它排进看护队列：

```bash
python "<skill目录>/scripts/sync.py"
```

- ZCode **已完全退出** → `display_name` 会当场写入 app.asar（其余项若已一致则跳过），
  完成后按第 4 步的提示让用户重启。
- ZCode **正在运行** → sync 会打印「ZCode 退出时写入」，并自动拉起看护；
  **告诉用户「已排期，下次完全退出 ZCode 时自动写入并重启」**，不要再说「已完成」。

> 如果用户不想等，告诉他：完全退出 ZCode（托盘右键 → 退出，关窗口不算）后，
> 看护会自动写入并重新拉起客户端。

### 第 4 步：回复用户

一条消息说清三件事：

1. **当前状态**：已写入 / 已排期（下次退出时生效）/ 已是目标名字。
2. **还原命令**（务必给）：
   ```bash
   python "<skill目录>/scripts/zcode_patcher.py" --display-name --revert
   ```
   还原不需要 `--name`，原文存在 sidecar `app.asar.name-patch.json` 里；
   执行前需完全退出 ZCode。
3. **名字限制**：1–40 字符，不能含引号、反引号、反斜杠、换行。

---

## 规则

- **不带参数 = 保持 ZCodium**：不写配置、不排期、不改任何文件，直接回复用户
  「当前保持 ZCodium，如需修改请用 `/zcode-patch-setdisplayname <你的名字>`」。
- **参数校验**（写配置前做）：去首尾空白；长度 1–40；不含 `` ` `` `"` `'` `\` 与换行。
  不合法就直接说明原因，不要写入。
- **不要自己发明命令**：`--display-name` 需要配合 `--name`；单给 `--display-name`
  会打印「未指定目标名，保持原样」并返回成功（空操作）。
- **不要写一次性看护脚本**：配置写入后 `sync.py` 会自动排期，这是既有机制。
- **不要重复启动看护**：`sync.py` 内部有单例锁，重复启动会直接退出，属正常。
- 路径坑：Git Bash 的 `/c/Users/...` 传给原生 python 时会被改写，**统一用 `C:\...` 绝对路径**。
