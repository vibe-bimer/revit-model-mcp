# 链接 CAD

`revit_link_cad`

<p class="facts"><span><b>分组</b> CAD 与 MEP</span><span><b>类型</b> 动作</span><span><b>基座与自研的区分</b> 基座（上游）</span><span><b>当前版本是否已有</b> 没有</span></p>

在 Revit 工作站把 DWG 链接或导入平面视图，返回 CAD 图层与范围。

## 参数 {#parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `dry_run` | 否 | False | boolean | 只排练：执行后回滚，返回同样的验证块。 |
| `layers` | 否 | None | any |  |
| `level` | 否 | None | any |  |
| `link` | 否 | True | boolean |  |
| `origin` | 否 | internal | string |  |
| `path` | 是 | — | string |  |
| `units` | 否 | auto | string |  |
| `view` | 否 | None | any | 视图的准确名称或十进制视图 ID。 |

### 通用参数 {#common-parameters}

| 参数 | 必填 | 默认值 | 类型 | 说明 |
| --- | :--: | --- | --- | --- |
| `document` | 否 | None | any | 打开多个模型时，用标题或路径指定目标文档。 |
| `timeout_seconds` | 否 | 600 | integer | 本次调用的等待上限（秒）。 |

## 功能说明（注册表原文） {#behavior}

以下保留工具在注册表中声明的英文原文，作为契约来源。

```text
Link or import a DWG into a plan view on the Revit workstation. Returns CAD layers and extents in mm.
```

---

[返回目录](index.md) · [自研工具的移植状态](fork-tools.md)
