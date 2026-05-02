# 03-HTTP与负载均衡

## HTTP 协议基础

### 请求报文结构

```
GET /api/users HTTP/1.1
Host: example.com
User-Agent: curl/7.68.0
Accept: application/json
Authorization: Bearer <token>

(空行)
(可选请求体)
```

### 状态码速查

| 范围 | 含义 | 常见 |
|------|------|------|
| 1xx | 信息 | 101 Switching Protocols |
| 2xx | 成功 | 200 OK, 201 Created, 204 No Content |
| 3xx | 重定向 | 301 永久, 302 临时, 304 Not Modified |
| 4xx | 客户端错误 | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| 5xx | 服务端错误 | 500 Internal Error, 502 Bad Gateway, 503 Unavailable, 504 Gateway Timeout |

### HTTP 版本差异

| 版本 | 特点 |
|------|------|
| HTTP/1.0 | 每次请求新建连接 |
| HTTP/1.1 | 持久连接 (Keep-Alive)、管道化 |
| HTTP/2 | 多路复用、头部压缩、Server Push |
| HTTP/3 | 基于 QUIC (UDP)，0-RTT 握手 |

## HTTPS (TLS)

```
客户端 → ClientHello (支持的加密套件)
服务端 ← ServerHello + 证书
客户端 → 密钥交换 → 对称加密通信
```

### 关键概念
- **证书链**：根证书 → 中间 CA → 域名证书
- **SNI**：一个 IP 绑定多个证书
- **证书类型**：DV (域名验证) / OV (组织验证) / EV (扩展验证)

## 负载均衡 (LB)

### L4 vs L7 负载均衡

| 层级 | 依据 | 工具 |
|------|------|------|
| L4 (传输层) | IP + Port | LVS、Nginx stream、HAProxy tcp |
| L7 (应用层) | HTTP Header/Path/Cookie | Nginx http、HAProxy http、Envoy |

### 负载均衡算法

| 算法 | 说明 | 适用场景 |
|------|------|----------|
| Round Robin | 轮询 | 后端能力相当 |
| Least Connections | 最少连接 | 长连接服务 |
| IP Hash | 按客户端 IP 哈希 | 会话保持 |
| Weighted | 加权 | 后端配置不均 |

### Nginx 反向代理示例

```nginx
upstream backend {
    least_conn;
    server 10.0.1.1:8080 weight=3;
    server 10.0.1.2:8080 weight=1;
    server 10.0.1.3:8080 backup;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 延伸阅读

- [01-TCPIP协议栈.md](01-TCPIP协议栈.md) — HTTP 的传输层基础
- [06-TLS与证书管理.md](06-TLS与证书管理.md) — HTTPS 深入
- [../12-高可用与容灾/01-负载均衡策略.md](../12-高可用与容灾/01-负载均衡策略.md) — 架构级 LB
