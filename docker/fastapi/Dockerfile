FROM python:3.10.11

EXPOSE 80

ENV PYTHONDONTWRITEBYTECODE=1


WORKDIR /run
COPY . /run

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip  \
    && pip install --no-cache-dir -r requirements.txt
RUN pip install pytest
RUN mkdir /run/logs

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "80", "src.app.main:app", "--reload" ]