import httpx
from bs4 import BeautifulSoup

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
