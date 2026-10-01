# 领域文档

本页说明工程技能在探索代码库时，应如何使用本仓库的领域文档。

<a id="before-exploring-read-these"></a>
## 探索前先阅读这些资料

- 仓库根目录的 **`CONTEXT.md`**；或者
- 若根目录存在 **`CONTEXT-MAP.md`**，先阅读它——它会指向每个上下文各自的 `CONTEXT.md`。阅读与当前主题相关的每一份。
- **`docs/adr/`**——阅读涉及即将工作区域的 ADR。在多上下文仓库中，也要检查 `src/<context>/docs/adr/` 中限定于该上下文的决策。

如果其中某些文件不存在，**直接继续，不必提示**。不要专门报告缺失，也不要一开始就建议创建。`/domain-modeling` 技能（通过 `/grill-with-docs` 和 `/improve-codebase-architecture` 进入）会在术语或决策真正确定时按需创建这些文档。

<a id="file-structure"></a>
## 文件结构

单上下文仓库（大多数仓库）：

```text
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文仓库（根目录存在 `CONTEXT-MAP.md`）：

```text
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← 系统级决策
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← 上下文专属决策
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

<a id="use-the-glossarys-vocabulary"></a>
## 使用词表中的术语

当输出中需要命名领域概念时（例如 Issue 标题、重构提案、假设或测试名称），使用 `CONTEXT.md` 定义的术语。不要改用词表明确避免的同义词。

如果需要的概念尚未出现在词表中，这本身就是一个信号：要么正在创造项目并不使用的语言（需要重新考虑），要么确实存在词表缺口（记录下来，交给 `/domain-modeling`）。

<a id="flag-adr-conflicts"></a>
## 明确指出 ADR 冲突

如果输出与已有 ADR 冲突，应明确指出，而不是默默覆盖原决策：

> _与 ADR-0007（事件溯源订单）冲突——但值得重新讨论，因为……_
