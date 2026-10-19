# 第三方组件与许可声明

本项目代码为原创实现。以下部分包含来自第三方的代码或设计参考，按相应许可要求在此集中声明。

## 1. 模型拉取前端脚本（MIT License）

- 文件：`skills/zcode-tokenspeed/scripts/zcode-model-puller.js`
- 同一项目的配置同步逻辑被移植到 `skills/zcode-tokenspeed/scripts/model_pull.py`（命令行版）

```
MIT License

Copyright (c) HHQ-666

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 2. 设计参考（非代码引用）

- 思考强度滑条的视觉规格参考了 `dsh-reasoning-effort` 项目公开的设计语言
  （渐变轨道 / 拖尾光斑 / 拖拽增辉 / 最高档呼吸），**代码为本项目自行实现**。
- 输入框「增强提示词」的交互与提示词要点对齐了 WorkBuddy 的 `input.enhance` 功能，
  提示词模板为本项目自行撰写。

## 3. 上游项目与 fork 归属

- 本仓库是 [`c80361619/zcode-toolkit`](https://github.com/c80361619/zcode-toolkit) 的 fork，
  对外品牌为 **ZCodium-toolkit**。
- 上游原始代码、补丁设计与文档的版权归 `c80361619` 所有，按 MIT License 使用；
  `LICENSE` 原文保留。
- 本 fork 自 0.6.20 起独立维护 ZCodium 兼容线，新增/修改部分由
  [`bludoge305`](https://github.com/bludoge305) 维护，同样按 MIT License 发布。
- 品牌名替换与窗口 ID 修复的原始实现来自同作者的 `ZCodium_username` 项目，
  已按 MIT License 移植并改走本项目的 asar 探测 / 备份 / 还原链路。
