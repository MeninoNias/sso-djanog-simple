import requests

# Dados para enviar no corpo da solicitação
data = {
    "email": "user_80673@example.com",
    "password": "123456"
}

# Credenciais de autenticação do IDP
idp_id = '8d465d27-6eb3-4ac1-8bac-807e0075e5fe'
api_key = '44426fb2-d386-4c93-aa25-a77b6542cd6e'

# URL do endpoint de login do seu sistema
host = 'http://127.0.0.1:8000'

#SERVER TESTE
# host = 'http://3.93.16.145'

path = 'sso/api/v1/login/'
# url = f'{host}/api/singin'
url = f'{host}/{path}'

# Realiza a solicitação POST com os dados e credenciais de autenticação
response = requests.post(
    url,
    json=data,
    auth=(idp_id, api_key),
    timeout=5
)

# Verifica a resposta
if response.status_code == 200:
    print("-------------------------------------")
    # print("Sucesso! O usuário foi autenticado.")
    print(response.json())
    print("-------------------------------------")
else:
    # print(response.__dict__)
    print("Erro ao autenticar o usuário. Status code:", response.status_code)
