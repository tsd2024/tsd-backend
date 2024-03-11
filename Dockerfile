FROM python:3.10.11

EXPOSE 80

ENV PYTHONDONTWRITEBYTECODE=1


WORKDIR /run
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip  \
    && pip install --no-cache-dir -r requirements.txt
RUN pip install pytest
RUN mkdir /run/logs

CMD ["/bin/bash"]