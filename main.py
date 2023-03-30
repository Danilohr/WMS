import datetime
from multiprocessing.dummy import current_process
from operator import indexOf
from pickle import FALSE
import re
import shutil
from token import EXACT_TOKEN_TYPES
from typing import List
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from twilio.rest import Client
from sh import mount

# Variables
options = Options()
options.headless = True
options.add_argument('--log-level=3')
driver = webdriver.Firefox(options=options)
linkMoodle = "https://ava.cefetmg.br/calendar/view.php?view=upcoming#"
linkSigaa = "https://sig.cefetmg.br/sigaa/verTelaLogin.do"
login = ""
senha = ""

option = Options()
option.headless = True
option.add_argument('--log-level=3')
driver = webdriver.Firefox(
    options=option)
lkLogin = ["https://sig.cefetmg.br/sigaa/verTelaLogin.do",
           "https://ava.cefetmg.br/calendar/view.php?view=upcoming#"]
login = ""
senha = ""
atvList = []

class Atividade:
    """Classe usada para armazenar os dados"""
    dia = mes = 0
    def __init__(self, data: str, materia: str, nome: str):
        self.data = data
        self.materia = materia
        self.nome = nome
        self.site = ""

    def setSite(self, site:str):
        self.site = site

    def __str__(self) -> str:
        return self.data+self.site+ " - " +self.materia+": " + self.nome

def LogarSites(linkSigaa:str, linkMoodle:str) -> List[Atividade]:
    """Acessa Sites e pega as Tarefas"""
    # Pega o login e a senha
    a = open("/home/danilo/Documents/Prog/logins.txt", "r")
    login = a.read().strip()
    senha = login.split(";")[1]
    login = login.split(";")[0]

    atvList:List[Atividade] = []
    def VerData(atv:Atividade):
        # Verifica se a atividade já passou
        hoje = datetime.date.today()
        if hoje.month<atv.mes or (hoje.month==atv.mes and hoje.day<=atv.dia):
            atvList.append(atv)
    def PreparaAtv(atv: Atividade, site: str) -> Atividade:
    # Substitui o nome inteiro da matéria pelo nome abreviado
        def arrumaMateria():
            if("infra" in atv.materia.lower()):
                atv.materia = "IFR"
            elif("segur" in atv.materia.lower()):
                atv.materia = "SR"
            elif("banco" in atv.materia.lower()):
                atv.materia = "BD"
            elif("projeto" in atv.materia.lower()):
                atv.materia = "PRC"
            elif("operacional" in atv.materia.lower()):
                atv.materia = "SSO"
            elif("emergentes" in atv.materia.lower()):
                atv.materia = "TER"
            elif("química" in atv.materia.lower()):
                atv.materia = "QUI"
            elif("sociologia" in atv.materia.lower()):
                atv.materia = "SOC"
            elif("portugu" in atv.materia.lower()):
                atv.materia = "POR"
            elif("matem" in atv.materia.lower()):
                atv.materia = "MAT"
            elif("hist" in atv.materia.lower()):
                atv.materia = "HIS"
            elif("físi" in atv.materia.lower()):
                atv.materia = "FIS"
            elif("empreen" in atv.materia.lower()):
                atv.materia = "EMP"
            elif("redação" in atv.materia.lower()):
                atv.materia = "RED T1"
            elif("ingl" in atv.materia.lower()):
                atv.materia = "ING T1"
        arrumaMateria()

        if(site == "(M)"):
            # Caso a data seja "Amanhã", calcula-se a data numérica
            if atv.data.startswith("Amanhã"):
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                atv.data = str(f"{tomorrow.day:02}") + "/" + \
                    str(f"{tomorrow.month:02}") + atv.data[:atv.data.index("Amanhã")]
            elif atv.data.startswith("Hoje"):
                today = datetime.date.today()
                atv.data = str(f"{today.day:02}") + "/" + \
                    str(f"{today.month:02}") + atv.data[:atv.data.index("Hoje")]
            else:
                # Procura por qual mês está a tarefa e substitui no formato numérico
                meses = ["janeiro", "fevereiro", "março", "abril", "maio", 
                    "junho", "julho", "agosto", "setembro", "outubro",
                    "novembro", "dezembro"]
                # Retira o nome por extenso
                for i, mes in enumerate(meses):
                    if(mes in atv.data.lower()):
                        atv.data = atv.data[atv.data.index(" ")+1:]
                        atv.data = f"{int(atv.data[:atv.data.index(mes)-1]):02}/{i+1:02}"
                        break

            # Retira o horário indesejado
            if(atv.data.endswith("23:59")):
                atv.data = atv.data[:atv.data.rfind(',')]
            else:
                atv.data = atv.data.replace(",", "")

            # Retira palavras descartáveis
            try:
                atv.nome = atv.nome[:atv.nome.index(" está marcado")]
            except ValueError: pass
            atv.nome = atv.nome.replace("ercício ", "", 1)
            procura = re.search(" - [0-9]*/[0-9]*/[0-9]*", atv.nome)
            if procura:
                atv.nome = atv.nome.replace(procura.group(), "")
            try:
                procura = str(re.search("- [0-9]*?.?[0-9]? pts", atv.nome).group())
                atv.nome = atv.nome.replace(procura, '('+procura[2:-3]+'pontos)')
            except (TypeError, AttributeError): pass

        else:
            horario = ""
            try:
                horario = str(re.search(" [0-9]*:[0-9]*", atv.data).group())
            except AttributeError: pass
            atv.data = atv.data[:atv.data.rfind("/")]
            if not "23:59" in horario:
                atv.data = atv.data + horario

            atv.nome = atv.nome.replace("Tarefa: ", "", 1)

        atv.dia = int(atv.data.split('/')[0])
        atv.mes = int(atv.data.split('/')[1].split()[0])

        # Adiciona o Site na Atividade
        atv.setSite(site)

        return atv

    driver.get(linkSigaa)
    driver.find_element(By.CSS_SELECTOR,
                        ".logon > form:nth-child(2) > table:nth-child(8) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)")\
        .send_keys(login)
    driver.find_element(By.CSS_SELECTOR,
                        ".logon > form:nth-child(2) > table:nth-child(8) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)")\
        .send_keys(senha)
    driver.find_element(By.CSS_SELECTOR,
                        ".logon > form:nth-child(2) > table:nth-child(8) > tfoot:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > input:nth-child(1)")\
        .click()
    tabelaSig = driver.find_elements(By.CSS_SELECTOR,
                                     "#avaliacao-portal tbody tr:not(:first-child)")

    for el in tabelaSig:
        data = str(el.find_element(By.CSS_SELECTOR,"td:nth-child(2)").text)
        nome = str(el.find_element(By.CSS_SELECTOR,
                   "td:nth-child(3) > small").text)
        materia = str(nome.split("\n")[0])
        nome = nome.split("\n")[1]

        atv = PreparaAtv(Atividade(data, materia, nome), "(S)")
        VerData(atv)

    driver.get(linkMoodle)
    driver.find_element(By.CSS_SELECTOR,
                        "#username").send_keys(login)
    driver.find_element(By.CSS_SELECTOR,
                        "#password").send_keys(senha)
    driver.find_element(By.CSS_SELECTOR,
                        "#loginbtn").click()
    tabelaAva = driver.find_elements(By.CSS_SELECTOR,
                                     "div.event")

    for el in tabelaAva:
        # Pega as informações da atividade
        data = str(el.find_element(
            By.CSS_SELECTOR, "div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)").text)
        materia = str(el.find_element(
            By.CSS_SELECTOR, ".col-11 > [href^='https://ava.cefetmg.br/course/view.php']").text)
        nome = str(el.find_element(By.CSS_SELECTOR, "h3:nth-child(1)").text)
        atv = PreparaAtv(Atividade(data, materia, nome), "(M)")
        VerData(atv)
    return atvList   

def OrganizaTarefas(atvList:List[Atividade]) -> List[Atividade]:
    i=0
    while i < len(atvList):
        l=i+1
        while l < len(atvList):
            if atvList[i].mes>atvList[l].mes or atvList[i].dia>atvList[l].dia and atvList[i].mes==atvList[l].mes:
                atvList[i], atvList[l] = atvList[l], atvList[i]
            l+=1
        i+=1
    return atvList
    
def criaTexto(atvList:List[Atividade]) -> str:
    data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    texto = f"BOT🤖 / Arquivo criado em: {data}\n\n"
    for atv in atvList:
        texto = texto+str(atv)+"\n"
    
    return texto

def escreveTexto(texto:str):
    arq = open("/home/danilo/Documents/Prog/Atividades.txt", "w")
    arq.write(texto)
    arq.close()
    #mount('/dev/sdb3', '/media/danilo/win')
    try:
        shutil.copyfile("/home/danilo/Documents/Prog/Atividades.txt", "/media/danilo/9A3C5A963C5A6D6F/Users/danilo/Documents/Atividades.txt")
    except Exception: pass
    
def Whatsapp(): 
    sid= "ACbb62c4b3ae1f962f04e4dc0c32ce65de"
    token = ""
    client=Client(sid,token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=texto,
        to='whatsapp: '
    )

atvList = LogarSites(linkSigaa, linkMoodle)
atvList = OrganizaTarefas(atvList)
texto=criaTexto(atvList)
escreveTexto(texto)
Whatsapp()
print(texto)

# driver.quit()
