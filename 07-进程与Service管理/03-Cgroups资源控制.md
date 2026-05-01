# 03-Cgroups资源控制

## Cgroups v1 vs v2

| 特性 | Cgroups v1 | Cgroups v2 |
|------|------------|------------|
| 层次结构 | 每控制器独立树 | 统一树 |
| 控制器 | 分别挂载 | 统一管理 |
| 线程模式 | 不支持 | 支持 |
| 压力通知 | 无 | PSI (Pressure Stall Info) |

```bash
# 检查当前版本
mount | grep cgroup
# v1: 多个 tmpfs
# v2: 单一 cgroup2 on /sys/fs/cgroup

# 查看是否使用 v2
stat -fc %T /sys/fs/cgroup
```

## 核心控制器

| 控制器 | 控制对象 | 参数 |
|--------|----------|------|
| **cpu** | CPU 使用份额 | cpu.weight (v2) / cpu.shares (v1) |
| **memory** | 内存使用上限 | memory.max / memory.high |
| **blkio** | IO 带宽 | io.max |
| **pids** | 进程数上限 | pids.max |
| **cpuset** | CPU 核心绑定 | cpuset.cpus |

## 使用 Cgroups

### 通过 systemd (推荐)

```ini
# /etc/systemd/system/myapp.service.d/limits.conf
[Service]
CPUQuota=200%          # 最多使用 2 个 CPU 核
MemoryMax=2G           # 最大内存 2G
MemoryHigh=1.5G        # 软限制，超过后降低优先级
IOReadBandwidthMax=/dev/sda 100M
IOWriteBandwidthMax=/dev/sda 50M
TasksMax=512           # 最大进程数
```

### 手动操作

```bash
# 创建 cgroup
mkdir /sys/fs/cgroup/myapp
# 设置限制
echo "1073741824" > /sys/fs/cgroup/myapp/memory.max  # 1G
echo "200000 1000" > /sys/fs/cgroup/myapp/cpu.max     # CPU 配额
# 将进程移入
echo <PID> > /sys/fs/cgroup/myapp/cgroup.procs
```

## OOM 与内存压力

Cgroups 的内存限制触发自己的 OOM：

```bash
# 查看 cgroup 的 OOM 次数
cat /sys/fs/cgroup/myapp/memory.events | grep oom

# 禁用 OOM Killer (进程会被挂起而不是被杀)
echo 1 > /sys/fs/cgroup/myapp/memory.oom_control
```

## 容器中的 Cgroups

Docker / Kubernetes 通过 Cgroups 实现资源限制：

```bash
docker run --memory=512m --cpus=2 myapp
# 本质: 创建 cgroup 并设置 memory.max 和 cpu.max
```

## 延伸阅读

- [[01-systemd深度使用]] — systemd 集成 Cgroups
- [[../09-容器与编排/01-Docker核心原理|Docker 核心原理]] — 容器隔离机制
- [[../04-系统性能/02-内存性能分析|内存性能分析]] — OOM 排查
