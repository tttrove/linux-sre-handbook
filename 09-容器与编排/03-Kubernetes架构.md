# 03-Kubernetes架构

## 集群架构

```
┌─────────────────── Control Plane ───────────────────┐
│                                                       │
│  etcd ←→ API Server ←→ Scheduler                     │
│               ↕                        ↕              │
│       Controller Manager      Cloud Controller Mgr    │
│                                                       │
└──────────────────────┬──────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───▼─────┐     ┌─────▼───┐      ┌──────▼──────┐
│ Node 1  │     │ Node 2  │      │ Node 3      │
│ kubelet │     │ kubelet │      │ kubelet      │
│ kube-proxy    │ kube-proxy│    │ kube-proxy  │
│ Container R   │ Container │    │ Container R  │
└─────────┘     └──────────┘      └─────────────┘
```

## Control Plane 组件

| 组件 | 职责 | 故障影响 |
|------|------|----------|
| **API Server** | 集群统一入口，REST API | 所有操作不可用 |
| **etcd** | 分布式 KV 存储，集群状态 | 无法读取/写入状态 |
| **Scheduler** | Pod 调度到 Node | 新 Pod 无法调度 |
| **Controller Manager** | 运行控制器 (Deployment/ReplicaSet...) | 期望状态不收敛 |
| **Cloud Controller Mgr** | 云厂商集成 | 云资源 (LB/存储) 异常 |

## Node 组件

| 组件 | 职责 |
|------|------|
| **kubelet** | Node 代理，管理 Pod 生命周期 |
| **kube-proxy** | 网络代理，实现 Service 规则 (iptables/IPVS) |
| **Container Runtime** | 实际运行容器 (containerd/CRI-O) |

## 请求流程

```
kubectl → API Server → 认证/授权/准入 → etcd (写入)
                                ↓
                         Scheduler (watch 新 Pod)
                                ↓
                         kubelet (watch 已调度的 Pod)
                                ↓
                         Container Runtime
```

## 延伸阅读

- [04-K8s核心资源](04-K8s核心资源.md) — 工作负载资源详解
- [05-K8s网络与存储](05-K8s网络与存储.md) — 网络模型
- [06-K8s运维实战](06-K8s运维实战.md) — 日常运维
