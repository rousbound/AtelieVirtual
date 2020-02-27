import json
import requests
import time

response = requests.get("http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes")
data = response.json()


#Find specific bus stops
def get_onibus(path=""):
  output = ""
  for bus in data['DATA']:
      DATAHORA = bus[0] 
      ORDEM = bus[1] 
      LINHA = bus[2] 
      LATITUDE = bus[3] 
      LONGITUDE = bus[4] 
      VELOCIDADE = bus[5] 
      output += str(LINHA)       +  ","  +\
                str(LATITUDE)    +  ","  +\
                str(LONGITUDE)   +  ","  +\
                str(DATAHORA)    +  ","  +\
                str(VELOCIDADE)  +  "\n"

  with open(path + "BusesPos.txt", "w") as fileTxt:
    fileTxt.write(output)


if __name__ == "__main__":
    get_onibus()
          

