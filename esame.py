
class ExamException(Exception):
    pass
#raise ExamException('Errore, lista valori vuota')
class CSVTimeSeriesFile:

    def __init__(self, name):
        self.name = name
        
    def get_data(self):
        
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
        for colonna in s:
            print(colonna)
            if colonna.lower().strip() == 'date':
                posmese=pos
            if colonna.lower().strip() == "passengers":
                pospersone=pos
            pos+=1
            
        if posmese==-1:
            raise ExamException('Errore, non esiste la colonna: date')
        if pospersone==-1:
            raise ExamException('Errore, non esiste la colonna: passengers')

        for line in my_file:
        
            elements = line.split(',')

            elements[posmese] = elements[posmese].strip()
            elements[pospersone] = elements[pospersone].strip()

            
            if elements[posmese] != 'date':
            
                temp.append(elements[posmese])
                temp.append(elements[pospersone])
                data.append(temp)
                temp = []

        print (data)
        my_file.close()
        countmese = 1
        first=1

        for i in range (len(data)-1):
            if  (data[i][0])[4] != '-':
                raise ExamException('Errore, formato data deverso da yyyy-mm')

            if first != 1:

                if countmese == 1:
                    if int((data[i-1][0])[0:4])>=int((data[i][0])[0:4]) or int((data[i+1][0])[0:4])<int((data[i][0])[0:4]):
                        raise ExamException('Errore, lista non ordinata')
                    if int((data[i-1][0])[5:7])!=12 or int((data[i+1][0])[5:7])!=2:
                        raise ExamException('Errore, lista non ordinata')
                    countmese = 2
                elif countmese == 12:
                    if int((data[i-1][0])[0:4])>int((data[i][0])[0:4]) or int((data[i+1][0])[0:4])<=int((data[i][0])[0:4]):
                        raise ExamException('Errore, lista non ordinata')
                    if int((data[i-1][0])[5:7])!=11 or int((data[i+1][0])[5:7])!=1:
                        raise ExamException('Errore, lista non ordinata')
                    countmese=1
                else :
                    if int((data[i-1][0])[0:4])>int((data[i][0])[0:4]) or int((data[i+1][0])[0:4])<int((data[i][0])[0:4]):
                        raise ExamException('Errore, lista non ordinata')
                    if int((data[i-1][0])[5:7])>int((data[i][0])[5:7]) or int((data[i+1][0])[5:7])<int((data[i][0])[5:7]):
                        raise ExamException('Errore, lista non ordinata')
                    countmese+=1
                    
            if first == 1:
                if int((data[i+1][0])[0:4])<int((data[i][0])[0:4]):
                    raise ExamException('Errore, lista non ordinata')
                if int((data[i+1][0])[5:7])!=2:
                    raise ExamException('Errore, lista non ordinata')
                countmese = 2
                first=0

        for passeggeri in data:
            if not passeggeri[1].isnumeric():
                passeggeri[1]=0



        return data

def compute_avg_monthly_difference(time_series, first_year, last_year):

    if isinstance(type(first_year), str):
        raise ExamException('Errore, first_year non è stato dato come stringa')
    if isinstance(type(first_year), str):
        raise ExamException('Errore, last_year non è stato dato come stringa')

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

    lista = []
    listaanno = []
    for i in range(nanni):
        listaanno.append([])
    

    for dato in time_series:
        if int(dato[0][0:4])>=primo_anno and int(dato[0][0:4])<=ultimo_anno:
            lista.append(dato)

    anno = int(lista[0][0][0:4])
    i=0
    for dato in lista:
        
        if int(dato[0][0:4])==anno:
            listaanno[i].append(dato[1])
        else:
            anno = int(dato[0][0:4])
            i+=1
            listaanno[i].append(dato[1])
        
    
    print ('\n----: "{}"'.format(listaanno))

    listamedia=[]
    
    for i in range(12):
        media=0.0
        annidivisione=0
        for j in range(1, nanni):
            print("---------------------")
            if int(listaanno[-j][i]) != 0 :
                print ('numero passeggeri last: "{}"'.format(listaanno[-j][i])) 
                for z in range (j+1, nanni+1):
                    if int(listaanno[-z][i]) != 0:
                        print ('numero passeggeri first: "{}"'.format(listaanno[-z][i])) 
                        media+=int(listaanno[-j][i])-int(listaanno[-z][i])
                        annidivisione+=1
                        break

                

        print ('****: "{}"'.format(media))      
        print ('****: "{}"'.format(nanni-1)) 
        print ('****: "{}"'.format(media/(annidivisione)))     
        listamedia.append(round((media/(annidivisione)), 2))
            
            
    return listamedia

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print('Nome del file: "{}"'.format(time_series_file.name))
#print('Dati contenuti nel file: \n"{}"'.format(time_series_file.get_data()))

print('\nOutput: "{}"' .format(compute_avg_monthly_difference(time_series, "1954", "1958")))