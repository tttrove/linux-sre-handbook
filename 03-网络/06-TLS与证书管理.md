# 06-TLS与证书管理

## TLS 握手流程

### TLS 1.2 完整握手（2-RTT）

```
Client → ClientHello (支持的加密套件, 随机数)
Server ← ServerHello + Certificate + ServerKeyExchange + ServerHelloDone
Client → ClientKeyExchange + ChangeCipherSpec + Finished
Server ← ChangeCipherSpec + Finished
```

### TLS 1.3 握手（1-RTT）

简化了握手流程，移除不安全算法，默认前向安全。

## 证书查验

```bash
# 查看远程证书
openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -text

# 关键信息
openssl x509 -noout -subject -dates -issuer -in cert.pem

# 证书链验证
openssl verify -CAfile ca-bundle.crt cert.pem

# 证书过期时间（批量检查）
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | \
    openssl x509 -noout -enddate
```

## 证书类型

| 类型 | 验证级别 | 颁发速度 | 适用场景 |
|------|----------|----------|----------|
| DV | 域名验证 | 分钟级 | 个人网站 |
| OV | 组织验证 | 1-3 天 | 企业网站 |
| EV | 扩展验证 | 3-10 天 | 金融等高风险 |

## 自签证书 vs CA 证书

```bash
# 生成自签证书
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# 生成 CSR（证书签名请求）
openssl req -new -newkey rsa:4096 -keyout key.pem -out csr.pem -nodes
```

## Let's Encrypt (ACME) 自动化

```bash
# certbot 自动获取
certbot certonly --standalone -d example.com -d www.example.com
certbot renew                    # 续期
certbot certificates             # 查看已获取证书
```

## SRE 最佳实践

1. **证书到期监控** — TLS 证书过期是常见故障源，设置 30 天提前告警
2. **HSTS** — HTTP Strict Transport Security 强制 HTTPS
3. **密钥安全** — 私钥加密存储，使用 HSM 或密钥管理服务
4. **最低 TLS 版本** — 至少 TLS 1.2，推荐 TLS 1.3
5. **密码套件选择** — 优先 AEAD（如 AES-GCM、ChaCha20-Poly1305）
6. **证书透明 (CT)** — 监控未授权证书签发

```bash
# 测试 TLS 版本和密码套件支持
nmap --script ssl-enum-ciphers -p 443 example.com
sslscan example.com
testssl.sh https://example.com
```

## 延伸阅读

- [03-HTTP与负载均衡.md](03-HTTP与负载均衡.md) — HTTPS 与负载均衡
- [04-网络排查工具链.md](04-网络排查工具链.md) — 排查 SSL 问题
