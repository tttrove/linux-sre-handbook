# 05-GitOps实践

## GitOps 核心原则

```
1. 声明式 — 用声明方式描述整个系统
2. 版本化 — 配置存储在 Git 中
3. 自动拉取 — Agent 自动同步期望状态
4. 持续调和 — 持续监控，实际状态 → 期望状态
```

## 工作流

```
开发者 push 代码 → CI 构建镜像 → 
更新配置仓库 (Git) → GitOps Agent 检测变更 →
自动同步到集群 → 状态持续调和
```

## ArgoCD

```bash
# 创建 Application
kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp-config.git
    path: overlays/production
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
EOF
```

## Flux CD

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/myorg/myapp-config
  ref:
    branch: main

---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 5m
  sourceRef:
    kind: GitRepository
    name: myapp
  path: ./overlays/production
  prune: true
```

## GitOps vs 传统 CI/CD

| 方面 | 传统 CI/CD | GitOps |
|------|------------|--------|
| 部署触发 | CI 工具 push 到集群 | Agent pull 配置变更 |
| 状态保证 | CI 执行一次 | 持续调和 |
| 回滚 | CI 再部署旧版 | Git revert |
| 访问控制 | CI 系统有集群权限 | 集群内 Agent 只读 Git |
| 审计 | CI 日志 | Git 历史 |

## 延伸阅读

- [04-CICD流水线设计](04-CICD流水线设计.md) — 传统 CI/CD
- [K8s 运维](../09-容器与编排/06-K8s运维实战.md)
