import pandas as pd
from scipy.signal import argrelextrema
import numpy as np
from matplotlib import pyplot as plt
import os

timestamp_file_name = "HPKR00030_2cicli_OV3_time.csv"                           # nome del file con i timestamp del trigger
 # definisco l'indirizzo, os.path.join() unisce un indirizzo base al nome di un file specifico
timestamp_path = os.path.join(os.getcwd(),timestamp_file_name)                  # getcwd() restituisce l'indirizzo della cartella nella quale è contenuto questo programma
                                                                                # (da sostituire con il path della cartella in cui sono i dati)
timestamp_table = pd.read_csv(timestamp_path)                                   # leggo i dati relativi ai timestamp del trigger, disponendoli in un dataframe
                                                                                # timestamp_table.head(10) per visualizzare i dati ottenuti
# rinomino le colonne, Event è un indice che va da 1 a 1000 (numero di eventi), mentre Delta T è il tempo trascorso dal trigger precedente
timestamp_table.rename(columns = {'X: (s)': 'Event', 'Y: (Hits)':'Timestamp'}, inplace = True)
N_of_events = len(timestamp_table)                                              # Numero di waveforms (o eventi), che corrisponde al numero di eventi di trigger
# .diff effettua la somma cumulativa di ogni riga con quelle precedente
timestamp_table["Timestamp"] = timestamp_table["Timestamp"].cumsum(axis=0)      # axis identifica l'asse, se lungo le righe (0) o lungo le colonne (1)
wf_data_points = 0                                                              # inizializzo la variabile wf_data_point che corrisponde al numero di punti in ogni waveform (6250)
# definisco il nome del file con i dati delle waveforms, questi dati sono posti in modo contiguo ovvero in un unico file csv
wf_file_name = "HPKR00030_2cicli_OV3_wf.csv"                                    # dividendo le righe in gruppi da 6250 elementi possiamo ottenere le singole waveforms
wf_path = os.path.join(os.getcwd(),wf_file_name)                                # stesso discorso del timestamp
wf_table = pd.DataFrame()                                                       # definisco un dataframe per le waveforms

with open(wf_file_name, 'r') as file_wf:                                        # apro il file e inserisco le righe in una lista
    lines = file_wf.readlines()
    for line_counter, line in enumerate(lines):                                 # cerco la riga che inizia per TIME ma prima cerco Record Lenght per ottenere il valore di wf_data_point
        if line.startswith("Record Length"): wf_data_points = int(line.split(',')[-1])
                                                                                # un altro modo per ottenere N_of_events sarebbe cercare la riga che contiene il numero di frames ("FastFrame Count,1000")
        if line.startswith("TIME"):
            wf_table = pd.read_csv(wf_path, header = line_counter-1)              # inizializzo il dataframe
            break                                                               # esco dal ciclo

# metodo usato a lezione (meno elegante ma funziona comunque, riportato giusto per completezza)
# line_counter = 0
# n_line = -1
# while n_line == -1:
#     line = waveform_file.readline()
#     line_counter += 1
#     if line_counter == 100:
#         print("ERROR")
# waveform_table = pd.read_csv("HPKR00030_2cicli_OV3_wf.csv", header = n_line-1)

# il per il calcolo dei timestamp, allo stesso modo, è più elegante di quello trattato a lezione, che riporto qui sotto per completezza
# timestamp_table.at[0,'Timestamp'] = timestamp_table.iloc[0]['Delta T']
# for i in timestamp_table.index[1:]:
#     timestamp_table.at[i,"Timestamp"] = timestamp_table.at[i-1,"Timestamp"] + timestamp_table.at[i,"Delta T"]

# funzione di analisi per la ricerca dei minimi
def analysis(timestamp_table, wf_table,wf_datapoints):
# inizializzo un dataframe generale
    general_min_list = []
    for n in range(N_of_events):
# end = '\r' inserisce \r alla fine della stringa, quindi riporta il puntatore all'inizio della riga in modo da sovrascrivere l'output precedente
        print("Analizzando l'evento numero " + str(n), end='\r')
# nome del singolo evento analizzato in questa iterazione del ciclo
        event_name = 'Event_' + str(n) + '.png'
# prima di estrarre i punti relativi alla singola waveform, convertiamo i tempi relativi in tempi assoluti
# la colonna "TIME" contiene, per ogni waveform, i tempi relativi all'evento di trigger che ha avviato l'acquisizione della waveform
# per convertire questi tempi relativi in tempi assoluti (o meglio relativi all'inizio della misura) dobbiamo aggiungere ai tempi di ogni waveform il corrispondente timestamp del trigger
        wf_table["TIME"].loc[wf_datapoints*n: (wf_datapoints*(n+1))-1] += timestamp_table.at[n,"Timestamp"]
# estraggo una singola waveform, ovvero 6250 punti, dalla tabella principale
        single_wf = wf_table.loc[wf_datapoints*n: (wf_datapoints*(n+1))-1].copy()
# la funzione argrelextrema restituisce gli estremi relativi, calcolati in base all'operatore np.less_equal
# aumentando l'ordine diminuiamo il numero di minimi trovati.
# Il range totale di punti viene suddiviso in intervalli di lunghezza proporzionale a "order", successivamente viene estratto il minimo assoluto di ogni intervall.
# i minimi così trovati sono i minimi relativi restituiti dalla funzione argrelextrema
        minimum_list = argrelextrema(single_wf.CH1.values, np.less_equal, order = 50)[0]
# la riga seguente serve per identificare i minimi ed inserirli nella singola waveform, in modo da vederli nei plot
        single_wf.loc[:,'min'] = single_wf.iloc[minimum_list]['CH1']
# eseguo un fit di ordine 0 (quindi una media) sui primi 250 punti, che rientrano nella zona di pre-trigger (ovvero i punti precedenti all'evento di trigger)
        baseline = np.polyfit(single_wf["TIME"].iloc[0:250], single_wf["CH1"].iloc[0:250],0)[0]
# definisco una lista di minimi "buoni" da riempire in seguito
        clean_minimum_list = []
# i minimi saranno considerati buoni se hanno ampiezza superiore a 0.006, rispetto alla baseline
        gap = 0.006
        previous_index = minimum_list[0]
        for index in minimum_list:
# un controllo sugli indici previene massimi vicini (provate a togliere and (index > previous_index + 50) e vedete cosa succede)
            if (baseline - single_wf["CH1"].iat[index] > gap) and (index > previous_index + 50):
                clean_minimum_list.append(index)
                previous_index = index
# aggiungo una colonna di minimi "buoni" alla tabella
        single_wf.loc[:,'clean_min'] = single_wf.iloc[clean_minimum_list]['CH1']
# l'indice corrispettivo sulla tabella principale è sfasato di un valore n*6250
        wf_index = (n*wf_datapoints)
        for index in clean_minimum_list:
            general_min_list.append(index + wf_index)
# le seguenti linee di comando servono per graficare le singole waveforms
# !!!!!!!!! attenzione al numero di cicli nel for, altrimenti aprite 6250 grafici !!!!!!!!!
        plt.plot(single_wf["TIME"], single_wf['CH1'], linestyle="-", linewidth=1)
        plt.scatter(single_wf["TIME"], single_wf['min'], color="darkred")
        plt.scatter(single_wf["TIME"], single_wf['clean_min'], color="green")
        plt.axhline(baseline, c='b')
        figure_path = os.path.join(os.path.join(os.getcwd(),'grafici'), event_name)
        plt.savefig(figure_path)
        plt.close()
    print('Analisi completata!!                       ')
    return general_min_list

# ora abbiamo una lista di minimi considerati validi, con rispettivi tempi e ampiezze (e altre colonne ridondanti che servivano per i plot)
min_list = analysis(timestamp_table, wf_table,wf_data_points)
# seleziono solo le righe corrispondenti ai minimi validi, utilizzando la lista di indici definita prima
minimum_table = wf_table.loc[min_list].copy()
# infine calcolo le differenze dei tempi relativi ai minimi delle waveforms
# diff calcola, per ogni riga, la differenza con la riga precedente (o due righe indietro se periods =2, o tre se periods=3, ecc)
minimum_table['TIME'] = minimum_table['TIME'].diff(periods=1)
minimum_table = minimum_table.iloc[1:,:]
# una volta trovati tutti picchi possiamo costruire il grafico ed estrarre i valori di DCR, AP e CT
minimum_table.rename(columns={'TIME':'Delta T (s)','CH1':'Amplitude (V)'}, inplace = True)            # rinomino le colonne
plt.scatter(minimum_table['Delta T (s)'],minimum_table['Amplitude (V)'])
plt.xscale("log")
plt.savefig('Amplitude_vs_dt.pdf')
plt.show()
plt.close()
# La Dark Count Rate è semplicemente il numero di eventi considerati validi, diviso per il tempo totale di misura
# la probabilità di After Pulse è la precentuale di eventi con delta t inferiore a 6 microsecondi
# la probabilità di Cross Talk è la percentuale di eventi con ampiezza superiore a 1 p.e. (p.e. = fotoelettrone, nel nostro caso pari a 8 mV)
