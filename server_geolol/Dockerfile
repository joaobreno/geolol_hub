FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app


# Copia apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Instala Redis e sudo
RUN apt-get update && apt-get install -y redis-server sudo

# Cria um usuário e define permissões
RUN useradd -m -s /bin/bash geolol && echo "geolol ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN useradd -ms /bin/sh celery
# This layer is rebuilt when a file changes in the project directory
COPY . /app
# Expõe a porta do Django
EXPOSE 8000

# Comando para rodar as migrações, setup e iniciar o servidor
# CMD ["sh", "-c", "python manage.py migrate && python manage.py first_setup && python manage.py runserver 0.0.0.0:8000"]
CMD /app/entrypoint.sh