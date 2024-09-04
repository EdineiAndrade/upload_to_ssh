import os
import pandas as pd

# Carregar o arquivo Excel
df = pd.read_excel("lista_imagens_2.xlsx")

# Definir o caminho da pasta onde as imagens estão armazenadas
#pasta_imagens = r'C:\Users\inec\Documents\_projetos\freelas\scraping_sites_estevao\site_gruposhopmix\imagens_capa'

# Função para ajustar o nome do arquivo"#
def ajustar_nome(nome_imagem):
    nome = os.path.splitext(nome_imagem)
    if len(nome_imagem) > 100:
        print(len(nome_imagem))
        nome, ext = os.path.splitext(nome_imagem)
        nome = nome[:35] + nome[-(90 - 35 - len(ext)):]  # Manter primeiros 10 e ajustar o final
        

        return nome + ext

    return nome_imagem

# Processar cada linha da planilha
for index, row in df.iterrows():
    id_imagem = row['produto']
    nome_imagem = row['foto1']  # Ajuste o nome da coluna conforme necessário
    pasta_imagens = row['Caminho da Imagem']
    caminho_imagem = pasta_imagens

    if os.path.exists(caminho_imagem):
        novo_nome = ajustar_nome(nome_imagem)
        novo_nome = nome_imagem.replace("miniatura","imagem-produto")
        novo_caminho = os.path.join(r"C:\Users\inec\Documents\_projetos\freelas\scraping_sites_estevao\site_gruposhopmix\imagens_miniaturas", novo_nome)
        tamanho_in = 0
        #if len(nome_imagem) > 100:
            # Renomear a imagem
        try:
            tamanho_in = len(nome_imagem)
            os.rename(caminho_imagem, novo_caminho) 
        except Exception as e:
            print(e)
            continue     
        # Atualizar o nome na planilha
        df.at[index, 'foto'] = novo_nome
        df.at[index, 'novo_link'] = novo_caminho
        tamanho_at = len(novo_nome)
        #print(caminho_imagem)
        print(f"{tamanho_in} -> {tamanho_at} | {novo_nome}")
        
# Salvar a planilha atualizada
df.to_excel(r"C:\Users\inec\Documents\_projetos\freelas\scraping_sites_estevao\site_gruposhopmix\link_imagens_5.xlsx", index=False)
