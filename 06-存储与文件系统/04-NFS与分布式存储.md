# 04-NFS与分布式存储

## NFS (Network File System)

### 服务端配置

```bash
# /etc/exports
/data   10.0.0.0/24(rw,sync,no_root_squash,no_subtree_check)

# 选项说明
# rw: 读写
# sync: 同步写入（数据安全）
# no_root_squash: 保留客户端 root 权限
# no_subtree_check: 不检查子目录
```

### 客户端挂载

```bash
mount -t nfs 10.0.0.1:/data /mnt/data
# 推荐挂载选项
mount -t nfs -o hard,intr,rsize=1048576,wsize=1048576,vers=4.2 \
    10.0.0.1:/data /mnt/data
```

### NFS 版本

| 版本 | 特点 |
|------|------|
| NFSv3 | 无状态，需额外 lockd/statd |
| NFSv4 | 有状态，集成锁管理，支持 Kerberos |
| NFSv4.2 | 支持服务端复制、稀疏文件 |

## 分布式文件系统

### GlusterFS
- 无中心节点架构
- 多种卷类型：Distributed / Replicated / Striped / Distributed-Replicated
- 适合文件共享和大容量存储

### Ceph
- 统一存储：对象 (RGW) + 块 (RBD) + 文件 (CephFS)
- CRUSH 算法无中心元数据
- 强一致性
- 适合大规模云存储

## 对象存储

```bash
# MinIO (S3 兼容)
minio server /data

# 使用
mc alias set myminio http://10.0.0.1:9000 accesskey secretkey
mc cp file.txt myminio/bucket/
```

## SRE 关注点

| 维度 | 关键检查 |
|------|----------|
| 可用性 | 冗余配置，避免单点 |
| 延迟 | NFS sync vs async，网络延迟 |
| 容量 | 配额管理，监控使用率 |
| 安全 | Kerberos 认证，加密传输 |
| 备份 | 快照 +异地复制 |

## 延伸阅读

- [[03-文件系统选型]] — 底层文件系统选择
- [[05-数据备份策略]] — 备份方案
