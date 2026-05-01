# 03-Grafana看板实践

## Grafana 核心概念

| 概念 | 说明 |
|------|------|
| **Data Source** | 数据源（Prometheus, Loki, MySQL 等） |
| **Dashboard** | 看板，包含多行多面板 |
| **Panel** | 面板，一种图表/表格/文本 |
| **Variable** | 变量，动态切换维度（env, host, service） |
| **Alert** | 图表告警规则 |

## 常用面板类型

| 面板 | 适用场景 | PromQL 配合 |
|------|----------|------------|
| **Time series** | 时序折线图 | rate/counter |
| **Stat** | 单值展示 | 瞬时查询 |
| **Gauge** | 仪表盘 | 百分比指标 |
| **Table** | 列表数据 | 多维度聚合 |
| **Heatmap** | 延迟分布热力图 | histogram |
| **Bar gauge** | 横向仪表盘/排行榜 | topk |
| **Pie chart** | 占比 | sum by |

## RED 看板模板

```
面板布局:
┌─────────────────────────────┐
│  Rate (每秒请求数)          │  ← 折线图, 按 method 分色
├─────────────────────────────┤
│  Errors (错误率 %)          │  ← 折线图, 区分 4xx/5xx
├─────────────────────────────┤
│  Duration (p50/p90/p99)     │  ← 折线图, 三条线
├──────────┬──────────────────┤
│  p99 延迟│  Heatmap 分布    │  ← 左: Stat, 右: Heatmap
│  (大数字) │                 │
├──────────┴──────────────────┤
│  Top N 慢接口               │  ← Table, topk(10, ...)
└─────────────────────────────┘
```

## 变量 (Variables)

```promql
# 数据源变量
label_values(node_uname_info, job)

# 多级联动
# 选 region → 再选 cluster → 再选 instance
label_values(node_uname_info{region="$region"}, cluster)
```

## SLO 看板

```
错误预算消耗图:
- 剩余错误预算: (<SLO> - <当前错误率>) / <SLO>
- 燃尽图: 显示本月错误预算消耗速率
- 告警: 消耗 > 50% 黄色, > 80% 红色

公式:
1 - (sum(rate(errors[30d])) / sum(rate(total[30d])))
```

## 告警规则（Grafana 侧）

Grafana 8+ 内置告警引擎：
- 支持多维度告警（按 label 分组）
- 告警状态：Normal / Pending / Alerting / No Data
- 通知策略：告警分组、静默、抑制

## 延伸阅读

- [[02-Prometheus生态]] — PromQL 语法
- [[06-告警规则设计]] — 告警策略
