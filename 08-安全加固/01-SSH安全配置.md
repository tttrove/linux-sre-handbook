# 01-SSH安全配置

## SSH 服务加固

### /etc/ssh/sshd_config 关键配置

```bash
# 禁用 root 直接登录
PermitRootLogin no

# 仅允许密钥认证
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no

# 限制用户和组
AllowUsers deploy sre_user
AllowGroups ssh-users

# 协议和安全算法
Protocol 2
HostKeyAlgorithms ssh-ed25519
KexAlgorithms curve25519-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com

# 连接限制
MaxAuthTries 3
MaxSessions 10
ClientAliveInterval 300
ClientAliveCountMax 2
LoginGraceTime 30

# 端口 (非标准端口减少自动扫描噪音)
Port 2222
```

## SSH 密钥管理

```bash
# 生成 Ed25519 密钥 (推荐)
ssh-keygen -t ed25519 -C "user@host"

# RSA 备选
ssh-keygen -t rsa -b 4096 -C "user@host"

# 公钥部署
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@remote

# 查看登录尝试
journalctl -u sshd -f
```

## ~/.ssh/authorized_keys 高级选项

```bash
# 限制密钥可用于特定来源 IP
from="10.0.0.0/24" ssh-ed25519 AAAAC3...

# 限制密钥可执行命令
command="/usr/local/bin/backup.sh",no-port-forwarding,no-agent-forwarding ssh-ed25519 AAAAC3...

# 应用场景: 备份专用密钥
```

## fail2ban 防暴力破解

```ini
# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = 2222
maxretry = 5
bantime = 3600
findtime = 600
```

## SSH 跳板机 (Bastion)

```bash
# ~/.ssh/config
Host internal-server
    HostName 10.0.1.100
    User deploy
    ProxyJump bastion.example.com
    IdentityFile ~/.ssh/id_ed25519
```

## 审计与排查

```bash
# 查看当前 SSH 会话
who
ss -tan state established '( dport = :ssh or sport = :ssh )'

# 查看失败登录
grep "Failed password" /var/log/auth.log
journalctl -u sshd | grep "Failed password"

# 检查异常 authorized_keys
find /home -name authorized_keys -exec cat {} \;
```

## 延伸阅读

- [[02-SELinux与AppArmor]] — 强制访问控制
- [[03-PAM认证机制]] — 认证层加固
- [[../03-网络/05-防火墙与iptables|防火墙]] — 网络层防御
