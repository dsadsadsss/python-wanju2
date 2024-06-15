# 使用官方的 Python 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有项目文件到工作目录
COPY . .

# 确保 start.sh 脚本具有可执行权限
RUN chmod +x ./start.sh

# 暴露 Flask 应用的端口
EXPOSE 8080

# 设置容器启动时的命令
CMD ["python", "app.py"]
