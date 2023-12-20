FROM python:3.9
COPY dist/operation_cli-0.1.0-py3-none-any.whl /opt/operations/operation_cli-0.1.0-py3-none-any.whl
ENV PATH=$PATH:/usr/local/lib/python3.9
ENV PATHONPATH $PATH
RUN pip3 install /opt/operations/*.whl -i https://pypi.tuna.tsinghua.edu.cn/simple/