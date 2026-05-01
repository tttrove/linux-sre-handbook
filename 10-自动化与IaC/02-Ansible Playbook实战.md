# 02-Ansible Playbook实战

## Playbook 示例：部署 Web 应用

```yaml
---
# site.yml
- name: Deploy web application
  hosts: web
  become: yes
  vars:
    app_user: myapp
    app_dir: /opt/myapp
    app_version: "1.2.3"

  tasks:
    - name: Create app user
      user:
        name: "{{ app_user }}"
        shell: /sbin/nologin
        create_home: no

    - name: Create app directory
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"

    - name: Deploy application binary
      copy:
        src: "files/myapp-{{ app_version }}.jar"
        dest: "{{ app_dir }}/myapp.jar"
        owner: "{{ app_user }}"

    - name: Deploy configuration
      template:
        src: templates/config.yaml.j2
        dest: /etc/myapp/config.yaml
      notify: restart myapp

    - name: Deploy systemd unit
      template:
        src: templates/myapp.service.j2
        dest: /etc/systemd/system/myapp.service
      notify: restart myapp

    - name: Start and enable service
      systemd:
        name: myapp
        state: started
        enabled: yes
        daemon_reload: yes

  handlers:
    - name: restart myapp
      systemd:
        name: myapp
        state: restarted
```

## 模板 (Jinja2)

```yaml
# templates/config.yaml.j2
server:
  port: {{ app_port | default(8080) }}
  host: 0.0.0.0

database:
  host: {{ db_host }}
  port: {{ db_port }}
  name: {{ db_name }}

{% if env == "production" %}
  pool_size: 50
{% else %}
  pool_size: 10
{% endif %}
```

## Role 目录结构

```
roles/
└── myapp/
    ├── tasks/
    │   └── main.yml        # 入口 tasks
    ├── handlers/
    │   └── main.yml
    ├── templates/
    │   ├── config.yaml.j2
    │   └── myapp.service.j2
    ├── files/
    │   └── myapp.jar
    ├── vars/
    │   └── main.yml
    ├── defaults/
    │   └── main.yml        # 默认变量 (优先级最低)
    └── meta/
        └── main.yml        # Role 依赖
```

## 常用模式

### 滚动更新

```yaml
- name: Rolling update
  hosts: web
  serial: 1                 # 一次只更新一台
  tasks:
    - name: Drain from LB
      # ...
    - name: Update app
      # ...
    - name: Add back to LB
      # ...
```

### 条件执行

```yaml
- name: Install EPEL on RHEL
  yum:
    name: epel-release
  when: ansible_os_family == "RedHat"
```

## 延伸阅读

- [[01-Ansible基础]]
- [[03-Terraform入门]] — IaC 互补工具
