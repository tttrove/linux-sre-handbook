# 01-TCP/IP协议栈

## OSI vs TCP/IP 模型

| OSI 七层 | TCP/IP 四层 | 协议 |
|----------|------------|------|
| 应用层 | 应用层 | HTTP, DNS, SSH, SMTP |
| 表示层 | 应用层 | TLS/SSL |
| 会话层 | 应用层 | - |
| 传输层 | 传输层 | TCP, UDP |
| 网络层 | 网络层 | IP, ICMP |
| 数据链路层 | 网络接口层 | ARP, Ethernet |
| 物理层 | 网络接口层 | 光纤、铜缆 |

## TCP 协议核心

### 三次握手

```
Client                    Server
  |─── SYN (seq=x) ──────→|
  |←─ SYN+ACK (seq=y,ack=x+1)──|
  |─── ACK (ack=y+1) ────→|
```

### 四次挥手

```
Client                    Server
  |─── FIN ──────────────→|
  |←─ ACK ────────────────|
  |←─ FIN ────────────────|
  |─── ACK ──────────────→|
```

### TCP 状态机

- **LISTEN** — 等待连接
- **SYN_SENT / SYN_RECV** — 握手阶段
- **ESTABLISHED** — 正常通信
- **FIN_WAIT / CLOSE_WAIT** — 关闭阶段
- **TIME_WAIT** — 等待 2MSL，确保远端收到最后的 ACK

### TIME_WAIT 问题

高并发短连接场景下 TIME_WAIT 堆积：
```bash
# 查看 TIME_WAIT 数量
ss -tan state time-wait | wc -l

# 内核调优
sysctl net.ipv4.tcp_tw_reuse=1    # 复用 TIME_WAIT 连接
sysctl net.ipv4.tcp_fin_timeout=15 # 减少超时
```

### 拥塞控制算法

| 算法 | 特点 |
|------|------|
| Cubic | Linux 默认，高速高延迟网络友好 |
| BBR | Google 开发，基于带宽和 RTT |

```bash
sysctl net.ipv4.tcp_congestion_control
# 查看可用算法
cat /proc/sys/net/ipv4/tcp_available_congestion_control
```

## UDP 协议

- 无连接，不保证可靠
- 适合实时通信（DNS、VoIP、视频流）
- DNS 默认 UDP 53，大包回退 TCP

## ICMP

- `ping` 和 `traceroute` 的底层协议
- 类型 8 = Echo Request, 类型 0 = Echo Reply
- 类型 3 = Destination Unreachable

## 内核参数（sysctl）速查

```bash
net.core.somaxconn         # listen backlog 最大值
net.ipv4.tcp_max_syn_backlog # SYN 队列长度
net.ipv4.ip_local_port_range  # 本地端口范围
net.core.netdev_max_backlog   # 网络接口接收队列
```

## 延伸阅读

- [02-DNS与域名解析.md](02-DNS与域名解析.md)
- [04-网络排查工具链.md](04-网络排查工具链.md)
- [../04-系统性能/04-网络性能分析.md](../04-系统性能/04-网络性能分析.md)
