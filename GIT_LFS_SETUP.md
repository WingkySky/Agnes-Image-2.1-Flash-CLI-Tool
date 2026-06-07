# Git LFS 优化配置指南

本指南介绍如何使用 Git LFS (Large File Storage) 优化 GitHub 文件上传限制。

## 为什么需要 Git LFS？

GitHub 对文件大小有限制：
- **单个文件最大 100 MB**（硬限制）
- **仓库推荐大小**：小于 1 GB
- **最佳实践**：单个文件大于 50 MB 时建议使用 LFS

使用 Git LFS 的好处：
- ✅ 避免 GitHub 文件大小限制
- ✅ 加快克隆和拉取速度
- ✅ 仅在需要时下载大文件
- ✅ 保持仓库轻量

## 本项目的配置说明

### 1. 已生成的配置文件

- [`.gitignore`](./.gitignore) - 排除不需要上传的文件（如 API Key、临时文件等）
- [`.gitattributes`](./.gitattributes) - Git LFS 追踪大文件配置
- 本文件 - 使用说明

### 2. LFS 追踪的文件类型

根据项目特性，以下类型的文件会使用 LFS 管理：

| 文件类型 | 说明 | 原因 |
|---------|------|------|
| `*.png`, `*.jpg`, `*.jpeg` | 图片文件 | AI 生成的图片通常较大 |
| `*.gif`, `*.webp` | 动图和WebP | 可能体积较大 |
| `output/**/*` | 输出目录 | 所有生成的图片 |
| `*.pt`, `*.pth` | 模型文件 | ML 模型通常很大 |
| `*.bin` | 二进制文件 | 大文件 |
| `*.zip`, `*.tar.gz` | 压缩包 | 通常体积较大 |
| 视频/音频文件 | 多媒体 | 天生大文件 |

## 快速开始

### 步骤 1：安装 Git LFS

**macOS:**
```bash
# 使用 Homebrew 安装
brew install git-lfs

# 或者使用 MacPorts
sudo port install git-lfs
```

**Windows:**
```bash
# 下载安装包：https://git-lfs.github.com
# 或使用 Chocolatey
choco install git-lfs
```

**Linux (Ubuntu/Debian):**
```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
```

### 步骤 2：初始化 Git LFS

在项目目录中运行：

```bash
# 初始化 Git LFS（只需要运行一次）
git lfs install

# 验证安装成功
git lfs version
```

### 步骤 3：将现有文件迁移到 LFS（可选）

如果项目已经有大文件，使用以下命令迁移：

```bash
# 迁移所有图片文件到 LFS
git lfs migrate import --include="*.png,*.jpg,*.jpeg"

# 或者迁移 output 目录
git lfs migrate import --include="output/**/*"

# 推送到远程仓库
git push --force
```

**注意：** 此操作会重写 git 历史，团队协作时请协调。

## 日常使用

### 查看 LFS 追踪的文件

```bash
# 查看当前 LFS 追踪的文件列表
git lfs ls-files

# 查看 LFS 追踪的规则
git lfs track

# 查看仓库大小
git lfs status
```

### 克隆使用 LFS 的仓库

```bash
# 正常克隆（自动下载 LFS 文件）
git clone https://github.com/username/repo.git

# 克隆时不下载 LFS 文件（节省空间）
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/username/repo.git

# 之后需要时再下载 LFS 文件
git lfs pull
```

### 只下载特定的 LFS 文件

```bash
# 只下载 output 目录的图片
git lfs pull --include="output/**/*.png"

# 排除某些文件
git lfs pull --exclude="*.jpg"
```

## 文件大小管理建议

### 方案 A：不上传生成的图片（推荐）

如果你只是分享代码，而不是分享图片，可以：

1. 编辑 `.gitignore`，取消以下两行的注释：
   ```
   output/
   *.png
   ```

2. 删除 output 目录中的文件（如果已提交）：
   ```bash
   git rm -r --cached output/
   git commit -m "Remove output images from version control"
   ```

### 方案 B：使用 LFS 管理图片（需要保留图片时）

1. 确保 LFS 已安装和初始化
2. `.gitattributes` 已经配置好了
3. 正常提交和推送即可

### 方案 C：使用外部图片托管

将图片上传到：
- **云存储**：阿里云 OSS、腾讯云 COS、AWS S3
- **图床**：imgur、sm.ms
- **CDN**：Cloudflare R2、七牛云

在代码中使用 URL 引用即可。

## GitHub LFS 存储配额

- **免费用户**：1 GB 存储，1 GB/月带宽
- **Pro 账户**：2 GB 存储，2 GB/月带宽
- **Teams/Enterprise**：更多配额

超过配额时可以：
1. 购买额外的存储空间（$5/月 每 50 GB）
2. 使用外部存储服务
3. 精简仓库内容

## 常见问题

### Q: 我需要安装 Git LFS 才能克隆这个仓库吗？

**A:** 是的，但 Git 会自动检测并提示。如果你只需要代码不需要图片，可以使用：
```bash
GIT_LFS_SKIP_SMUDGE=1 git clone <repo-url>
```

### Q: 忘记配置 LFS，已经提交了大文件怎么办？

```bash
# 1. 安装和初始化 LFS
git lfs install

# 2. 追踪文件类型
git lfs track "*.png"

# 3. 重写历史（谨慎使用）
git lfs migrate import --include="*.png"

# 4. 强制推送
git push --force
```

### Q: 如何移除 LFS 追踪？

```bash
# 取消追踪特定文件类型
git lfs untrack "*.png"

# 重新提交
git add .gitattributes
git commit -m "Stop tracking PNG files with LFS"
```

### Q: 本地仓库太大了怎么办？

```bash
# 清理 LFS 缓存
git lfs prune

# 清理旧的提交
git reflog expire --expire-unreachable=now --all
git gc --prune=now

# 查看 LFS 存储使用情况
git lfs ls-files --size
```

## 本项目推荐的工作流程

### 开发时

1. 正常使用 `agnes_image.py` 生成图片
2. 图片会自动保存到 `output/` 目录
3. 根据需要决定是否上传图片

### 提交代码时

```bash
# 添加代码文件
git add agnes_image.py
git add README*.md
git add .gitignore
git add .gitattributes

# 添加图片（如果选择上传）
git add output/

# 提交
git commit -m "Add image generation feature"

# LFS 会自动处理大文件
git push
```

## 更多信息

- Git LFS 官网：https://git-lfs.github.com
- GitHub LFS 文档：https://docs.github.com/en/repositories/working-with-files/managing-large-files
- Git LFS 规格说明：https://github.com/git-lfs/git-lfs/tree/main/docs
