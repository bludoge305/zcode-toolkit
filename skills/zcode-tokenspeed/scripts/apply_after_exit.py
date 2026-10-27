#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ZCode 退出后自动打补丁看护（计划任务 / 插件开关同步调用，勿手动常跑）
轮询等待 ZCode.exe 全部退出 → 按期望状态应用/还原补丁（重打包级需文件未被占用）
→ 重启 ZCode → 记录日志后退出。日志: scripts/_apply_after_exit.log

两种调用方式：
  1) 无参数（本地计划任务）：应用 档位配置 + TPS 状态栏 + 滑条 + 拉取按钮（见 DEFAULT_TASKS）
  2) `--want=<键>=on|off`（插件 sync.py 传入，可多个）：只处理指定开关，off 走 --revert

取消方式: schtasks /Delete /TN ZCodePatchApply /F（并删除本脚本）

退出码约定（与 zcode_patcher.py 一致）：0=成功、1=有项目失败/等待超时、2=预检失败（ZCode 仍在运行）。
"""

import os
import subprocess
import sys
import time
from pathlib import Path

try:                                   # 控制台编码/窗口安全网（见 _console.py 的说明）
    from _console import no_window_kwargs
except ImportError:                    # 被别处 import 时脚本目录可能不在 sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _console import no_window_kwargs

HERE = Path(__file__).resolve().parent
LOG = HERE / "_apply_after_exit.log"
# ★ 单例锁与需求清单必须放在**所有插件副本共享**的位置。
# 原先 PID_FILE / WANT_FILE 都挂在 HERE 下，而本脚本在机器上常同时存在于多处：
#   cache\<市场>\<插件>\<版本>\skills\...\scripts\   （客户端实际加载的）
#   <仓库>\skills\...\scripts\                        （开发者本机/手动运行）
# 两份副本各自的 pid 文件互不可见 → 谁都没被拦住 → 两个看护在客户端退出后
# **同时**重打包同一个 app.asar，互相把对方的临时文件顶掉（WinError 5），
# 并且抢先的那个把 pid 删掉、后一个误判「客户端已再次运行」而跳过重启。
# 放到数据目录（与发行版无关的那个）后，全局只有一个看护能进入处理阶段。
def _shared_state_dir() -> Path:
    """跨副本共享的看护状态目录（优先客户端真实在用的数据目录）。"""
    home = Path.home()
    for name in (".zcode", ".zcodium"):
        d = home / name
        if (d / "v2").is_dir() or (d / "cli").is_dir():
            return d
    return home / ".zcode"


SHARED_DIR = _shared_state_dir()
PID_FILE = SHARED_DIR / "_watchdog.pid"
WANT_FILE = SHARED_DIR / "_watchdog.want"
POLL_SEC = 3
MAX_WAIT_SEC = 24 * 3600
PYTHON = sys.executable or "python"
#: 子进程超时（秒）。看护是**无人值守**运行的，一旦某个子进程挂死就再也没有人
#: 会来收拾 —— 表现为「明明退出了却永远不生效」（与 7.5 节那个故障长得一样）。
#: tasklist 正常 <1s；zcode_patcher 在 311MB asar 上实测 2~3s，给足余量。
TASKLIST_TIMEOUT = 30
PATCH_TIMEOUT = 600


def _import_patcher():
    """导入主脚本模块；sys.path 只在缺失时插入。

    看护轮询循环每 POLL_SEC 秒调一次 zcode_running() → 本函数被反复执行，
    不能每次都 insert（sys.path 会无界增长——24h 上限约 2.9 万个重复项）。
    """
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import zcode_patcher as zp
    return zp


def log(msg: str) -> None:
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def is_pid_alive(pid: int) -> bool:
    """检查指定 PID 进程是否仍在存活运行。"""
    if pid <= 0:
        return False
    if sys.platform == "win32":
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            SYNCHRONIZE = 0x00100000
            h = ctypes.windll.kernel32.OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE, False, pid
            )
            if not h:
                return False
            exit_code = ctypes.c_ulong()
            ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(exit_code))
            ctypes.windll.kernel32.CloseHandle(h)
            return exit_code.value == 259  # STILL_ACTIVE
        except Exception:
            return False
    else:
        try:
            import os
            os.kill(pid, 0)
            return True
        except OSError:
            return False


def zcode_running() -> bool:
    # 复用主脚本 zcode_patcher.zcode_running() 的跨平台检测（Windows: tasklist 检索
    # ZCode.exe；POSIX: pgrep -f ZCode）。看护的判定必须与补丁预检同源，否则会出现
    # 「看护以为退干净了、动手时又被预检拒绝」的永久错位。
    # 历史问题：这里曾直接跑 ["tasklist"] 并检索 b"ZCode.exe" —— macOS/Linux 上没有
    # tasklist，FileNotFoundError 未被捕获（except 只接 TimeoutExpired），看护在第一次
    # 轮询就崩溃；启动方又把 stderr 定向到 DEVNULL，崩溃完全无声，表现为
    # 「等退出 0 次、完成 0 次」、补丁永远写不进去。
    try:
        return _import_patcher().zcode_running()
    except Exception as e:
        log(f"运行检测失败: {type(e).__name__}: {e}，本轮按「仍在运行」处理")
        return True


def _find_exe(res: Path) -> Path | None:
    """从 asar 所在目录（<安装根>/resources）推出各平台的客户端主程序路径。

    Windows 上同时支持原版 ZCode.exe 与 ZCodium 发行版的 ZCodium.exe。
    """
    root = res.parent                       # Windows: 安装根；macOS: Contents
    cands: list[Path] = [root / "ZCode.exe", root / "ZCodium.exe"]   # Windows（两版发行）
    if sys.platform == "darwin":
        cands = [root / "MacOS" / "ZCode", root / "MacOS" / "ZCodium"] + cands
    else:
        cands += [root / "zcode", root / "ZCode", root / "zcodium", root / "ZCodium"]
    for c in cands:
        if c.is_file():
            return c
    return None


def resolve_install() -> tuple[Path | None, Path | None]:
    """复用主脚本的跨平台探测拿到 (asar 目录, 客户端可执行文件)。

    ★ 这里曾是「看护等到退出却不重启」的根因：客户端退出后，运行时进程探测失效；
    ZCodium 没有卸载注册表项、又装在 D:\\Apps 这类非标准目录，常规扫描全部落空，
    于是 resolve_install() 返回 (None, None)，看护只记一行「未找到主程序」就退出了。
    现在主脚本会缓存成功探测到的安装根（_from_cached_install），退出后仍能命中。
    """
    try:
        zp = _import_patcher()
        for cjs in zp.discover():
            res = cjs.parent.parent
            if (res / "app.asar").is_file():
                return res, _find_exe(res)
    except Exception as e:
        log(f"安装探测失败: {type(e).__name__}: {e}")
    return None, None


# 配置键 -> zcode_patcher.py 参数（与 sync.py 的 PATCHES 一一对应，顺序也保持一致）
# 漏一个键的后果：`--want=<键>=on` 会被 parse_wants 当「未知开关」忽略，
# 于是那个开关**开不起来也关不干净**（enhance_prompt 就漏过这一条）。
PATCH_ARGS = {
    "usage_chart": ["--usage-chart"],
    "model_width": ["--model-width"],
    "tps_footer": ["--tps-footer"],
    "thought_slider": ["--thought-slider"],
    "enhance_prompt": ["--enhance-prompt"],
    "model_puller": ["--model-puller"],
    "display_name": ["--display-name"],
}
# 未收到 --want 时的默认动作（本地计划任务用）：全量 7 项补丁按序全部应用
DEFAULT_TASKS = [
    ["--reasoning-config"],
    ["--usage-chart"],
    ["--model-width"],
    ["--tps-footer"],
    ["--thought-slider"],
    ["--enhance-prompt"],
    ["--model-puller"],
]


#: 值语义是「字符串参数」而非纯布尔的开关。
#: display_name 的值就是目标名字（`--want=display_name=Bludoge`），
#: 执行时拼成 `--display-name --name Bludoge`。
STRING_KEYS = {"display_name"}


def _parse_want_value(key: str, raw: str):
    """把 --want 的值归一：字符串型开关返回名字，其余返回 bool（off→False）。"""
    v = raw.strip()
    if key in STRING_KEYS:
        if v.lower() in ("off", "false", "0", "no", ""):
            return False
        if v.lower() in ("on", "true", "1", "yes"):
            return True
        return v                      # 名字原样返回
    return v.lower() not in ("off", "false", "0", "no", "")


def _task_args(key: str, value) -> list[str]:
    """把开关值翻译成 zcode_patcher 的参数。"""
    base = PATCH_ARGS[key]
    # 布尔 true 不携带名字（老配置/未迁移的情形），避免把 "True" 当名字写上界面
    if key in STRING_KEYS and isinstance(value, str) and value:
        return [*base, "--name", value]
    return list(base)


def _save_wants(argv: list[str]) -> None:
    """把传入的 --want 参数与已存的合并并写入 WANT_FILE。"""
    wants_dict = {}
    if WANT_FILE.is_file():
        try:
            import json
            wants_dict = json.loads(WANT_FILE.read_text(encoding="utf-8"))
        except Exception:
            wants_dict = {}
    for a in argv:
        if a.startswith("--want="):
            key, _, val = a[len("--want="):].partition("=")
            key = key.strip()
            if key in PATCH_ARGS:
                wants_dict[key] = _parse_want_value(key, val)
    if wants_dict:
        try:
            import json
            WANT_FILE.write_text(json.dumps(wants_dict, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass
    elif WANT_FILE.is_file():
        try:
            WANT_FILE.unlink(missing_ok=True)
        except Exception:
            pass


def parse_wants(argv: list[str]):
    """解析 sync.py 传入的 --want=<key>=on|off 或 WANT_FILE。
    返回 [(args, revert), ...]；没有任何 --want 输入时返回 None（走 DEFAULT_TASKS）。"""
    has_explicit_input = any(a.startswith("--want=") for a in argv) or WANT_FILE.is_file()
    merged_wants = {}
    if WANT_FILE.is_file():
        try:
            import json
            merged_wants = json.loads(WANT_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    for a in argv:
        if a.startswith("--want="):
            key, _, val = a[len("--want="):].partition("=")
            key = key.strip()
            if key in PATCH_ARGS:
                merged_wants[key] = _parse_want_value(key, val)

    if not has_explicit_input and not merged_wants:
        return None
    tasks = []
    for key, value in merged_wants.items():
        enabled = bool(value)
        if key in STRING_KEYS:
            # 字符串型开关（display_name）：空值 = 无参语义 = **写回 ZCodium**，
            # 所以无论值有没有，都是「应用」而不是 revert。revert 仅用于精确撤销 sidecar。
            tasks.append((_task_args(key, value), False))
            continue
        tasks.append((_task_args(key, value), not enabled))
    return tasks


def batch_tasks(tasks: list[tuple[list[str], bool]]) -> list[tuple[list[str], bool]]:
    """将同方向（revert 或 apply）的补丁参数合并为批量调用，避免多次解包/重打包 asar。

    规则：
      1. 先执行 revert（还原关闭的项），再执行 apply（应用开启的项）；
      2. 针对同一方向：
         - 拥有具体命令行参数的补丁（如 --tps-footer, --enhance-prompt 等）合并为单次批量调用，
           参数保持既有顺序并去重。
    """
    batched = []
    for target_revert in (True, False):
        subset = [args for args, rev in tasks if rev == target_revert]
        if not subset:
            continue
        merged_args = []
        for args in subset:
            for a in args:
                if a not in merged_args:
                    merged_args.append(a)
        if merged_args:
            batched.append((merged_args, target_revert))
    return batched


def _cleanup_singletons(cur_pid: int, keep_wants: bool = False) -> None:
    """清理单例状态。

    keep_wants=True 时**保留 WANT_FILE**：用于「部分补丁失败」的收尾——
    把失败项留在需求清单里，下次同步/退出时看护会继续尝试，而不是把待办直接吞掉。
    （2026-10-28 实测：升级到 1.17.2 后 enhance_prompt 因杀软占用失败，want 被清空，
      结果那一项就此丢失，直到用户下次手动跑 sync 才补回来。）
    """
    try:
        if PID_FILE.is_file() and PID_FILE.read_text(encoding="utf-8").strip() == str(cur_pid):
            PID_FILE.unlink(missing_ok=True)
        if not keep_wants:
            WANT_FILE.unlink(missing_ok=True)
    except Exception:
        pass


def main() -> int:
    import os
    cur_pid = os.getpid()
    if PID_FILE.is_file():
        try:
            old_pid = int(PID_FILE.read_text(encoding="utf-8").strip())
            if old_pid != cur_pid and is_pid_alive(old_pid):
                log(f"已有活跃看护运行中 (PID {old_pid})，已登记最新需求，本实例退出")
                _save_wants(sys.argv[1:])
                return 0
        except Exception:
            pass
    try:
        PID_FILE.write_text(str(cur_pid), encoding="utf-8")
    except Exception:
        pass
    _save_wants(sys.argv[1:])

    # 预检：如果明确指定了需求但过滤后无待办任务，直接退出
    early_tasks = parse_wants(sys.argv[1:])
    if early_tasks is not None and not early_tasks:
        log("没有待应用的补丁任务，看护退出，不进行等待与重启")
        _cleanup_singletons(cur_pid)
        return 0

    log(f"看护启动，等待 ZCode 退出 (PID {cur_pid})…")
    waited = 0
    while zcode_running():
        time.sleep(POLL_SEC)
        waited += POLL_SEC
        if waited >= MAX_WAIT_SEC:
            log("等待超时（24h），放弃")
            _cleanup_singletons(cur_pid)
            return 1

    raw_tasks = parse_wants(sys.argv[1:])
    if raw_tasks is None:
        raw_tasks = [(args, False) for args in DEFAULT_TASKS]
    if not raw_tasks:
        log("ZCode 已退出，但检查后无有效补丁任务需要执行，看护完成，不重启 ZCode")
        _cleanup_singletons(cur_pid)
        return 0
    desc = "、".join(("还原 " if rev else "应用 ") + (" ".join(a) or "内核补丁") for a, rev in raw_tasks)
    log(f"ZCode 已退出（等待 {waited}s），开始处理：{desc}")

    tasks = batch_tasks(raw_tasks)
    failed = 0
    for args, revert in tasks:
        cmd = [PYTHON, str(HERE / "zcode_patcher.py"), *args] + (["--revert"] if revert else [])
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=PATCH_TIMEOUT,
                               **no_window_kwargs())
        except subprocess.TimeoutExpired:
            # 超时 = 这一项没做成。继续跑剩下的项（能写一项是一项），最后计入 failed。
            log(f"$ zcode_patcher.py {' '.join(cmd[2:])}  [超时 {PATCH_TIMEOUT}s]")
            failed += 1
            continue
        out = ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8", "replace")
        log(f"$ zcode_patcher.py {' '.join(cmd[2:])}  [exit={r.returncode}]\n{out}".rstrip())
        if r.returncode == 2:
            log("预检未通过（ZCode 在等待期间被重新拉起），本次放弃，不重启")
            _cleanup_singletons(cur_pid)
            return 1
        if r.returncode != 0:
            failed += 1

    res, exe = resolve_install()
    # 有失败项时保留 want：下次退出/同步会继续尝试这些补丁，不让它们凭空消失。
    _cleanup_singletons(cur_pid, keep_wants=(failed > 0))
    if exe is None:
        log("未找到客户端主程序（Windows: ZCode.exe / ZCodium.exe），请手动启动")
        return 1
    log(f"处理完成（失败 {failed} 项），重启客户端")
    # ★ 「检测到已再次运行就跳过重启」是错的：退出期间的看护，客户端**本来就已经不在**；
    #   真正要防的是「处理过程中用户又把客户端打开了」——那种情况下不该再拉一个。
    #   这里改成只在「本轮确实没跑过任何补丁、且客户端已由别人拉起」时才跳过，
    #   避免把自己该做的重启也一并跳过（曾导致「退出后补丁打了一半、客户端没回来」）。
    if zcode_running():
        log("检测到客户端已再次运行（可能由用户或其他实例拉起），跳过重启")
        return 0
    try:
        if os.name == "nt":
            subprocess.Popen([str(exe)], cwd=str(exe.parent),
                             creationflags=0x00000008)   # DETACHED_PROCESS——保持上游原样，Windows 行为零变化
        elif sys.platform == "darwin" and res is not None and res.parent.parent.suffix == ".app":
            # macOS 经 Launch Services 打开 .app 包。注意 creationflags 是 Windows 专属
            # 参数，POSIX 上传入会直接抛 ValueError，所以必须按平台分流。
            subprocess.Popen(["open", str(res.parent.parent)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             **no_window_kwargs())
        else:
            subprocess.Popen([str(exe)], cwd=str(exe.parent), start_new_session=True,
                             **no_window_kwargs())
    except Exception as e:
        log(f"重启 ZCode 失败（请手动启动）: {e}")
        return 1
    log("DONE")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # 看护无人值守：崩溃必须留痕。此前 stderr 被 start_watchdog 定向到 DEVNULL，
        # 崩溃无声 —— 这正是 macOS 上「等退出 0 次」长期没被发现的原因。
        import traceback
        log("看护异常退出:\n" + traceback.format_exc())
        sys.exit(1)
