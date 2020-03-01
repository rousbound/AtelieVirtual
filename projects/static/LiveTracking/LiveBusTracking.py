import json
import requests
import time

def get_onibus():
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
  return output

while True:
    try:  
      response = requests.get("http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes")
      data = response.json()


              

      output = get_onibus()
      with open("BusesPos.txt", "w") as fileTxt:
        fileTxt.write(output)
      time.sleep(5)
    except:
        print("Error getting request")
