# Linux SRE 知识库 - 总索引

> 本知识库面向 Linux SRE（Site Reliability Engineer），覆盖从基础原理到高阶实践的完整体系。使用标准 Markdown 链接构建网状知识结构，同时兼容 Obsidian 双向链接与 GitHub 渲染。

---

## 板块导航

### [01-Linux基础](01-Linux基础/README.md)
操作系统原理、内核架构、进程、内存、文件系统、用户权限、启动流程、包管理。

### [02-Shell与脚本](02-Shell与脚本/README.md)
Bash 语法、文本处理（grep/sed/awk）、命令速查、调试技巧、实战案例。

### [03-网络](03-网络/README.md)
TCP/IP 协议栈、DNS、HTTP、负载均衡、网络排查工具链、iptables、TLS 证书。

### [04-系统性能](04-系统性能/README.md)
CPU、内存、磁盘 IO、网络性能分析，性能工具图谱（top/perf/strace/bpftrace），调优案例。

### [05-可观测性](05-可观测性/README.md)
监控体系设计、Prometheus、Grafana、ELK/Loki 日志、分布式追踪、告警规则。

### [06-存储与文件系统](06-存储与文件系统/README.md)
LVM、RAID、文件系统选型（ext4/xfs/zfs/btrfs）、NFS 分布式存储、备份策略。

### [07-进程与Service管理](07-进程与Service管理/README.md)
systemd、进程调度、Cgroups、Supervisor、Cron 定时任务。

### [08-安全加固](08-安全加固/README.md)
SSH 安全、SELinux/AppArmor、PAM 认证、审计合规、内核安全、入侵检测。

### [09-容器与编排](09-容器与编排/README.md)
Docker 原理与最佳实践、Kubernetes 架构、核心资源、网络存储、运维实战、容器安全。

### [10-自动化与IaC](10-自动化与IaC/README.md)
Ansible、Terraform、CI/CD 流水线设计、GitOps 实践。

### [11-故障排查方法论](11-故障排查方法论/README.md)
USE/RED 方法论、常见故障模式、应急响应 SOP、事后复盘模板、经典案例库。

### [12-高可用与容灾](12-高可用与容灾/README.md)
负载均衡策略、主从集群、故障转移、灾备恢复、容量规划。

### [13-面试与成长](13-面试与成长/README.md)
SRE 面试题集、场景设计题、学习资源与成长路线。

---

## 使用建议

- **新手入门**：建议从 `01-Linux基础` → `02-Shell与脚本` → `03-网络` 顺序学习
- **日常运维**：重点关注 `04-系统性能`、`05-可观测性`、`11-故障排查方法论`
- **架构设计**：深入 `09-容器与编排`、`12-高可用与容灾`、`10-自动化与IaC`
- **面试准备**：直接跳转 `13-面试与成长`

## SRE 核心原则

1. **服务水平目标 (SLO)** — 定义什么是"够好"
2. **消除琐事 (Toil)** — 自动化重复劳动
3. **故障预算 (Error Budget)** — 平衡稳定性与发布速度
4. **无指责文化 (Blameless)** — 从事后复盘中学习
5. **可观测性驱动** — 一切决策基于数据
