# 01-CPU性能分析

## CPU 核心指标

| 指标 | 含义 | 健康阈值 |
|------|------|----------|
| us (user) | 用户态 CPU | 视业务而定 |
| sy (system) | 内核态 CPU | < 30% |
| ni (nice) | 低优先级 CPU | 视情况 |
| id (idle) | 空闲 | 越高越好 |
| wa (iowait) | 等待 IO | < 10% |
| hi (hardware irq) | 硬中断 | 尽量小 |
| si (software irq) | 软中断 | 尽量小 |
| st (steal) | 虚拟化偷取 | 0% |

## 工具链

### 1. 全局概览

```bash
top           # 实时进程视图（交互式）
htop          # 增强版 top
uptime        # 1/5/15 分钟平均负载
vmstat 1      # CPU + 内存 + IO 总览
mpstat -P ALL 1  # 每个 CPU 核心的详细统计
```

### 2. 进程级分析

```bash
pidstat 1              # 每个进程的 CPU 使用
pidstat -p <PID> 1     # 特定进程
pidstat -w 1           # 上下文切换
pidstat -t -p <PID> 1  # 线程级 CPU
```

### 3. 深度分析

```bash
# perf — CPU 性能剖析
perf top                # 实时热点函数
perf record -p <PID> -g -- sleep 30  # 记录 30 秒
perf report             # 查看报告
perf stat -p <PID>      # 性能计数器

# strace — 系统调用跟踪
strace -c -p <PID>      # 系统调用统计
strace -T -p <PID>      # 显示每次调用耗时

# bpftrace — 动态追踪
bpftrace -e 'kprobe:vfs_read { @[comm] = count(); }'
```

## 上下文切换

```bash
vmstat 1         # cs 列：每秒上下文切换次数
pidstat -w 1     # cswch/s (自愿) + nvcswch/s (非自愿)

# 频繁上下文切换的可能原因：
# 1. 线程数过多
# 2. 锁竞争
# 3. IO 等待频繁唤醒
```

## 中断分析

```bash
cat /proc/interrupts   # 各中断的 CPU 分布
cat /proc/softirqs     # 软中断统计

# 网络中断优化：设置中断亲和性
echo 2 > /proc/irq/<IRQ_NUM>/smp_affinity  # 绑定到 CPU1
```

## CPU 问题决策树

```
CPU 使用率高？
├─ us 高 → 应用计算密集 → perf 找热点
├─ sy 高 → 系统调用过多 → strace -c 分析
├─ wa 高 → IO 等待 → iostat 分析磁盘
├─ si 高 → 软中断多 → 检查网络、网卡队列
└─ st 高 → 宿主机过载 → 检查虚拟化层
```

## 延伸阅读

- [02-内存性能分析.md](02-内存性能分析.md)
- [03-磁盘IO分析.md](03-磁盘IO分析.md)
- [05-性能工具图谱.md](05-性能工具图谱.md)
- [../01-Linux基础/03-进程与线程.md](../01-Linux基础/03-进程与线程.md)
