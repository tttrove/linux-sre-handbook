# 02-DNS与域名解析

## DNS 解析流程

```
应用 (浏览器)
  → stub resolver (本地)
    → /etc/hosts
    → /etc/resolv.conf (DNS 服务器)
      → 递归查询
        → 根域名服务器
          → TLD 服务器
            → 权威 DNS 服务器
```

## 记录类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **A** | IPv4 地址 | `example.com. A 93.184.216.34` |
| **AAAA** | IPv6 地址 | `example.com. AAAA 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | 别名 | `www.example.com. CNAME example.com.` |
| **MX** | 邮件服务器 | `example.com. MX 10 mail.example.com.` |
| **TXT** | 文本（SPF/DKIM 等） | 域名验证、安全策略 |
| **NS** | 权威 DNS 服务器 | `example.com. NS ns1.example.com.` |
| **SOA** | 授权起始 | 包含序列号、刷新时间等 |
| **SRV** | 服务定位 | 指定特定服务的地址和端口 |
| **PTR** | 反向解析 | IP → 域名 |

## /etc/resolv.conf

```bash
nameserver 8.8.8.8       # DNS 服务器
nameserver 8.8.4.4
search example.com        # 搜索域
options timeout:2 rotate  # 选项
```

## 排查工具

```bash
# 正向解析
dig example.com
dig example.com +short
dig @8.8.8.8 example.com   # 指定 DNS 服务器
dig example.com ANY         # 所有记录类型
dig -x 8.8.8.8              # 反向解析

# 追踪
dig +trace example.com      # 完整追踪

# 交互式工具
nslookup example.com
host example.com

# 检查 DNS 缓存
systemd-resolve --statistics  # systemd-resolved
```

## 常见问题

| 问题 | 排查 |
|------|------|
| DNS 解析慢 | `dig +trace` 追踪，检查递归服务器 |
| 缓存问题 | TTL 过长，修改记录后等待过期 |
| DNSSEC 失败 | 检查签名是否正确配置 |
| 劫持/污染 | 对比不同 DNS 服务器结果 |

## Linux DNS 配置管理

```bash
# systemd-resolved (常见于 Ubuntu)
systemd-resolve --status
resolvectl status

# 传统方式
cat /etc/resolv.conf
cat /etc/nsswitch.conf   # hosts: files dns — 解析顺序
```

## 延伸阅读

- [01-TCPIP协议栈](01-TCPIP协议栈.md) — DNS 的传输层基础
- [03-HTTP与负载均衡](03-HTTP与负载均衡.md) — DNS 负载均衡
- [04-网络排查工具链](04-网络排查工具链.md) — 更多排查工具
