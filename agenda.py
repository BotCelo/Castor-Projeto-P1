import sys
import ctypes, sys
TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'
def printCores(texto, cor):
  print(cor + texto + RESET)
def adicionar(descricao, extras):
  data = ""
  hora = ""
  prioridade = ""
  contexto = ""
  projeto = ""
  descricao = descricao + " "
  for x in extras:
    if dataValida(x) == True:
      data = x + " "
    if horaValida(x) == True:
      hora = x + " "
    if prioridadeValida(x) == True:
      prioridade = x + " "
    if contextoValido(x) == True:
      contexto = x + " "
    if projetoValido(x) == True:
      projeto = x + " "
    novaAtividade = data + hora + prioridade + descricao + contexto + projeto
  if descricao == "":
    return False
  try:
    fp = open(TODO_FILE, "a", encoding='utf-8-sig')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo" + TODO_FILE)
    print(err)
    return False
  return True
  
      
def prioridadeValida(pri):
    lista = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","ç","z","x","c","v","b","n","m"]
    prioridade = pri.lower()
    if len(prioridade) == 3:
      if prioridade[0] != "(" or prioridade[2] != ")":
          return False
      elif prioridade[1] not in lista:
          return False
      else:
          return True
    else:
        return False

def horaValida(horaMin):
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
      hora = horaMin[0] + horaMin[1]
      hora = int(hora)
      minuto = horaMin[2] + horaMin[3]
      minuto = int(minuto)
      if hora >= 00 and hora <= 23 and minuto >= 00 and minuto <= 59:
          return True
      else:
          return False
      
def dataValida(data):
    if len(data) != 8:
        return False
    if not soDigitos(data):
        return False
    else:
        dia = int(data[0] + data[1])
        mes = int(data[2] + data[3])
        ano = int(data[4] + data[5] + data[6] + data[7])
        if mes == 2 and dia > 28 or dia < 1:
            return False
        elif (mes == 4 or mes == 6 or mes == 9 or mes == 11) and dia > 30 or dia < 1:
            return False 
        elif dia > 31 or dia < 1:
            return False
        elif mes > 12 or mes < 1:
            return False
        elif ano >= 0 and ano <= 9999:
            return True
                    
def projetoValido(proj):
    if len(proj) < 2:
        return False
    elif proj[0] != "+":
        return False
    else:
        return True
    
    return False
def contextoValido(cont):
    if len(cont) < 2:
        return False
    elif cont[0] != "@":
        return False
    else:
        return True
    
def soDigitos(numero):
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True

def organizar(linhas):

  itens = []
  for l in linhas:
    data = ''
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    ################ COMPLETAR
    for x in tokens:
        if dataValida(x) == False and horaValida(x) == False and prioridadeValida(x) == False and contextoValido(x) == False and projetoValido(x)== False:
            desc = desc + x + " "
        else:
          if dataValida(x) == True: 
              if desc != "": # tentar explicar pro professor que esse if
                             # significa que descrição não estar vazia
                             # implica em data inválida, visto que elas apaercem
                             # antes da descrição
                        
                desc = desc + x + " "
              else:
                data = x
          if horaValida(x) == True:
              if desc != "":
                desc = desc + x + " "
              else:
                hora = x
          if prioridadeValida(x) == True:
            if desc != "":
              desc = desc + x + " "
            else:
               pri = x
               
          if contextoValido(x) == True:
              contexto = x
          if projetoValido(x) == True:
              projeto = x
    if desc != "":
      desc = desc.strip()
      itens.append((desc, (data, hora, pri, contexto, projeto)))
    if desc == "":
      desc = data + " " + hora + " " + pri + " " + contexto + " " + contexto + " " + projeto
      itens.append((desc, ("", "", "", "", "")))
      
      
  return itens

def listar():
  arqv = open(TODO_FILE, "r", encoding='utf-8-sig')
  linhas = arqv.readlines()
  arqv.close
  atividades = organizar(linhas)
  atividades = ordenarPorPrioridade(atividades)
  atividades = ordenarPorDataHora(atividades)
  i = 1
  for x in atividades:
    numeroAtividade = str(i)
    if x[1][0] != "":
      dia = x[1][0]
      dia = dia[0:2] + "/" + dia[2:4] + "/" + dia[4:] + " "
    else:
      dia = ""
    if x[1][1] != "":
      horaMin = x[1][1]
      horaMin = horaMin[0:2] + "h" + horaMin[2:] + "m" + " "
    else:
      horaMin = ""
    if x[1][2] != "":
      pri = x[1][2] + " "
    else:
      pri = ""
    desc = x[0] + " "
    if x[1][3] != "":
      lugar = x[1][3] + " "
    else:
      lugar = ""
    if x[1][4] != "":
      projeto = x[1][4] + " "
    else:
      projeto = ""
    i = i + 1
      
    x = numeroAtividade + " " + dia + horaMin + pri + desc + lugar + projeto
    if pri == "(A) ":
      printCores(x, REVERSE+RED)
    if pri == "(B) ":
      printCores(x, CYAN)
    if pri == "(C) ":
      printCores(x, BLUE)
    if pri == "(D) ":
      printCores(x, GREEN)
    if pri != "(A) " and pri != "(B) " and pri != "(C) " and pri != "(D) ":
      print(x)

  return   #atividades
    #essa função n retorna nada, mas eu usei o return pra testar
  


def ordenarPorDataHora(itens):
    indice = []
    itensOrdenados = []
    for x in range(len(itens)):
      indice.append(["","","",""])
      indice[x][0] = x
      if itens[x][1][2] == "":
         indice[x][1] = "ZZ"
      else:
        indice[x][1] = itens[x][1][2]
      if itens[x][1][0] == "":
         indice[x][2] = "ZZZZZZZZ"
      else:
        data = itens[x][1][0]
        ano = data[4:]
        mes = data[2:4]
        dia = data[0:2]
        indice[x][2] = ano + mes + dia
      if itens[x][1][1] == "":
        indice[x][3] = "ZZZZ"
      else:
        indice[x][3] = itens[x][1][1]

    indice = sorted(indice, key=lambda x:(x[1],x[2],x[3]))  
    for x in range(len(indice)):
    #print(itens[indice[x][0]])
          itensOrdenados.append(itens[indice[x][0]]) #pega número da linha que está sempre na posição 0 de qualquer linhas, tal que a linha é percorrida no for range
    return itensOrdenados
  
def ordenarPorPrioridade(itens):
  indice = []
  itensOrdenados = []
  for x in range(len(itens)):
    indice.append(["","","",""])
    indice[x][0] = x
    if itens[x][1][2] == "":
       indice[x][1] = "(ZZ)"
    else:
      indice[x][1] = itens[x][1][2]

    indice = sorted(indice, key=lambda x:(x[1]))  
  for x in range(len(indice)):
    #print(itens[indice[x][0]])
    itensOrdenados.append(itens[indice[x][0]])
  return itensOrdenados

def fazer(num):
  linhas1 = []
  arqv = open(TODO_FILE, "r", encoding='utf-8-sig')
  linhas = arqv.readlines()    
  arqv.close()
  atividades = organizar(linhas)
  atividades = ordenarPorPrioridade(atividades)
  atividades = ordenarPorDataHora(atividades)
  i = 1
  for x in atividades:
    linhas1.append(x[1][0] + " " + x[1][1] + " " + x[1][2] + " " + x[0] + " " + x[1][3] + " " + x[1][4])
  for x in range(len(linhas1)+1):
    if x == num:
      linhaPop = linhas1.pop(x-1)
      arqv = open("done.txt", "a+", encoding = 'utf-8-sig')
      linhaPop = linhaPop.strip()
      arqv.write(linhaPop + "\n")
      arqv.close()
      remover(x)
    i = i + 1
       
def remover(num):
  print(num)
  linhas2 = []
  arqv = open(TODO_FILE, "r", encoding='utf-8-sig')
  linhas = arqv.readlines()    
  arqv.close()
  atividades = organizar(linhas)
  atividades = ordenarPorPrioridade(atividades)
  atividades = ordenarPorDataHora(atividades)
  i = 1
  for x in atividades:
    linhas2.append(x[1][0] + " " + x[1][1] + " " + x[1][2] + " " + x[0] + " " + x[1][3] + " " + x[1][4])
  for x in range(len(linhas2)+1):
      if i == num:
         linhas2.pop(i-1)
         arqv = open(TODO_FILE, "w", encoding='utf-8-sig')
         for x in linhas2:
           x = x.strip()
           arqv.write(x + "\n")
         arqv.close()
      i = i + 1
       
 # return
def priorizar(num, prioridade):
  if prioridadeValida(prioridade) == False:
    print("Prioridade inválida")
  else:
    linhas3 = []
    arqv = open(TODO_FILE, "r", encoding='utf-8-sig')
    linhas = arqv.readlines()    
    arqv.close()
    atividades = organizar(linhas)
    atividades = ordenarPorPrioridade(atividades)
    atividades = ordenarPorDataHora(atividades)
    for x in range(len(atividades)):
      if x != num:
        linhas3.append(atividades[x][1][0] + " " + atividades[x][1][1] + " " + atividades[x][1][2] + " " + atividades[x][0] + " " + atividades[x][1][3] + " " + atividades[x][1][4])
      else:
        linhas3.append(atividades[x][1][0] + " " + atividades[x][1][1] + " " + prioridade + " " + atividades[x][0] + " " + atividades[x][1][3] + " " + atividades[x][1][4])
    arqv = open(TODO_FILE, "w", encoding = 'utf-8-sig')
    for x in linhas3:
       arqv.write(x + "\n")
    arqv.close()
        
    return
def processarComandos(comandos):
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    listar()
    ################ COMPLETAR

  elif comandos[1] == REMOVER:
    remover(int(comandos[2]))

    ################ COMPLETAR    

  elif comandos[1] == FAZER:
    fazer(int(comandos[2]))

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    priorizar(int(comandos[2]),comandos[3])    

    ################ COMPLETAR

  else :
    print("Comando inválido.")

#verifica se existe mais de um parâmetro na linha de comando pra ñ dar indexação
if len(sys.argv) > 1:
  processarComandos(sys.argv)
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
#processarComandos(sys.argv)


    
