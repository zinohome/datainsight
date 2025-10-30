# 部件寿命图表 SQL 语句和分组条形图配置说明

## 📊 SQL 语句

### 使用 Peewee ORM 的实现

```python
# 位置：callbacks/core_pages_c/dashboard_line_c.py
# 函数：get_health_bar_aggregate_data()

DynamicHealthModel.select(
    DynamicHealthModel.部件,
    fn.MAX(DynamicHealthModel.已耗).alias('max_value'),
    fn.AVG(DynamicHealthModel.已耗).alias('avg_value'),
    fn.MIN(DynamicHealthModel.已耗).alias('min_value')
).where(
    DynamicHealthModel.部件.in_(target_devices)
).group_by(DynamicHealthModel.部件)
```

### 对应的原始 PostgreSQL SQL 语句

```sql
SELECT 
    部件,
    MAX(已耗) as max_value,
    AVG(已耗) as avg_value,
    MIN(已耗) as min_value
FROM public.c_chart_health_equipment
WHERE 部件 IN (
    '冷凝风机累计运行时间-U11',
    '冷凝风机累计运行时间-U22',
    '通风机累计运行时间-U11',
    '通风机累计运行时间-U22',
    '压缩机累计运行时间-U11',
    '压缩机累计运行时间-U22'
)
GROUP BY 部件
ORDER BY 
    CASE 部件
        WHEN '冷凝风机累计运行时间-U11' THEN 1
        WHEN '冷凝风机累计运行时间-U22' THEN 2
        WHEN '通风机累计运行时间-U11' THEN 3
        WHEN '通风机累计运行时间-U22' THEN 4
        WHEN '压缩机累计运行时间-U11' THEN 5
        WHEN '压缩机累计运行时间-U22' THEN 6
        ELSE 999
    END;
```

### SQL 说明

**表名**: `public.c_chart_health_equipment`

**字段说明**:
- `部件` (VARCHAR): 设备名称（例如："冷凝风机累计运行时间-U11"）
- `已耗` (FLOAT): 已消耗的寿命值（这就是我们要统计的"寿命值"）
- `车号` (VARCHAR): 车号
- `车厢号` (INTEGER) 或 `车厢` (VARCHAR): 车厢标识（根据配置决定）

**查询逻辑**:
1. **筛选条件**: `WHERE 部件 IN (...)` - 只查询配置的6个设备
2. **分组**: `GROUP BY 部件` - 按设备分组
3. **聚合函数**:
   - `MAX(已耗)`: 所有车辆、所有车厢中该设备的最大值
   - `AVG(已耗)`: 所有车辆、所有车厢中该设备的平均值
   - `MIN(已耗)`: 所有车辆、所有车厢中该设备的最小值

**数据范围**: 
- 查询**所有车辆、所有车厢**的数据
- 不限制车号和车厢号
- 只限制设备类型（部件字段）

---

## 🎨 分组条形图配置

### 组件位置

**文件**: `views/core_pages/dashboard_line_charts.py`  
**行号**: 708-732

### 完整配置代码

```python
fact.AntdBar(
    id='l_h_health_bar',
    data=[],  # 初始为空，由回调填充
    xField='device',      # X轴：设备名称
    yField='value',       # Y轴：寿命值（已耗）
    seriesField='type',   # 系列：最高值/平均值/最小值
    isStack=False,        # 分组柱状图（非堆叠）
    isPercent=False,
    # 自定义颜色映射：最高值=黄色，平均值=绿色，最小值=蓝色
    color=['#ffeb3b', '#4caf50', '#2196f3'],  # 黄色、绿色、蓝色
    label={
        'formatter': {'func': '(item) => item.value.toFixed(0)'}
    },
    legend={
        'position': 'top'
    },
    style={
        'height': '300px',
        'width': '100%',
        'border': 'none',
        'border-collapse': 'collapse',
        'border-spacing': '0',
        'backgroundColor': 'transparent'
    },
)
```

### 配置参数详解

| 参数 | 值 | 说明 |
|------|-----|------|
| `id` | `'l_h_health_bar'` | 图表组件唯一标识 |
| `data` | `[]` | 初始数据（空数组），由回调函数 `update_both_tables()` 填充 |
| `xField` | `'device'` | X轴字段：设备名称（例如："冷凝风机-U11"） |
| `yField` | `'value'` | Y轴字段：寿命值（已耗字段的值） |
| `seriesField` | `'type'` | 系列字段：用于分组，值为"最高值"、"平均值"、"最小值" |
| `isStack` | `False` | **关键参数**：设为 `False` 表示分组柱状图（非堆叠） |
| `isPercent` | `False` | 不使用百分比堆叠 |
| `color` | `['#ffeb3b', '#4caf50', '#2196f3']` | 颜色数组：<br>- `#ffeb3b` (黄色) - 最高值<br>- `#4caf50` (绿色) - 平均值<br>- `#2196f3` (蓝色) - 最小值 |
| `label.formatter` | `'(item) => item.value.toFixed(0)'` | 标签格式化函数：显示数值，保留0位小数 |
| `legend.position` | `'top'` | 图例位置：顶部显示 |
| `style.height` | `'300px'` | 图表高度 |
| `style.width` | `'100%'` | 图表宽度（100%） |
| `style.backgroundColor` | `'transparent'` | 背景透明 |

### 数据格式（由回调函数提供）

图表接收的数据格式：

```python
[
    {
        'device': '冷凝风机-U11',      # X轴：设备名称（已简化）
        'type': '最高值',              # 系列：用于分组和颜色映射
        'type_key': 'max',             # 内部排序键
        'value': 14500.0,              # Y轴：寿命值
        'color': '#ffeb3b'             # 颜色（黄色）
    },
    {
        'device': '冷凝风机-U11',
        'type': '平均值',
        'type_key': 'avg',
        'value': 11000.0,
        'color': '#4caf50'             # 绿色
    },
    {
        'device': '冷凝风机-U11',
        'type': '最小值',
        'type_key': 'min',
        'value': 8000.0,
        'color': '#2196f3'             # 蓝色
    },
    # ... 其他设备的数据
]
```

### 图表显示效果

**X轴**: 6个设备名称（按配置顺序）
- 冷凝风机-U11
- 冷凝风机-U22
- 通风机-U11
- 通风机-U22
- 压缩机-U11
- 压缩机-U22

**Y轴**: 寿命值（已耗），数值范围根据数据自动调整

**每个设备显示3个柱状图**（分组显示）:
- 黄色柱：最高值
- 绿色柱：平均值
- 蓝色柱：最小值

**图例**: 顶部显示，标注"最高值"（黄）、"平均值"（绿）、"最小值"（蓝）

---

## 🔄 数据流转过程

```
1. 数据库查询
   ↓
2. get_health_bar_aggregate_data() 函数
   - 执行SQL聚合查询
   - 转换为图表数据格式
   ↓
3. get_health_data() 函数
   - 调用 get_health_bar_aggregate_data()
   - 返回 (new_formatted_health, bar_data)
   ↓
4. update_both_tables() 回调函数
   - 接收 bar_data
   - 更新图表组件的 data 属性
   ↓
5. fact.AntdBar 组件渲染
   - 根据配置渲染分组柱状图
```

---

## ⚙️ 相关配置

### 设备列表配置

**位置**: `configs/base_config.py`

```python
health_bar_devices: List[str] = [
    '冷凝风机累计运行时间-U11',
    '冷凝风机累计运行时间-U22',
    '通风机累计运行时间-U11',
    '通风机累计运行时间-U22',
    '压缩机累计运行时间-U11',
    '压缩机累计运行时间-U22'
]
```

**注意**: 
- 设备名称必须与数据库中的 `部件` 字段值完全匹配
- 显示名称会自动简化（移除"累计运行时间"等字样）

---

## 📝 总结

### SQL 核心逻辑
- **聚合**: 使用 `MAX()`, `AVG()`, `MIN()` 函数
- **分组**: 按 `部件` 字段分组
- **筛选**: 只查询配置的6个设备
- **范围**: 所有车辆、所有车厢的数据

### 图表配置核心
- **类型**: 分组柱状图（`isStack=False`）
- **字段映射**: `xField='device'`, `yField='value'`, `seriesField='type'`
- **颜色方案**: 黄色（最高）、绿色（平均）、蓝色（最小）
- **显示**: 每个设备显示3个柱状图（分组展示）

---

**文档生成时间**: 2024-12-19  
**最后更新**: 根据最新代码自动生成

