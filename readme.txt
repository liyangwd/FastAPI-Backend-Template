Poetry (version 1.7.1)
安装好 poetry 之后,设置 poetry lock 的时候生成的虚拟环境在当前目录
poetry config virtualenvs.in-project true

在 docker 打镜像发布的时候，是不需要 dev 依赖的，所以在打包的时候可以使用如下命令，比如格式校验这种包
RUN poetry install --no-dev



TODO
precommit  done
celery
requestid  done
日志格式统一 done


本地开发运行步骤
基础环境准备
1.准备好 pgsql 链接信息
2.本地安装 poetry；可以用 pip install poetry 安装；或者其他形式
3.执行 poetry config virtualenvs.in-project true

项目配置准备
1.拷贝 .env.example 为 .env ；修改其中的 pgsql 链接信息
2.BACKEND_LOG_PATH 为日志路径，根据实际情况修改为完整路径
3.执行项目根目录下的 init.sh 脚本，初始化项目
4.根据开发环境指定 .venv虚拟环境
5.运行项目 backend -> src -> main.py 文件
6.访问 http://127.0.0.1:8000/docs 查看接口文档
