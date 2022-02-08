class CSVTimeSeriesFile:

    def __init__(self, name):
        self.name = name

    def get_data(self):
        
        data = []
        my_file = open(self.name, 'r')

        #ricerca colonna data e passengers
        for line in my_file:
        
            elements = line.split(',')
            elements[0] = elements[0].strip()
            elements[1] = elements[1].strip()
        
            if elements[0] != 'date':
            
                data.append(elements)

        my_file.close()

        return data

def compute_avg_monthly_difference(time_series, first_year, last_year):

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
        for j in range(1, nanni):
            media+=int(listaanno[-j][i])-int(listaanno[-j-1][i])
            print(j)
            print ('\n----: "{}"'.format(listaanno[-j][i]))
            print ('-: "{}"'.format(listaanno[-j-1][i]))
        print ('****: "{}"'.format(media))      
        print ('****: "{}"'.format(nanni-1)) 
        print ('****: "{}"'.format(media/(nanni-1)))     
        listamedia.append(round((media/(nanni-1)), 2))
            
            
    return listamedia

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print('Nome del file: "{}"'.format(time_series_file.name))
#print('Dati contenuti nel file: \n"{}"'.format(time_series_file.get_data()))

print('\nOutput: "{}"' .format(compute_avg_monthly_difference(time_series, "1949", "1951")))