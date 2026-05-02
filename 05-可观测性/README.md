# 05-可观测性

## 本节导航

- [01-监控体系设计](01-监控体系设计.md)
- [02-Prometheus生态](02-Prometheus生态.md)
- [03-Grafana看板实践](03-Grafana看板实践.md)
- [04-日志管理](04-日志管理.md)
- [05-分布式追踪](05-分布式追踪.md)
- [06-告警规则设计](06-告警规则设计.md)

## 学习目标

构建完整的可观测性体系：Metrics（指标）、Logging（日志）、Tracing（追踪）三大支柱，掌握 Prometheus + Grafana + Loki + Tempo 技术栈。

## 三大支柱

| 支柱 | 回答的问题 | 工具 |
|------|------------|------|
| **Metrics** | 系统"有多异常" | Prometheus, VictoriaMetrics |
| **Logging** | 发生了什么"事件" | Loki, ELK |
| **Tracing** | 请求"经过了哪里" | Jaeger, Tempo, Zipkin |

## 相关板块

- [04-系统性能](../04-系统性能/README.md) — 性能数据来源
- [11-故障排查方法论](../11-故障排查方法论/README.md) — 基于可观测数据的排查
- [12-高可用与容灾](../12-高可用与容灾/README.md) — 告警与故障联动
