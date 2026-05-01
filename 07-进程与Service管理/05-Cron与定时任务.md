# 05-Cron与定时任务

## Cron 基础

### crontab 格式

```
分钟 小时 日 月 星期 命令
*    *    *  *   *   command

# 特殊字符
*    任意值
,    列举 (1,3,5)
-    范围 (1-5)
/    步进 (*/5 = 每5)
```

### 示例

```bash
# 每天凌晨 2 点执行备份
0 2 * * * /opt/scripts/backup.sh

# 每 5 分钟检查服务
*/5 * * * * /opt/scripts/healthcheck.sh

# 每周一 9 点发送报告
0 9 * * 1 /opt/scripts/report.sh
```

## crontab 管理

```bash
crontab -l              # 列出当前用户任务
crontab -e              # 编辑
crontab -u user -l      # 查看指定用户任务

# 系统级配置
cat /etc/crontab
ls /etc/cron.d/         # 系统任务
ls /etc/cron.daily/      # 每天执行的脚本
ls /etc/cron.hourly/     # 每小时
```

## systemd Timer (现代替代)

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Backup Service

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup.sh

# /etc/systemd/system/backup.timer
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=daily         # 或 Mon *-*-* 02:00:00
Persistent=true          # 错过时间点后立即补跑
RandomizedDelaySec=300   # 随机延迟避免惊群

[Install]
WantedBy=timers.target
```

```bash
systemctl enable backup.timer
systemctl start backup.timer
systemctl list-timers
```

## Cron vs systemd Timer

| 特性 | Cron | systemd Timer |
|------|------|---------------|
| 日志 | syslog | journalctl |
| 随机延迟 | 需 shell 实现 | 内置 |
| 依赖管理 | 无 | 可以 After/Requires |
| 资源控制 | 无 | Cgroups |
| 错过执行 | 不补 | Persistent 可补 |
| 环境变量 | 继承 cron 环境 | 独立配置 |

## SRE 最佳实践

1. **日志重定向** — cron 输出重定向到文件或 syslog
2. **锁机制** — 防止重叠执行：`flock -n /tmp/backup.lock ...`
3. **超时控制** — 防止任务卡死：`timeout 3600 your_script`
4. **错误告警** — 关键任务失败后通知
5. **时区明确** — crontab 使用系统时区

```bash
# 带锁和超时的 cron 条目
*/10 * * * * flock -n /tmp/task.lock timeout 300 /opt/scripts/task.sh
```

## 延伸阅读

- [01-systemd深度使用](01-systemd深度使用.md) — systemd Timer
- [04-Supervisor与进程守护](04-Supervisor与进程守护.md) — 长驻进程
