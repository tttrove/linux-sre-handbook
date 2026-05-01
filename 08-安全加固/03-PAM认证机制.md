# 03-PAM认证机制

## PAM 架构

```
应用 (sshd, login, sudo)
    ↓
PAM API (libpam)
    ↓
配置文件 (/etc/pam.d/*)
    ↓
PAM 模块 (.so)
    ↓
后台 (LDAP, MySQL, /etc/shadow, ...)
```

## 配置文件格式

```
type  control  module-path  module-arguments

# /etc/pam.d/sshd 示例
auth    required    pam_env.so
auth    required    pam_unix.so  try_first_pass
account required    pam_unix.so
password requisite  pam_pwquality.so minlen=12
session required    pam_limits.so
```

## 管理类型 (type)

| 类型 | 触发时机 |
|------|----------|
| auth | 用户认证 (密码/密钥) |
| account | 账户状态检查 (过期/锁定) |
| password | 密码更新 |
| session | 会话建立/销毁 |

## 控制标志 (control)

| 标志 | 含义 |
|------|------|
| required | 失败继续执行后续模块，最终仍失败 |
| requisite | 失败立即返回，不执行后续 |
| sufficient | 成功立即返回 (跳过后续模块) |
| optional | 可忽略的模块 |

## 常用模块

### pam_unix — 传统密码认证
```bash
auth required pam_unix.so try_first_pass nullok
```

### pam_tally2 — 登录失败锁定
```bash
auth required pam_tally2.so deny=5 unlock_time=600
```

### pam_pwquality — 密码复杂度
```bash
password requisite pam_pwquality.so \
    minlen=12 \
    dcredit=-1 \    # 至少 1 位数字
    ucredit=-1 \    # 至少 1 位大写
    lcredit=-1 \    # 至少 1 位小写
    ocredit=-1 \    # 至少 1 位特殊字符
    enforce_for_root
```

### pam_limits — 资源限制
```bash
session required pam_limits.so

# /etc/security/limits.conf
*       soft    nofile  65536
*       hard    nofile  65536
*       soft    nproc   4096
```

## 排查技巧

```bash
# 查看认证日志
tail -f /var/log/auth.log        # Debian/Ubuntu
tail -f /var/log/secure          # RHEL/CentOS

# 调试模式 (慎用)
# 在控制标志后加 debug: sufficient debug
```

## 延伸阅读

- [01-SSH安全配置](01-SSH安全配置.md) — SSH 层认证
- [用户与权限](../01-Linux基础/06-用户与权限.md) — 权限基础
