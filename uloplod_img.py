from dotenv import load_dotenv
from termcolor import colored
import paramiko
import os
import pandas as pd
import time

load_dotenv()

def connect_ssh():
    #conexão SSH e retorna o cliente SSH e SFTP
    hostname = os.getenv('HOST_NAME')
    port = int(os.getenv('PORT'))
    username = os.getenv('USER')
    password = os.getenv('PASSWORD')
    private_key_path = "id_key"
    
    #Carregando a chave privada RSA
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path, password=password)

    #Criando o cliente SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, pkey=private_key)
    
    #Criando o cliente SFTP
    sftp = ssh.open_sftp()
    
    return ssh, sftp

def upload_file(sftp, local_file_path, remote_file_path):
    #Upload da imagem para o servidor remoto e retorna o status.
    try:
        time.sleep(.1)
        sftp.put(local_file_path, remote_file_path)
        print(colored(f"Sucesso ao enviar: ==> {remote_file_path}",'green'))
        return 'Sucesso'
    except Exception as e:
        print(e)
        return f'Erro: {e}'

def process_files(list_img, remote_directory, size_limit_kb=1000):
    #Processa arquivos na pasta local e envia para o servidor remoto se atender aos critérios.
    results = []
    df = pd.read_excel(list_img)
    files = df['img_path']
    
    ssh, sftp = connect_ssh()

    for index,file_path in enumerate(files):
        file_size_kb = os.path.getsize(file_path) / 1024  # Tamanho em KB
        file_name = os.path.basename(file_path)
        remote_file_path = f"{remote_directory}/{file_name}"
        print(f"Processando arquivo {index}: {file_path}")
        if file_size_kb <= size_limit_kb:
            status = upload_file(sftp, file_path, remote_file_path)
            
        else:
            status = 'Ignorado: tamanho excedido'
        
        results.append([file_name, file_size_kb, status])
    
    sftp.close()
    ssh.close()
    return results

def save_to_excel(results, excel_file_path):
    #Salva os resultados em uma planilha Excel usando pandas
    # Criar um DataFrame a partir da lista de resultados
    df = pd.DataFrame(results, columns=['Nome do Arquivo', 'Tamanho (KB)', 'Status'])
    
    # Salvar o DataFrame em um arquivo Excel
    df.to_excel(excel_file_path, index=False, sheet_name='Status de Upload')

def main():
    base_path = os.getenv('BASE_PATH')
    list_img = os.path.join(base_path,'Edinei\\freelas\\site_03_triboshoes\\arquivos\\list_img_to_ssh.xlsx')
    remote_directory = "public_html/sistema/painel_loja/images/produtos"
    excel_file_path = os.path.join(base_path,"\\Edinei\\freelas\\site_03_triboshoes\\arquivos\\result_to_ssh.xlsx")
    
    results = process_files(list_img, remote_directory)
    save_to_excel(results, excel_file_path)
    print(f"Resultados salvos em {excel_file_path}")

if __name__ == "__main__":
    main()
