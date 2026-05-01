# 01-Docker核心原理

## Docker 架构

```
Docker Client (CLI)
    ↓ REST API
Docker Daemon (dockerd)
    ├─ containerd (容器运行时管理)
    │   └─ runc (OCI 运行时, 实际创建容器)
    └─ 镜像管理 (pull/push/build)
```

## 隔离机制

Docker 不是虚拟机，使用的是 Linux 内核的隔离特性：

| 机制 | 隔离内容 | 内核特性 |
|------|----------|----------|
| **Namespace** | 进程/网络/挂载/用户隔离 | clone() with flags |
| **Cgroups** | CPU/内存/IO 资源限制 | cgroup v1/v2 |
| **UnionFS** | 镜像分层、写时复制 | overlay2/aufs |
| **Capabilities** | 权限最小化 | capset/capget |

### 7 种 Namespace

| Namespace | 隔离内容 |
|-----------|----------|
| PID | 进程 ID 空间 |
| NET | 网络设备、IP、端口 |
| MNT | 文件系统挂载点 |
| UTS | 主机名和域名 |
| IPC | 进程间通信 (信号量、消息队列) |
| USER | 用户和组 ID 映射 |
| CGROUP | Cgroup 根目录 |

## 存储驱动

```bash
docker info | grep "Storage Driver"
# 推荐: overlay2
# 各驱动对比:
# overlay2 — 主流, 内核 4.0+
# devicemapper — 传统, 需要 direct-lvm
# aufs — 旧版
```

### 镜像分层原理

```
Layer 5: 应用代码 (可写容器层)
Layer 4: COPY app.jar
Layer 3: RUN apt-get install ...
Layer 2: FROM openjdk:11
Layer 1: 基础镜像 (ubuntu/debian/alpine)
```

## 常用命令

```bash
# 镜像
docker images
docker pull nginx:1.25
docker build -t myapp:v1 .
docker tag myapp:v1 registry.example.com/myapp:v1
docker push registry.example.com/myapp:v1

# 容器
docker run -d --name web -p 8080:80 nginx
docker run --rm -it alpine sh
docker logs -f web
docker exec -it web bash
docker inspect web

# 资源限制
docker run --memory=512m --cpus=2 --pids-limit=100 myapp

# 清理
docker system prune -a      # 清理未使用的镜像/容器/网络
docker image prune -a       # 仅清理镜像
```

## 延伸阅读

- [02-Dockerfile最佳实践](02-Dockerfile最佳实践.md)
- [07-容器安全](07-容器安全.md)
- [Cgroups](../07-进程与Service管理/03-Cgroups资源控制.md)
