FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala dependências do Django e do Celery
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y redis-server
RUN apt-get update && apt-get install -y sudo
RUN useradd -m -s /bin/bash geolol && echo "geolol ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER geolol

# Expõe a porta do Django
EXPOSE 8000

# Comando para rodar as migrações, setup e iniciar o servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py first_setup && python manage.py runserver 0.0.0.0:8000"]
