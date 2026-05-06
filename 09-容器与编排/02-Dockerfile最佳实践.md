# 02-Dockerfile最佳实践

## 基础原则

1. **减小镜像体积** — 使用多阶段构建、Alpine 基础镜像
2. **利用缓存** — 将不常变的命令放前面
3. **安全优先** — 非 root 运行、最小权限
4. **可复现** — 明确版本号，避免 latest

## 多阶段构建

```dockerfile
# === 构建阶段 ===
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o app .

# === 运行阶段 ===
FROM alpine:3.19
RUN apk add --no-cache ca-certificates tzdata
RUN adduser -D -u 1000 appuser
USER appuser
COPY --from=builder /app/app /app/
EXPOSE 8080
CMD ["/app/app"]
```

最终镜像只有几十 MB，不包含 Go 工具链。

## 分层优化

```dockerfile
FROM node:20-alpine
WORKDIR /app

# 1. 先复制依赖描述文件 (利用缓存)
COPY package.json package-lock.json ./
RUN npm ci --production

# 2. 再复制源码 (变更频繁)
COPY . .

USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

## 最佳实践清单

- **不使用 latest 标签** — 用明确的版本号 (1.21-alpine 而非 latest)
- **合并 RUN 命令** — `RUN cmd1 && cmd2` 减少层数
- **清理依赖缓存** — `apt-get clean && rm -rf /var/lib/apt/lists/*`
- **HEALTHCHECK** — 定义容器健康检查
- **.dockerignore** — 排除 node_modules、.git 等

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget -qO- http://localhost:8080/health || exit 1
```

## 调试技巧

```bash
# 检查镜像层
docker history myapp:latest
docker history --no-trunc myapp:latest

# 分析镜像大小
dive myapp:latest              # 镜像层分析工具

# 进入构建中间层
docker run --rm -it <sha256_hash> sh
```

## 延伸阅读

- [01-Docker核心原理.md](01-Docker核心原理.md)
- [07-容器安全.md](07-容器安全.md)
