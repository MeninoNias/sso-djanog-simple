# Use a imagem base do Python
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY requirements.txt /app/
COPY . /app/

ADD run_deploy.sh /
RUN chmod +x /run_deploy.sh

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta em que a aplicação Django está sendo executada
EXPOSE 8000

# Comando para iniciar o servidor Django
CMD ["/run_deploy.sh"]