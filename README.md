# Upload de Imagens via SSH

Este projeto faz upload de imagens de uma pasta local para uma pasta remota em um servidor usando SSH. Além disso, ele gera um relatório em Excel com o status de cada upload.

## Funcionalidades

- Conexão segura com o servidor via SSH usando uma chave privada RSA.
- Upload de arquivos de imagem (.jpg) de uma pasta local para uma pasta remota.
- Verificação do tamanho dos arquivos antes do upload.
- Geração de um relatório em Excel com o status de cada arquivo (enviado com sucesso, ignorado devido ao tamanho, etc.).

## Requisitos

- Python 3.x
- Pacotes necessários: `dotenv`, `paramiko`, `os`, `glob`, `pandas`, `time`

## Instalação

1. Clone este repositório.
2. Instale as dependências necessárias usando pip:

   ```bash
   pip install -r requirements.txt
   ```
