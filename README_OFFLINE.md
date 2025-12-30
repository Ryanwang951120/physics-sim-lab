# 離線環境部署指南 (Offline Deployment Guide)

本指南說明如何在無網路環境的機器上部署此物理模擬應用程式。

## 1. 檔案準備
在有網路的機器上（当前机器），我们已经生成了以下离线镜像文件：
- **`physics-sim-offline.tar`** (Docker 映像檔)

请将此文件复制到目标机器（无网络环境）。

## 2. 在目標機器上載入映像檔
在目标机器上打开终端（Terminal 或 PowerShell），进入存放 `.tar` 文件的目录，运行：

```bash
docker load -i physics-sim-offline.tar
```

成功后，你会看到类似 `Loaded image: physics-sim:latest` 的提示。

## 3. 啟動應用程式
映像檔载入后，直接运行容器即可：

```bash
docker run -d -p 8501:8501 --name physics-lab physics-sim:latest
```

## 4. 訪問應用
打开浏览器访问：
http://localhost:8501

---

### 常用管理命令

- **停止服务**: `docker stop physics-lab`
- **删除服务**: `docker rm physics-lab`
- **查看日志**: `docker logs physics-lab`
