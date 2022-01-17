# 7/12/2021
# Waveforms processing with Python

Oscilloscopio utilizzato: TEKTRONICS MS064

Modalità utilizzata: FastFrame
Frame è sionimo di wavelength.
- seleziono numero di *frame* che voglio acquisire
- ogni frame è definito dallo scatto del trigger (quindi acquisiamo solo segnale triggerato)
- la *record length* è la lunghezza del frame acquisito, fornita come numero di intervalli di acquisizione
- c'è un pretrigger che può essere impostato per acquisire anche la parte della waveform prima del trigger
- la frequenza di campionamento (ordine GHz) è il reciproco del sample interval

Data structure
- 2 file di dati
- file 1 (wf): contiene i timestamp dei punti della waveform relativi allo 0 che è lo scatto del trigger (tempi negativi sono tutti i tempi del pretrigger), e le misure delle ampiezze delle waveforms
- file 2 (timestamps): contiene indice e *timestamp* che sono il tempo intercorso rispetto all'evento precedente

2 possibilità:
- converto tempi relativi sulle wf in tempi assoluti
- uso direttamente i tempi relativi per plottare

NOTE VARIE IMPORTANTI:
- la baseline è calcolata sui dati di pretrigger
