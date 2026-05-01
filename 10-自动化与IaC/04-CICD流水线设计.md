# 04-CICD流水线设计

## CI/CD 基本概念

```
Code → Build → Test → Release → Deploy → Monitor
│                   CI                  │   CD   │
```

| 阶段 | 说明 |
|------|------|
| **CI (持续集成)** | 代码合并后自动构建和测试 |
| **CD (持续交付)** | 自动部署到预发布环境，人工审批上线 |
| **CD (持续部署)** | 全自动部署到生产环境 |

## GitHub Actions 示例

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: docker build -t ${{ secrets.REGISTRY }}/myapp:${{ github.sha }} .
      - name: Test
        run: docker run --rm myapp:${{ github.sha }} pytest
      - name: Push
        run: docker push ${{ secrets.REGISTRY }}/myapp:${{ github.sha }}

  deploy:
    needs: build-test
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to K8s
        run: |
          kubectl set image deploy/myapp app=${{ secrets.REGISTRY }}/myapp:${{ github.sha }}
          kubectl rollout status deploy/myapp
```

## 部署策略

| 策略 | 说明 | 风险 |
|------|------|------|
| **滚动更新** | 逐一替换实例 | 低 |
| **蓝绿部署** | 新旧两套环境，切流量 | 低，需要双倍资源 |
| **金丝雀发布** | 5%→20%→100% 渐进切流 | 低，需流量控制能力 |
| **A/B 测试** | 按用户特征分流 | 需细分流量 |

## CI/CD 最佳实践

1. **一次构建，多处部署** — 同一镜像在不同环境部署
2. **环境一致化** — 预发布与生产环境一致
3. **快速回滚** — 回滚时间 < 5 分钟
4. **门禁检查** — 安全扫描、测试覆盖率
5. **不可变基础设施** — 部署即替换，不在线修改

## 延伸阅读

- [[03-Terraform入门]] — 基础设施 CI/CD
- [[05-GitOps实践]] — 声明式部署
- [[../09-容器与编排/06-K8s运维实战|K8s 运维]]
