# 01-Ansible基础

## Ansible 架构

```
Control Node (Ansible)
    ↓ SSH (无 agent)
Managed Nodes (目标服务器)
```

## 核心概念

| 概念 | 说明 |
|------|------|
| **Inventory** | 主机清单 |
| **Module** | 执行单元 (copy, yum, service...) |
| **Task** | 一个模块调用 |
| **Play** | 一组 Task 的集合 |
| **Playbook** | 一组 Play 的 YAML 文件 |
| **Role** | 可复用的 Ansible 内容集合 |
| **Fact** | 自动发现的系统信息 |

## 基础命令

```bash
# Ad-hoc 命令
ansible all -m ping
ansible web -m command -a "uptime"
ansible db -m yum -a "name=nginx state=present" -b

# Playbook
ansible-playbook site.yml
ansible-playbook site.yml --check       # 干跑
ansible-playbook site.yml --limit web   # 限定主机
ansible-playbook site.yml --start-at-task="Install Nginx"

# 查看信息
ansible-doc -l                # 模块列表
ansible-doc -s copy           # 模块用法
```

## Inventory

```ini
# hosts.ini
[web]
web-1 ansible_host=10.0.0.1
web-2 ansible_host=10.0.0.2

[db]
db-1 ansible_host=10.0.1.1 ansible_user=postgres

[all:vars]
ansible_user=deploy
ansible_ssh_private_key_file=~/.ssh/id_ed25519
```

## 常用模块

```yaml
# 文件操作
- copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'

- template:
    src: nginx.conf.j2   # Jinja2 模板
    dest: /etc/nginx/nginx.conf

# 包管理
- yum: name=nginx state=latest      # RHEL
- apt: name=nginx state=present     # Debian

# 服务管理
- systemd:
    name: nginx
    state: started
    enabled: yes

# 用户管理
- user:
    name: myapp
    state: present
    shell: /sbin/nologin
```

## 延伸阅读

- [02-Ansible Playbook实战.md](02-Ansible%20Playbook实战.md)
- [../07-进程与Service管理/01-systemd深度使用.md](../07-进程与Service管理/01-systemd深度使用.md)
