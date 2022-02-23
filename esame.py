
class ExamException(Exception):
    pass

class CSVTimeSeriesFile:

    def __init__(self, name):
        self.name = name
        
    def get_data(self):
        
        #verifico che il file sia leggibile
        try:
            my_file = open(self.name, 'r')
            s=my_file.readline()
        except Exception as e:
            self.can_read = False
            raise ExamException('Errore in apertura del file: "{}"'.format(e))

        data = []
        temp = []

        s = s.split(',')
        posmese=-1
        pospersone=-1
        pos=0

        #cerco le colonne dei dati
        for colonna in s:
            if colonna.lower().strip() == 'date':
                posmese=pos
            if colonna.lower().strip() == "passengers":
                pospersone=pos
            pos+=1
            
        if posmese==-1:
            raise ExamException('Errore, non esiste la colonna: date')
        if pospersone==-1:
            raise ExamException('Errore, non esiste la colonna: passengers')

        #creo la lista data
        for line in my_file:
        
            elements = line.split(',')
            try:
                elements[posmese] = elements[posmese].strip()
                elements[pospersone] = elements[pospersone].strip()

                if elements[posmese] != 'date':
            
                    temp.append(elements[posmese])
                    temp.append(elements[pospersone])
                    data.append(temp)
                    temp = []
            except:
                pass

        my_file.close()

        #verifico che la lista sia ordinata
        countmese = 1
        first=1

        for i in range (len(data)-1):
            if  len(data[i][0])!=7 or ((data[i][0])[5:7]).isnumeric()==False or ((data[i][0])[0:4]).isnumeric()==False or (data[i][0])[4] != '-':
                data.pop(i)
        for i in range (len(data)-1):

            if first != 1:
                if countmese == 1:
                    if int((data[i-1][0])[0:4])>=int((data[i][0])[0:4]) or int((data[i+1][0])[0:4])<int((data[i][0])[0:4]):
                        raise ExamException('Errore, lista non ordinata')
                    if int((data[i-1][0])[5:7])>12 or int((data[i+1][0])[5:7])>12:
                        raise ExamException('Errore, lista non ordinata')
                    countmese = int((data[i+1][0])[5:7])
                elif countmese == 12:
                    if int((data[i-1][0])[0:4])>int((data[i][0])[0:4]) or int((data[i+1][0])[0:4])<=int((data[i][0])[0:4]):
                        raise ExamException('Errore, lista non ordinata')
                    if int((data[i-1][0])[5:7])>12 or int((data[i+1][0])[5:7])>12:
                        raise ExamException('Errore, lista non ordinata')
                    countmese=int((data[i+1][0])[5:7])
                else :
                    print(int((data[i-1][0])[5:7]))
                    if int((data[i-1][0])[0:4])>int((data[i][0])[0:4]) or int((data[i+1][0])[0:4])<int((data[i][0])[0:4]):
                        raise ExamException('Errore, lista non ordinata')
                    if (int((data[i][0])[0:4])==int((data[i+1][0])[0:4]) and int((data[i][0])[0:4])==int((data[i-1][0])[0:4]) ) and (int((data[i-1][0])[5:7])>=int((data[i][0])[5:7]) or int((data[i+1][0])[5:7])<=int((data[i][0])[5:7])):
                        raise ExamException('Errore, lista non ordinata')
                    if int((data[i+1][0])[5:7])>12:
                        raise ExamException('Errore, lista non ordinata')
                    countmese=int((data[i+1][0])[5:7])
                        
            if first == 1:
                if int((data[i+1][0])[0:4])<int((data[i][0])[0:4]):
                    raise ExamException('Errore, lista non ordinata')
                if int((data[i+1][0])[5:7])>12:
                    raise ExamException('Errore, lista non ordinata')
                countmese = int((data[i+1][0])[5:7])
                first=0

        #verifico che il dato nella colonna dei passeggeri sia un numero positivo
        for passeggeri in data:
            if not passeggeri[1].isnumeric():
                passeggeri[1]=-1



        return data

def detect_similar_monthly_variations(time_series, years):

    first_year=years[0]
    last_year=years[1]
    
    if int(first_year)>int(last_year):
        temp=last_year
        last_year=first_year
        first_year=temp
    
    if int(first_year)!=int(last_year)-1:
        raise ExamException('Errore, i due anno dati in input non sono consecutivi')
    if isinstance(type(first_year), str):
        raise ExamException('Errore, first_year non è stato dato come stringa')
    if isinstance(type(first_year), str):
        raise ExamException('Errore, last_year non è stato dato come stringa')

    #verifico che i due anni siano presenti nella lista
    check1 = 0
    check2 = 0
    for dato in time_series:
        if first_year in dato[0]:
            check1 = 1
        if last_year in dato[0]:
            check2 = 1

    if check1 == 0:
        raise ExamException('Errore, first_year non è presente nella lista')
    if check2 == 0:
        raise ExamException('Errore, last_year non è presente nella lista')

    primo_anno=int(first_year)
    ultimo_anno=int(last_year)
    nanni = ultimo_anno-primo_anno+1
    output = []

    anno1=[None,None,None,None,None,None,None,None,None,None,None,None]
    anno2=[None,None,None,None,None,None,None,None,None,None,None,None]

    for dato in time_series:
        if dato[0][0:4]==first_year:
            if dato[1]!=-1:
                anno1[int(dato[0][5:7])-1]=int(dato[1])
            else:
                anno1[int(dato[0][5:7])-1]=None
    for dato in time_series:
        if dato[0][0:4]==last_year:
            if dato[1]!=-1:
                anno2[int(dato[0][5:7])-1]=int(dato[1])
            else:
                anno2[int(dato[0][5:7])-1]=None

    listadifferenza=[[],[]]
    for i in range( 11 ):
        if anno1[i+1]!= None and anno1[i]!= None:
            listadifferenza[0].append(abs(anno1[i+1]-anno1[i]))
        else:
            listadifferenza[0].append(None)
    for i in range( 11 ):
        if anno2[i+1]!= None and anno2[i]!= None:
            listadifferenza[1].append(abs(anno2[i+1]-anno2[i]))
        else:
            listadifferenza[1].append(None)

    variazione=[]
    print (listadifferenza)
    for i in range (11):
        if listadifferenza[0][i]!=None and listadifferenza[1][i]!=None:
            if abs(listadifferenza[0][i] - listadifferenza[1][i])<=2:
                variazione.append(True)
            else:
                variazione.append(False)
        else:
            variazione.append(False)
    return variazione

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
#print('Nome del file: "{}"'.format(time_series_file.name))
#print('Dati contenuti nel file: \n"{}"'.format(time_series_file.get_data()))

#print('\nOutput: "{}"' .format(compute_avg_monthly_difference(time_series, "1949", "1951")
print(detect_similar_monthly_variations(time_series, ["1950", "1951"]))

