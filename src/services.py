import httpx
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"

def fetch_opcao(opcao: str):
    """
    Faz scraping da tabela de Embrapa para a opção informada
    e retorna lista de registros (listas de strings).
    """
    r = httpx.get(BASE_URL, params={"opcao": opcao}, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")
    if not table:
        return []
    dados = []
    for tr in table.find_all("tr"):
        cols = [td.get_text(strip=True) for td in tr.find_all(["th","td"])]
        dados.append(cols)
    return dados

def crawl_embrapa(year):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"
    response = httpx.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    tables = soup.find_all('table', class_='tb_base')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) == 2 and cols[0] != 'Produto' and cols[0] != 'Total':
                product = cols[0]
                quantity = cols[1].replace('.', '').replace('-', '0')
                try:
                    quantity = int(quantity)
                except ValueError:
                    quantity = 0
                data.append([product, quantity])

    df = pd.DataFrame(data, columns=['Produto', 'Quantidade (L.)'])
    return df
