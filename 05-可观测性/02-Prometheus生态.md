# 02-Prometheus生态

## Prometheus 架构

```
┌──────────┐    scrape     ┌──────────────┐
│ Targets  │←─────────────│  Prometheus   │
│ (exporter│              │   Server      │
│  /app)   │              │               │
└──────────┘              │  - TSDB       │
                          │  - Rules      │
                          │  - Alerting   │
                          └──────┬────────┘
                                 │
                    ┌────────────┴───────────┐
                    │                        │
               ┌────▼─────┐            ┌────▼─────┐
               │ Grafana   │            │Alertmanager│
               │ (Dashboards)│          │ (告警通知) │
               └──────────┘            └──────────┘
```

## 数据模型

```
<metric_name>{<label>=<value>, ...} <value> [<timestamp>]

# 示例:
http_requests_total{method="GET", handler="/api", status="200"} 1234 1714560000
```

### 指标类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **Counter** | 只增不减的计数 | http_requests_total |
| **Gauge** | 可增可减的值 | memory_usage_bytes |
| **Histogram** | 分桶统计(默认累积) | request_duration_seconds |
| **Summary** | 分位数统计 | 类似 Histogram + φ-quantile |

## PromQL 核心语法

```promql
# 基本查询
http_requests_total{status="500"}

# 范围查询
rate(http_requests_total[5m])              # 5 分钟内的每秒速率
irate(http_requests_total[5m])             # 基于最后两个点的瞬时速率

# 聚合
sum(rate(http_requests_total[5m])) by (method)
avg(node_cpu_seconds_total) by (instance)

# 分位数
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# 预测
predict_linear(node_filesystem_free_bytes[1h], 4 * 3600) < 0  # 4小时后磁盘满

# 运算符
rate(errors_total[5m]) / rate(requests_total[5m])   # 错误率
```

## 常用 Exporters

| Exporter | 用途 |
|----------|------|
| node_exporter | 主机指标 (CPU/内存/磁盘/网络) |
| mysqld_exporter | MySQL |
| redis_exporter | Redis |
| blackbox_exporter | HTTP/TCP/DNS 探测 |
| kube-state-metrics | K8s 资源状态 |
| postgres_exporter | PostgreSQL |

## 高可用方案

- **Prometheus HA**：两个实例相同配置独立抓取
- **Thanos / Cortex**：水平扩展、长期存储
- **VictoriaMetrics**：高性能替代（更好的压缩/查询性能）

## 延伸阅读

- [01-监控体系设计.md](01-监控体系设计.md)
- [03-Grafana看板实践.md](03-Grafana看板实践.md)
- [06-告警规则设计.md](06-告警规则设计.md)
