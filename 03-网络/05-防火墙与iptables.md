# 05-防火墙与iptables

## Netfilter 架构

iptables 是用户态工具，操作内核的 Netfilter 框架：

```
数据包 → PREROUTING → INPUT → 本地进程
            ↓                    ↑
        FORWARD (路由转发)
            ↓                    ↓
数据包 → POSTROUTING → OUTPUT ← 本地进程
```

## iptables 四表五链

| 表 (Table) | 用途 |
|-------------|------|
| **filter** | 默认表，包过滤 |
| **nat** | 网络地址转换 |
| **mangle** | 包修改 (TOS/TTL) |
| **raw** | 连接跟踪例外 |

| 链 (Chain) | 触发时机 |
|-------------|----------|
| PREROUTING | 进入网络栈之前 |
| INPUT | 发往本地进程 |
| FORWARD | 经过本机转发 |
| OUTPUT | 从本地进程发出 |
| POSTROUTING | 离开网络栈之前 |

## 常用命令

```bash
# 查看规则
iptables -L -n -v                # 列出规则（数字格式，详细）
iptables -L -n --line-numbers    # 带行号

# 添加规则
iptables -A INPUT -p tcp --dport 22 -j ACCEPT     # 追加
iptables -I INPUT 1 -p tcp --dport 80 -j ACCEPT    # 插入到第 1 行

# 删除规则
iptables -D INPUT 3                                 # 按行号删除
iptables -D INPUT -p tcp --dport 22 -j ACCEPT        # 按内容删除

# 策略设置
iptables -P INPUT DROP                               # 默认丢弃
iptables -P FORWARD DROP

# 保存 / 恢复
iptables-save > /etc/iptables/rules.v4
iptables-restore < /etc/iptables/rules.v4
```

## SRE 实践规则

```bash
# 允许本地回环
iptables -A INPUT -i lo -j ACCEPT

# 允许已建立的连接
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 允许 SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 限速防暴力破解
iptables -A INPUT -p tcp --dport 22 -m recent --set
iptables -A INPUT -p tcp --dport 22 -m recent --update --seconds 60 --hitcount 5 -j DROP

# 默认拒绝
iptables -P INPUT DROP
```

## nftables (iptables 继任者)

```bash
nft list ruleset
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0\; }
nft add rule inet filter input tcp dport 22 accept
```

## firewalld / ufw 上层工具

```bash
# firewalld (RHEL系)
firewall-cmd --list-all
firewall-cmd --add-port=8080/tcp --permanent

# ufw (Ubuntu)
ufw status verbose
ufw allow 22/tcp
```

## 排查清单

- 规则顺序：iptables 按序匹配，第一条命中即停止
- 默认策略：`iptables -L -n | head`
- 连接跟踪表满：`cat /proc/net/nf_conntrack | wc -l`
- docker/ufw 冲突：Docker 直接操作 iptables

## 延伸阅读

- [[04-网络排查工具链]]
- [[../08-安全加固/_索引|08-安全加固]]
