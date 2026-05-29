FROM python:3.11-slim

# Устанавливаем компилятор
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    gcc \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir grpcio==1.60.0 grpcio-tools==1.60.0 protobuf==4.25.3

# Копируем proto файлы
COPY proto/ ./proto/

# СОЗДАЁМ ПАПКУ generated ПЕРЕД ГЕНЕРАЦИЕЙ
RUN mkdir -p ./generated

# Генерируем gRPC код
RUN python -m grpc_tools.protoc -I./proto --python_out=./generated --grpc_python_out=./generated ./proto/service.proto

# Копируем код приложения
COPY app/ ./app/
COPY generated/ ./generated/

# Создаём __init__.py
RUN touch /app/generated/__init__.py && \
    touch /app/app/__init__.py

# Опционально: удаляем компилятор для уменьшения образа
RUN apt-get purge -y --auto-remove g++ gcc make

EXPOSE 50051

CMD ["python", "app/server.py"]