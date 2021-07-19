# PROJETO CRIADO EM CONJUNTO COM A LEST CODE PARA O DESENVOLVIMENTO DO PROGRAMA BECAS ( SANTANDER UNIVERSITARIO),
# para a conclusão da segunda fase do processo seletivo.
# CURSO: DATA SCIENCE

#   Dev. Cristiano Freitas
#   email: junior.brown.eda@gmail.com
#   Data de inicio do projeto: 12/07/2021
#   Data de "Final" do projeto: 15/05/2021



import  csv
import requests as r
import datetime as dt




# API de dados registrados sobre: Confirmados, Obtos, Recuperados, Ativo, Data.
# Todos os dados são relacionados ao caso da covid-19 no Brasil

# Uso da API onde os registros estão salvos
coder = 'https://api.covid19api.com/dayone/country/brazil'
req = r.get(coder)

dados = req.json()

# adicão de objetos da tabela através do conceito de list do python

final_dados = []

for obj in dados:
  final_dados.append([obj['Confirmed'],obj['Deaths'],obj['Recovered'],obj['Active'],obj['Date']])

final_dados.insert(0, ['Confirmados', 'Obtos', 'Recuperados', 'Ativo', 'Data'])

CONFIRMADOS = 0
OBTOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

# Tratamento do objeto DATA: uma limpeza nos dados das datas do caso, deixando a vizualização mais limpa.

for i in range(1, len(final_dados)):
  final_dados[i][DATA] = final_dados[i][DATA][:10]



with open('brasil_covid.csv', 'w', encoding='utf-8') as file:

  writer = csv.writer(file)
  writer.writerow(final_dados)

for i in range(1, len(final_dados)):

  final_dados[i][DATA] = dt.datetime.strptime(final_dados[i][DATA], '%Y-%m-%d')


# função para a criação do GRAFICO para a vizualização dos dados acima

def get_data(y, labels):
  if type(y[0]) == list:
    datasets = []
    for i in range(len(y)):
      datasets.append({
        'label': labels[i],
        'data': y[i]
      })
    return datasets
  else:
    return [{
      'label': labels[0],
      'data': y

    }]



def set_title(title=''):
  if title == '':
    display = 'true'
  else:
    display = 'false'
  return{
    'title': title,
    'display': display
  }


def create_chart(x, y, labels, kind='bar', title=''):

  datasets = get_data(y, labels)
  options = set_title(title)

  chart = {
    'type': kind,
    'data': {

      'labels': x,
      'datasets': datasets

    },
    'options': options
  }

  return chart

def get_api(chart):
  url = 'https://quickchart.io/chart'
  req = r.get(f'{url}?c={str(chart)}')
  return req.content

def save_image(path, content):
  with open(path,'wb') as image:
    image.write(content)

from PIL import Image
from IPython.display import display

def display_image(path):
  img_pil = Image.open(path)
  display(img_pil)

y_data_1 = []
for obs in final_dados[1::10]:
  y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in final_dados[1::10]:
  y_data_2.append(obs[RECUPERADOS])

labels = ['Confirmados', 'Recuperados']

x = []
for obs in final_dados[1::10]:
  x.append(obs[DATA].strftime('%d/%m/%Y'))

chart = create_chart(x, [y_data_1, y_data_2], labels, title = 'Grafico Covid')
chart_content = get_api(chart)
save_image('grafico_covid.png', chart_content)
display_image('grafico_covid.png')

# função para a criação do QRCODE para a vizualização do grafico

from urllib.parse import quote


def get_qrcode(link):
  text= quote(link)
  url_base = 'https://quickchart.io/qr'
  req = r.get(f'{url_base}?c={str(text)}')
  return req.content

url_base= 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qrcode_covid.png', get_qrcode(link))
display_image('qrcode_covid.png')




