# 动作工具（14）

<p class="facts">英文完整契约：把右上角语言切到 English 可看完整契约　逐工具的中文说明见 <a href="../features/">功能总览</a></p>

| 工具 | 一句话 | 参数个数 | 起始版本 |
| --- | --- | :--: | --- |
| `revit_select` | [在 Revit 里选中指定构件（空列表=清除选择）](features/revit_select.md) | 2 | 0.1.0 |
| `revit_show` | [在视图里定位/高亮构件，必要时打开对应视图](features/revit_show.md) | 3 | 0.2.0 |
| `revit_isolate` | [临时隔离显示（reset=true 恢复）](features/revit_isolate.md) | 3 | 0.2.0 |
| `revit_move` | [按模型轴平移构件（mm）](features/revit_move.md) | 6 | 0.1.0 |
| `revit_place_family` | [在指定标高放置已载入的族实例，可绕 Z 旋转](features/revit_place_family.md) | 8 | 0.2.0 |
| `revit_create_wall` | [按两点建直墙（mm，指定标高、墙类型、高度）](features/revit_create_wall.md) | 7 | 0.2.0 |
| `revit_create_floor` | [按闭合轮廓建楼板（至少 3 个顶点，mm）](features/revit_create_floor.md) | 5 | 0.2.0 |
| `revit_set_phase` | [赋创建阶段 / 拆除阶段（空串清除，null 不变）](features/revit_set_phase.md) | 5 | 0.3.0 |
| `revit_merge_phases` | [把一个阶段的引用并入另一个阶段并删除空阶段](features/revit_merge_phases.md) | 4 | 0.3.0 |
| `revit_set_parameter` | [按参数名写值（长度 mm、面积 m²，其余按内部单位）](features/revit_set_parameter.md) | 5 | 0.1.0 |
| `revit_delete` | [删除构件及其依赖](features/revit_delete.md) | 3 | 0.1.0 |
| `revit_reset_element_ids` | [同文档内换 ID：只对无宿主、无依赖的独立构件有效](features/revit_reset_element_ids.md) | 3 | 0.8.0 |
| `revit_rebuild_model_ids` | [整模型换新 ID：把三维视图可选中的构件重建为一份或多份新模型](features/revit_rebuild_model_ids.md) | 10 | 0.8.0 |
| `revit_batch` | [1–50 步动作合并成一次撤销（revit_batch）](features/revit_batch.md) | 3 | 0.2.0 |
