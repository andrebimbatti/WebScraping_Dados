from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import zipfile
from tqdm import tqdm
from rich import print
import os


os.system('cls')

# Configurando o chrome para o download
caminho_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_download = os.path.join(caminho_atual, "downloads")
chrome_options = Options()
chrome_options.add_experimental_option('prefs',{
    'download.default_directory': diretorio_download,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enable': True
})

def aguardar_download_concluir(diretorio):
    """
    Função para aguardar até que todos os downloads sejam concluídos.
    
    :param diretorio: Diretório onde os arquivos estão sendo baixados.
    """
    while True:
        # Verifica se existem arquivos .crdownload ou outros arquivos temporários
        arquivos_temp = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.crdownload')]
        
        if not arquivos_temp:
            print("Download concluído!")
            break
        
        sleep(1)


# Iniciando o navegador
url = 'https://dadosabertos.rfb.gov.br/CNPJ/dados_abertos_cnpj/2024-08/'
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
wait = WebDriverWait(driver, 10)
sleep(10)

#iniciando loop para pegar os links

numero_downloads = 100

for i in range(4, numero_downloads):
    xpath_downloads = f'/html/body/table/tbody/tr[{i}]/td[2]/a'
    try:
        # Aguarda o elemento estar presente e obtém o link de download
        botao_download = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_downloads)))
        botao_download.click()
        sleep(10)
        aguardar_download_concluir(diretorio_download)

    except Exception:
        print(f"Não foi encontrado mais links para downloads")
        break

driver.quit()
sleep(3)

# Função para descompactar arquivos
def descompactar_arquivos(diretorio):
    for arquivo in tqdm(os.listdir(diretorio), desc="Descompactando arquivos"):
        if arquivo.endswith(".zip"):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            try:
                with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                    zip_ref.extractall(diretorio)
                print(f"Arquivo {arquivo} descompactado com sucesso!")
                
            except zipfile.BadZipFile:
                print(f"Erro: {arquivo} não é um arquivo zip válido.")
            except Exception as e:
                print(f"Erro ao descompactar {arquivo}: {e}")

descompactar_arquivos(diretorio_download)

print(f'[green]Arquivos descompactados com sucesso!')