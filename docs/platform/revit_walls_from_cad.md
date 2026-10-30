# 从 CAD 建墙

`revit_walls_from_cad`

<p class="facts"><span><b>分组</b> CAD 与 MEP</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>状态</b> 未发布（集成分支）</span><span><b>发布版版本</b> 0.9.0</span><span><b>来源分支</b> <code>integration/upstream-1.0</code></span><span><b>来源提交</b> <code>55d6ea51f5100b73faf6f02621b973642f12b08e</code></span><span><b>发布版有同名工具</b> 没有</span><span><b>本页契约适用于发布版</b> 否</span></p>

桥接洞口、配对平行 CAD 线并在一次撤销内连接基本墙；Revit 拒绝的连接会列出原因。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `cad_id` | 是 | — | integer |  |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `height_mm` | 否 | 3000 | number |  |
| `join` | 否 | True | boolean |  |
| `layers` | 是 | — | array |  |
| `level` | 是 | — | string |  |
| `max_gap_mm` | 否 | 3000 | number |  |
| `max_thickness_mm` | 否 | 700 | number |  |
| `min_length_mm` | 否 | 300 | number |  |
| `min_thickness_mm` | 否 | 80 | number |  |
| `wall_type` | 否 | None | any |  |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `timeout_seconds` | 否 | 600 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Bridge openings, pair parallel CAD lines and join basic walls in one undo entry. Dimensions are mm. Joins Revit rejects are left out and reported as unjoinedEnds with unjoinedReasons; dry_run reports the same join numbers.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
