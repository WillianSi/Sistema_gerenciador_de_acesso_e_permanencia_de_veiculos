from asyncio.windows_events import NULL
import mysql.connector
from mysql.connector import errorcode
import pytesseract
import cv2
import datetime

def desenhaContornos(contornos, imagem):
    for c in contornos:
        # perimetro do contorno, verifica se o contorno é fechado
        perimetro = cv2.arcLength(c, True)
        if perimetro > 120:
            # aproxima os contornos da forma correspondente
            approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            # verifica se é um quadrado ou retangulo de acordo com a qtd de vertices
            if len(approx) == 4:
                # Contorna a placa atraves dos contornos encontrados
                (x, y, lar, alt) = cv2.boundingRect(c)
                cv2.rectangle(imagem, (x, y), (x + lar, y + alt), (0, 255, 0), 2)
                # segmenta a placa da imagem
                roi = imagem[y:y + alt, x:x + lar]
                cv2.imwrite("output/roi.png", roi)

def buscaRetanguloPlaca(source):
    # Captura ou Video
    video = cv2.VideoCapture(source)
    while video.isOpened():

        ret, frame = video.read()

        if (ret == False):
            break


        # area de localização u 720p
        area = frame[500:, 300:800]

        # area de localização 480p
        # area = frame[350:, 220:500]

        # escala de cinza
        img_result = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

        # limiarização
        ret, img_result = cv2.threshold(img_result, 90, 255, cv2.THRESH_BINARY)

        # desfoque
        img_result = cv2.GaussianBlur(img_result, (5, 5), 0)
        
        cv2.imshow('RES', img_result)

        # lista os contornos
        contornos, hier = cv2.findContours(img_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # limite horizontal
        cv2.line(frame, (0, 500), (1280, 500), (0, 0, 255), 1)
        # limite vertical 1
        cv2.line(frame, (300, 0), (300, 720), (0, 0, 255), 1)
        # limite vertical 2
        cv2.line(frame, (800, 0), (800, 720), (0, 0, 255), 1)

        cv2.imshow('FRAME', frame)

        desenhaContornos(contornos, area)

        cv2.imshow('RES', area)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    video.release()
    preProcessamentoRoi()
    cv2.destroyAllWindows()

def preProcessamentoRoi():
    img_roi = cv2.imread("output/roi.png")
    # cv2.imshow("ENTRADA", img_roi)
    if img_roi is None:
        return

    # redmensiona a imagem da placa em 4x
    img = cv2.resize(img_roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # Converte para escala de cinza
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Escala Cinza", img)

    # Binariza imagem
    _, img = cv2.threshold(img, 56, 255, cv2.THRESH_BINARY)
    cv2.imshow("Limiar", img)

    # Desfoque na Imagem
    img = cv2.GaussianBlur(img, (5, 5), cv2.BORDER_REFLECT101)
    # cv2.imshow("Desfoque", img)

    # Aplica reconhecimento OCR no ROI com o Tesseract
    cv2.imwrite("output/roi-ocr.png", img)

    return img

def reconhecimentoOCR():
    img_roi_ocr = cv2.imread("output/roi-ocr.png")
    if img_roi_ocr is None:
        return
    #Executa o tesseract
    caminho = r'C:\Users\Willian Silvestre\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = caminho
    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'
    saida = pytesseract.image_to_string(img_roi_ocr, lang='eng', config=config)

    # Leitura da placa como saida
    return saida

def validate_plate(plate, authorized_plate):
    #Verifica se a placa está no vetor de authorized_plate e faz um retorno
    if plate in authorized_plate:
        return 'Autorizado'
    else:
        return 'Não autorizado'

def procurado_plate(plate, search_place):
    #Verifica se a placa está no vetor de search_place e faz um retorno
    if plate in search_place:
        return 'Procurado'
    else:
        return 'Não procurado'

def date_veiculo(numero, plates):
    if numero in plates:
        #Pega a data e hora de saidaa e salva no banco
        agora = datetime.datetime.now()
        dataSaida = agora.strftime("%d/%m/%Y")
        horaSaida = agora.strftime("%H : %M")
        plates.remove(numero)
        #Cria um select na tabelas carros
        sql_select_Query = "select * from carros"
        # MySQLCursorDict cria um cursor que retorna linhas como dicionários
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            idCarros = row["idCarros"]
            placa = row["placa"]
            if (placa == numero):
                print("ent")
                update_horaSaida = ("UPDATE carros SET horaSaida = '"+horaSaida+"'  WHERE idCarros = '"+str(idCarros)+"'")
                update_dataSaida = ("UPDATE carros SET dataSaida = '"+dataSaida+"'  WHERE idCarros = '"+str(idCarros)+"'")
                cursor.execute(update_horaSaida)
                cursor.execute(update_dataSaida)
                db_connection.commit()
           
    else:
        #Pega a data e hora de entrada e salva no banco
        agora = datetime.datetime.now()
        horaEntrada = agora.strftime("%H : %M")
        dataEntrada = agora.strftime("%d/%m/%Y")
        plates.append(numero)
        #Cria um select na tabelas carros
        sql_select_Query = "select * from carros"
        # MySQLCursorDict cria um cursor que retorna linhas como dicionários
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            idCarros = row["idCarros"]
            placa = row["placa"]
            if (placa == numero):
                update_horaEntrada = ("UPDATE carros SET horaEntrada = '"+horaEntrada+"'  WHERE idCarros = '"+str(idCarros)+"'")
                update_dataEntrada = ("UPDATE carros SET dataEntrada = '"+dataEntrada+"'  WHERE idCarros = '"+str(idCarros)+"'")
                cursor.execute(update_horaEntrada)
                cursor.execute(update_dataEntrada)
                db_connection.commit()

def permanence_veiculo():
        #Cria um select na tabelas carros
        sql_select_Query = "select * from carros"
        # MySQLCursorDict cria um cursor que retorna linhas como dicionários
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        #Contador de carros permanentes
        cont = 0
        print("Carros permanentes:")
        #for que salva em uma variavel os dados das colunas da tabela
        for row in records:
            placa = row["placa"]
            horaEntrada = row["horaEntrada"]
            dataEntrada = row["dataEntrada"]
            dataSaida = row["dataSaida"]
            veiculoOficial = row["veiculoOficial"]
            veiculoProcurado = row["veiculoProcurado"]
            #if em que se a dataSaida for None eles printa as informaçãoes das variaveis
            if (dataSaida == None):
                cont += 1
                print("\n")
                print("----- CARRO ",cont,"-----")
                print("Veiculo: " , placa, "\nHora de entrada: ", horaEntrada, "\nData de entrada: ", dataEntrada,"\nOficial: ", veiculoOficial,"\nProcurado: ", veiculoProcurado)

        print("\nNumero total de veiculos permanecentes: ", cont, "\n")
        print("---------------------------------")

def daily_report():
    #input para verificar se irá mesmo querer o relatorio
    relatorio = input("Você desseja um relatorio do dia (s/n): ")
    if (relatorio == 's' or relatorio == 'S' or relatorio == 'sim' or relatorio == 'Sim'):
        print("Relatorios:")
        #for que salva em uma variavel os dados das colunas da tabela para printa as informaçãoes das variaveis
        for row in records:
            idCarros = row["idCarros"]
            placa = row["placa"]
            horaEntrada = row["horaEntrada"]
            horaSaida = row["horaSaida"]
            dataEntrada = row["dataEntrada"]
            dataSaida = row["dataSaida"]
            veiculoOficial = row["veiculoOficial"]
            veiculoProcurado = row["veiculoProcurado"]

            print("\n")
            print("----- CARRO ", idCarros,"-----")
            print("Veiculo: " , placa, "\nHora de entrada: ", horaEntrada, "\nData de entrada: ", dataEntrada, "\nHora de saida: ", horaSaida, "\nData de saida: ", dataSaida,"\nOficial: ", veiculoOficial,"\nProcurado: ", veiculoProcurado)
    print("---------------------------------")

if __name__ == "__main__":
   
   #Abrindo conexão com o banco
    try:
        db_connection = mysql.connector.connect(host='localhost', user='root', password='2bF83Jz@7', database='projetoCompGrafica')
        print("Banco de Dados Conectado!")
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco de Dados Nao existe")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Seu Nome ou Senha Esta Errado")
        else:
            print(error)

    cursor = db_connection.cursor()

    #Chamado o video
    source = "resource/video720p.mkv"

    #Vetor de placas autorizadas
    authorized_plate = ['FUN-0972', 'BRA2E19']
    #Vetor de placas procuradas
    search_place = ['FUN-0972','OJJ3984']
    #Vetor de placas
    plates = ['FUN-0972']
    
    #Chamada da função buscaRetanguloPlaca passando o video
    #buscaRetanguloPlaca(source)
    #Chamada da função preProcessamentoRoi passando a imagem da placa
    #preProcessamentoRoi()
    #Chamada da função reconhecimentoOCR passando e salva seu retorno na variavel numero
    numero = reconhecimentoOCR()
    #Tira a quebra de linha da variavel numero
    numero = numero.strip('\n')   
    #For para chamar a função validate_plate e verificar se é um veiculo ificial
    for i in range(len(plates)):
        oficialVeiculo = validate_plate(plates[i], authorized_plate)
    #For para chamar a função procurado_plate e verificar se é um veiculo procurado
    for i in range(len(plates)):
        procuradoVeiculo = procurado_plate(plates[i], search_place)
    
    #Cria um select na tabelas carros
    sql_select_Query = "select * from carros"
    # MySQLCursorDict cria um cursor que retorna linhas como dicionários
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    #Inserindo valores no banco
    for row in records:
        pl = row["placa"]
        if (numero != pl):
            inserir_valores = ("INSERT INTO carros (idCarros, placa, veiculoOficial, veiculoProcurado) VALUES (null,'" +numero+"','" +oficialVeiculo+"','"+procuradoVeiculo+"') ")
            cursor.execute(inserir_valores)
            db_connection.commit()
            break

    #Chamada da função date_veiculo para saber se o veiculo está saindo ou entrando
    date_veiculo(numero,plates)

    #Pega a hora do sistema
    agoraH = datetime.datetime.now()
    horaAgora = agoraH.strftime("%H")
    #if chamada da função permanence_veiculo para saber quantos e quais veiculos permanecem no campus
    if (horaAgora == '22'):
        permanence_veiculo()
    #if chamada da função daily_report para obter um relatorio veiculos no banco
    if (horaAgora == '22'): 
        daily_report()

    #Fecha a conexão com o banco
    db_connection.close()