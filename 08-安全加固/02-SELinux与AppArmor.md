# 02-SELinux与AppArmor

## MAC vs DAC

- **DAC (自主访问控制)**：文件所有者决定权限，root 可绕过
- **MAC (强制访问控制)**：系统级策略，root 也受限

## SELinux (RHEL 系默认)

### 三种模式

```bash
getenforce                    # 查看当前模式
setenforce 0                  # 切换为 Permissive (不阻断, 只记录)
setenforce 1                  # 切换为 Enforcing

# /etc/selinux/config
SELINUX=enforcing
```

| 模式 | 行为 |
|------|------|
| Enforcing | 强制执行策略，拒绝违规操作 |
| Permissive | 仅记录违规，不拒绝 (调试用) |
| Disabled | 完全关闭 |

### 核心概念

- **主体 (Subject)**：进程
- **客体 (Object)**：文件、端口、设备等
- **类型 (Type)**：`_t` 后缀，如 `httpd_t`, `httpd_sys_content_t`
- **域转换 (Domain Transition)**：进程从一个域切换到另一个域

### 常用命令

```bash
# 查看上下文
ls -Z /var/www/html/
ps -eZ | grep httpd

# 修改文件上下文
chcon -t httpd_sys_content_t /var/www/html/index.html
restorecon -v /var/www/html/index.html  # 恢复默认

# 布尔值开关
getsebool -a | grep httpd
setsebool -P httpd_can_network_connect on  # 持久化

# 审计日志排查
ausearch -m avc -ts recent
# 或
journalctl -t setroubleshoot

# 生成策略模块
audit2allow -a -M mypolicy
semodule -i mypolicy.pp
```

## AppArmor (Ubuntu/Debian 默认)

```bash
# 查看状态
aa-status

# 模式切换
aa-complain /path/to/profile    # 仅记录 (类似 permissive)
aa-enforce /path/to/profile     # 强制执行

# 生成 profile
aa-autodep /usr/sbin/nginx
aa-genprof /usr/sbin/nginx      # 交互式生成
```

## SRE 实践建议

- **不要直接禁用** — 先用 Permissive/complain 模式调试
- **读懂审计日志** — SELinux AVC / AppArmor DENIED 是常见故障源
- **非标准路径** — 应用数据放非标准路径时别忘了设 context
- **Docker/K8s** — 容器安全也依赖 SELinux/AppArmor

## 延伸阅读

- [01-SSH安全配置.md](01-SSH安全配置.md)
- [05-内核安全参数.md](05-内核安全参数.md)
- [../09-容器与编排/07-容器安全.md](../09-容器与编排/07-容器安全.md)
