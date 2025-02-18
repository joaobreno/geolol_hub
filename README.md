# Projeto GeoLoL HUB

Este é um projeto Django que pode ser executado localmente ou via Docker.

---

## 🚀 Rodando o projeto localmente

### 📌 Pré-requisitos
- Python 3.10 instalado
- Virtualenv
- Banco de dados MySQL rodando

### ⚙️ Passos para rodar localmente

1. Clone o repositório:  
   ```bash
   git clone git@github.com:joaobreno/geolol_hub.git
   cd server_geolol
   ```

2. Crie um ambiente virtual
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\Activate.ps1`
    ```

3. Instale as dependências
    ```bash
    pip install -r requirements.txt
    ```

4. Execute o comando para criar os modelos obrigatórios
    ```bash
    python manage.py first_setup
    ```
5. Alterar arquivos do AllAuth
    <br>Para seguir a padronização do projeto, é necessário fazer algumas alterações manuais nos inputs utilizados do AllAuth. Para isso, é necessário alterar as linhas dispostas em **CONFIGS ALL AUTH.txt**

5. Execute o servidor de desenvolvimento
    ```bash
    python manage.py runserver
    ```
    O servidor estará rodando em http://127.0.0.1:8000/.

---

## 🚀 Rodando com o Docker

### 📌 Pré-requisitos
- Docker
- Docker Compose

#### 🐳 Como instalar o Docker e Docker Compose

##### Docker  
Para instalar o Docker, siga o guia oficial de instalação de acordo com o seu sistema operacional:

- [Instalar Docker no Windows](https://docs.docker.com/desktop/install/windows/)
- [Instalar Docker no macOS](https://docs.docker.com/desktop/install/mac/)
- [Instalar Docker no Linux](https://docs.docker.com/engine/install/)

##### Docker Compose  
O **Docker Compose** já vem incluído no Docker Desktop para **Windows** e **macOS**.  
Para **Linux**, siga o guia oficial:

- [Instalar Docker Compose no Linux](https://docs.docker.com/compose/install/linux/)

Após a instalação, verifique se o Docker e o Docker Compose estão funcionando corretamente com os seguintes comandos:<br>
    ```
    docker --version
    ```

### ⚙️ Passos para a configuração
1. Clone o repositório:  
   ```bash
   git clone git@github.com:joaobreno/geolol_hub.git
   cd server_geolol
   ```

2. Execute o Docker Compose
    O projeto usa três arquivos docker-compose para diferentes configurações. Para rodar o projeto localmente com o banco de dados e todas as outras dependências, use o seguinte comando:
    ```bash
    docker-compose -f docker-compose-ci.yml -f docker-compose-db.yaml -f .\docker-compose.yml up --build
    ```
    O servidor estará rodando em http://127.0.0.1:8000/