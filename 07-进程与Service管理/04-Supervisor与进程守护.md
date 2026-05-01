# 04-Supervisor与进程守护

## Supervisor 概述

Supervisor 是 Python 写的进程管理工具，用于守护非 systemd 场景的长驻进程。

```ini
# /etc/supervisor/conf.d/myapp.conf
[program:myapp]
command=/opt/myapp/bin/myapp --config /etc/myapp.yaml
directory=/opt/myapp
user=myapp
autostart=true
autorestart=true
startretries=3
redirect_stderr=true
stdout_logfile=/var/log/myapp/app.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
environment=ENV="production"
```

## 常用命令

```bash
supervisorctl status                # 查看所有进程
supervisorctl start myapp
supervisorctl stop myapp
supervisorctl restart myapp
supervisorctl reload                # 重载配置
supervisorctl tail -f myapp         # 查看日志
```

## Supervisor vs systemd

| 特性 | Supervisor | systemd |
|------|------------|---------|
| PID 1 | 否 | 是 |
| 依赖管理 | 手动 | 内置 |
| 资源控制 | 无 | Cgroups 原生支持 |
| 定时任务 | 无 | Timer unit |
| Python 应用友好 | ★★★ | ★★ |
| 配置简洁 | ★★★ | ★★ |

**选型建议**：系统级服务用 systemd，Python 应用用 Supervisor，容器内直接用容器的进程管理。

## systemd 管理的替代方案

如果必须用 systemd 但需要进程级控制：

```ini
[Service]
ExecStart=/usr/bin/supervisord -n
ExecStop=/usr/bin/supervisorctl shutdown
```

## 容器中的进程管理

容器内通常不运行 systemd，直接用进程作为 PID 1。需要注意：
- **僵尸进程回收** — 使用 `tini` 或 `docker run --init`
- **信号转发** — PID 1 需要正确转发 SIGTERM

```bash
docker run --init myimage    # 自动注入 tini 作为 PID 1
```

## 延伸阅读

- [01-systemd深度使用](01-systemd深度使用.md) — systemd 方案
- [05-Cron与定时任务](05-Cron与定时任务.md) — 定时任务管理
