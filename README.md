# Gamificação SalesRun

---

## Executando o Projeto

Siga as etapas abaixo para configurar e executar o projeto no ambiente local:

1. **Criar um ambiente virtual:**

   ```bash
   python -m venv venv
   ```

2. **Ativar o ambiente virtual:**

   ```bash
   ./venv/Scripts/activate
   ```

3. **Instalar dependências:**

   ```bash
   pip install django
   pip install mysqlclient
   pip install Pillow
   ```

4. **Configurar o Banco de Dados:**

   - Navegue até a pasta `gamificacao`.
   - Abra o arquivo `settings.py`.
   - Localize a variável `DATABASES = {}`.
   - Configure a conexão com o banco de dados. Para instruções detalhadas, consulte a documentação oficial do Django:
     [https://docs.djangoproject.com/en/5.1/ref/databases/](https://docs.djangoproject.com/en/5.1/ref/databases/)

5. **Aplicar as migrações do banco de dados:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

Para ter acesso ao aplicativo, é necessário realizar o cadastro do primeiro usuário com permissões de administrador. Siga as etapas abaixo:

## Cadastro do Primeiro Usuário (Administrador)

1. **Localizar a função `cadastro_view`:**

   - Navegue até a pasta `administrador`.
   - Abra o arquivo `views.py`.
   - Procure a função `cadastro_view`.

2. **Remove a restrição de login temporariamente:**

   - Localize a linha acima da função `cadastro_view` que contém `@login_required`.
   - Comente ou remova temporariamente essa linha.

3. **Iniciar o servidor:**

   - No terminal, inicie o servidor Django utilizando:
     ```bash
     python manage.py runserver
     ```

4. **Acessar a página de cadastro:**

   - Abra o navegador e acesse o endereço:

     ```
     http://127.0.0.1:8000/cadastro
     ```

   - Preencha o formulário para criar o primeiro usuário administrador.

5. **Restaurar a restrição de login:**

   - Volte ao arquivo `views.py`.
   - Recoloque a linha `@login_required` acima da função `cadastro_view`.

6. **Reiniciar o servidor:**
   - Após restaurar o código, reinicie o servidor:
     ```bash
     python manage.py runserver
     ```

Acesse o aplicativo no navegador:
`http://127.0.0.1:8000`

---
