#!/bin/bash

# 检查 Poetry 是否已安装
if ! command -v poetry &> /dev/null
then
    echo "Poetry 未安装，请先安装 Poetry。(version 1.7.1)"
    exit 1
fi

# 安装项目依赖
echo "正在安装项目依赖..."
poetry install

# 安装 pre-commit 钩子
echo "正在安装 pre-commit 钩子..."
pre-commit install

echo "初始化完成！"
