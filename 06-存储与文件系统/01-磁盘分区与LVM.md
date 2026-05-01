# 01-磁盘分区与LVM

## 块设备层次

```
磁盘 (/dev/sda)
  → 分区 (/dev/sda1, /dev/sda2)
    → LVM PV (物理卷)
      → VG (卷组)
        → LV (逻辑卷)
          → 文件系统 → 挂载点
```

## 分区工具

```bash
# 查看
lsblk                      # 块设备树
fdisk -l                   # 分区表
parted -l                  # GPT 分区表

# MBR vs GPT
# MBR: 最大 2TB, 4 个主分区
# GPT: 最大 9.4ZB, 128 个分区, 有 CRC 校验
```

## LVM (逻辑卷管理)

### 核心概念

| 概念 | 说明 |
|------|------|
| **PV** (Physical Volume) | 物理卷，通常是磁盘分区 |
| **VG** (Volume Group) | 卷组，由一个或多个 PV 组成 |
| **LV** (Logical Volume) | 逻辑卷，从 VG 中分配 |
| **PE** (Physical Extent) | 物理块，VG 的最小分配单元（默认 4MB） |

### 操作流程

```bash
# 创建
pvcreate /dev/sdb1                    # 创建 PV
vgcreate vg_data /dev/sdb1            # 创建 VG
lvcreate -L 100G -n lv_database vg_data  # 创建 LV
mkfs.xfs /dev/vg_data/lv_database     # 格式化
mount /dev/vg_data/lv_database /data  # 挂载

# 扩容 (在线)
vgextend vg_data /dev/sdc1            # 添加 PV 到 VG
lvextend -L +50G /dev/vg_data/lv_database  # 扩展 LV
xfs_growfs /data                      # 扩展文件系统 (XFS)
# 或 resize2fs /data                  # ext4

# 快照
lvcreate -L 10G -s -n snap_db /dev/vg_data/lv_database
lvconvert --merge vg_data/snap_db     # 恢复快照
```

### SRE 关注点

- **VG 空间预留** — VG 至少留 10% 空闲做快照和紧急扩容
- **PE 大小** — 影响最大 LV 数量
- **磁盘替换** — `pvmove` 在线迁移数据到新磁盘
- **监控** — `vgs` / `lvs` 命令检查 VG/LV 状态

## 延伸阅读

- [02-RAID与存储冗余](02-RAID与存储冗余.md)
- [03-文件系统选型](03-文件系统选型.md)
