Poetry (version 1.7.1)
安装好 poetry 之后,设置 poetry lock 的时候生成的虚拟环境在当前目录
poetry config virtualenvs.in-project true

在 docker 打镜像发布的时候，是不需要 dev 依赖的，所以在打包的时候可以使用如下命令，比如格式校验这种包
RUN poetry install --no-dev



TODO
precommit  done
celery
requestid
日志格式统一
