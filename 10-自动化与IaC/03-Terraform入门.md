# 03-Terraform入门

## Terraform 核心概念

| 概念 | 说明 |
|------|------|
| **Provider** | 云平台接口 (AWS, GCP, Azure...) |
| **Resource** | 可管理的基础设施对象 |
| **State** | 基础设施当前状态 (terraform.tfstate) |
| **Module** | 可复用的 Terraform 配置集合 |

## 工作流

```
1. Write: 编写 .tf 配置文件
2. Plan: terraform plan (查看变更)
3. Apply: terraform apply (执行变更)
4. Destroy: terraform destroy (销毁资源)
```

## 基础示例 — AWS EC2

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  count         = 3

  vpc_security_group_ids = [aws_security_group.web.id]

  tags = {
    Name = "web-${count.index + 1}"
    Env  = var.environment
  }
}

resource "aws_security_group" "web" {
  name = "web-sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## 变量与输出

```hcl
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

output "web_ips" {
  value = aws_instance.web[*].public_ip
}
```

## 状态管理

```bash
# 远程状态 (团队协作必须)
terraform init    # 初始化 backend

# 状态查看
terraform state list
terraform state show aws_instance.web[0]

# 导入已有资源
terraform import aws_instance.web i-1234567890abcdef

# 锁定 (防止并发)
terraform apply -lock=true
```

## SRE 最佳实践

1. **远程状态存储** — S3 + DynamoDB 锁
2. **Module 化** — 不要重复写相同配置
3. **变量化** — 环境差异通过变量传入
4. **Plan 审查** — CI 中自动 plan，人工确认后 apply
5. **标记管理** — 统一 Tag 命名规范

## 延伸阅读

- [04-CICD流水线设计](04-CICD流水线设计.md) — Terraform 在 CI/CD 中
- [05-GitOps实践](05-GitOps实践.md) — GitOps 理念
