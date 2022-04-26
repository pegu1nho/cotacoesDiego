import requests
import sqlite3
import datetime
import config

banco = sqlite3.connect('cotacoes.db')
cursor = banco.cursor()

#cursor.execute("CREATE TABLE cotacao (id_cotacao integer PRIMARY KEY AUTOINCREMENT, dolar text, euro text, data text, hora text)")

fields = 'only_results,USD,EUR'
key = config.api_key
URL = f'https://api.hgbrasil.com/finance?format=json&array_limit=1&fields={fields}&key={key}'

def inserir_banco(dolar, euro, data, hora):
    cursor.execute("INSERT INTO cotacao (dolar, euro, data, hora) VALUES ('"+dolar+"', '"+euro+"', '"+data+"', '"+hora+"')")
    banco.commit()

def buscar_banco():
    cursor.execute("SELECT * FROM cotacao")
    print(cursor.fetchall())

def consultar_dados(url, moeda):

    resposta = requests.get(URL)

    if resposta:

        r = resposta.json()

        valor = r['currencies'][f'{moeda}']['buy']

        return valor

def converte(val, val2):
    return val * val2

def imprime_moedas(usd, eur):
    print(f"Valor do Dólar: {usd}")
    print(f"Valor do Euro: {eur}")

def imprime_conversao(dolar, euro):
    print(f"\nConversão em:")
    print(f"Dólar: {dolar}")
    print(f"Euro: {euro}")

def retorna_data():
    d = datetime.datetime.now()
    data = (f"{d.day}/{d.month}/{d.year}")
    return data

def retorna_hora():
    d = datetime.datetime.now()
    hora = (f"{d.hour}:{d.minute}:{d.second}")
    return hora

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    usd = consultar_dados(URL, 'USD')
    eur = consultar_dados(URL, 'EUR')
    imprime_moedas(usd, eur)

    valor = float(input("\nDigite um valor em real: "))

    dolar = converte(valor, usd)
    euro = converte(valor, eur)
    imprime_conversao(dolar, euro)

    inserir_banco(str(dolar), str(euro), retorna_data(), retorna_hora())
    buscar_banco()












