# 01-systemd深度使用

## systemd 架构

```
systemd (PID 1)
 ├─ systemd-journald   (日志)
 ├─ systemd-logind     (登录管理)
 ├─ systemd-networkd   (网络)
 ├─ systemd-resolved   (DNS)
 ├─ systemd-timesyncd  (时间同步)
 └─ systemd-udevd      (设备管理)
```

## Unit 类型

| 类型 | 后缀 | 说明 |
|------|------|------|
| Service | .service | 服务进程 |
| Socket | .socket | IPC/网络 socket |
| Timer | .timer | 定时器（替代 cron） |
| Target | .target | 组管理（替代运行级别） |
| Mount | .mount | 挂载点 |
| Device | .device | 设备 |

## Service Unit 编写

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target
Requires=network.target

[Service]
Type=simple              # simple/oneshot/forking/notify
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/myapp --config /etc/myapp/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -SIGTERM $MAINPID
Restart=on-failure
RestartSec=5
LimitNOFILE=65536
LimitNPROC=4096
PrivateTmp=true
NoNewPrivileges=true
ReadOnlyPaths=/usr

[Install]
WantedBy=multi-user.target
```

### Service Type 选择

| Type | 说明 |
|------|------|
| simple | 默认，ExecStart 启动即视为就绪 |
| forking | 父进程退出后视为就绪（传统守护进程） |
| oneshot | 执行完 ExecStart 后退出 |
| notify | 进程通过 sd_notify 通知就绪 |
| idle | 等所有作业完成后再启动 |

## 常用管理命令

```bash
systemctl status myapp            # 服务状态
systemctl start/stop/restart myapp
systemctl enable/disable myapp    # 开机启动
systemctl daemon-reload           # 重载 unit 文件
systemctl list-units --state=failed  # 失败的 unit
systemctl list-timers             # 定时器列表

# 日志
journalctl -u myapp -f            # 跟踪日志
journalctl -u myapp --since "1 hour ago"
journalctl -u myapp -p err        # 只看错误
journalctl --disk-usage           # 日志磁盘占用
```

## 资源限制

在 unit 文件中配置：

```ini
[Service]
MemoryMax=2G
CPUQuota=200%
TasksMax=512
```

## 延伸阅读

- [[02-进程调度与优先级]]
- [[03-Cgroups资源控制]]
- [[../01-Linux基础/07-启动流程|启动流程]]
