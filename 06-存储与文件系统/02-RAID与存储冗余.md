# 02-RAID与存储冗余

## RAID 级别对比

| 级别 | 最少磁盘 | 容量利用率 | 读性能 | 写性能 | 容错 | 经典场景 |
|------|----------|------------|--------|--------|------|----------|
| RAID 0 | 2 | 100% | ★★★ | ★★★ | 无 | 临时/缓存 |
| RAID 1 | 2 | 50% | ★★ | ★★ | 1 块 | 系统盘、SSD |
| RAID 5 | 3 | (n-1)/n | ★★ | ★ | 1 块 | 读多写少 |
| RAID 6 | 4 | (n-2)/n | ★★ | ★ | 2 块 | 大容量 HDD |
| RAID 10 | 4 | 50% | ★★★ | ★★ | 每组 1 块 | 数据库、高性能 |

## RAID 选择决策

```
高性能?     → RAID 10 (多数场景推荐)
性价比?     → RAID 5/6 (注意写惩罚)
冗余性?     → RAID 6 (大容量 HDD, 重建时间长)
简单镜像?   → RAID 1 (SSD 系统盘)
```

## mdadm 管理

```bash
# 创建 RAID 1
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sda /dev/sdb

# 查看状态
cat /proc/mdstat
mdadm --detail /dev/md0

# 模拟故障和替换
mdadm --manage /dev/md0 --fail /dev/sda
mdadm --manage /dev/md0 --remove /dev/sda
mdadm --manage /dev/md0 --add /dev/sdc    # 自动重建

# 热备盘
mdadm --create ... --spare-devices=1 /dev/sdc  # 创建时指定
```

## 硬件 RAID vs 软件 RAID

| 特性 | 硬件 RAID | 软件 RAID (mdadm) |
|------|-----------|-------------------|
| 性能 | 高（独立 CPU） | 依赖主机 CPU |
| 成本 | 高 | 免费 |
| 可移植性 | 需同型号卡 | 任意 Linux |
| 维护 | 需要特定工具 | 标准 Linux 工具 |

## 云环境中的冗余

云环境通常不直接使用 RAID：
- **EBS (AWS)**：自带多副本，用 RAID 0 提升性能
- **本地 SSD**：RAID 0 条带化增加 IOPS
- **对象存储**：自动冗余，无需 RAID

## 延伸阅读

- [[01-磁盘分区与LVM]]
- [[../04-系统性能/03-磁盘IO分析|磁盘 IO 分析]]
