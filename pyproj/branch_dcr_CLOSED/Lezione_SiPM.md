# Lezione SiPM

Rivelatori per fotoni: bolometri?

Diodi al silicio:
- componente elettronico passivo, bipolare, non-lineare (relazione che lega tensione e corrente ai capi non è lineare)
- un diodo è una giunzione tra pezzi di silicio drogati diversamente: in questo modo si crea una "valvola", nel senso che la corrente è in grado di scorrere solo in una direzione
- la parte attiva è la giunzione (pn tipicamente)

Caratterizzazione corrente in un diodo
- polarizzazione diretta (forward): la corrente può fluire liberamente e in corrispondenza della tensione V_d la corrente diverge
- polarizzazione inversa (reverse): la corrente è dell'ordine del pA e scorre in verso opposto
- oltre la tensione di breakdown abbiamo un'effetto valanga dovuto alla rottura della giunzione pn. Il passaggio di una singola carica genera una valanga, attraverso un processo di scattering, di coppie elettrone-lacuna. Il valore di breakdown del campo elettrico è 3e5 V/cm

--> APD = Avalanche PhotoDiode
Il guadagno tipico per un fotone nel visibile (qualche eV) è di 1e6, 1e7 fotoelettroni.
La valanga viene interrotta con una resistenza di quenching aggiunta in serie al diodo, che produce una caduta di tensione tale che la tensione torna al di sotto del valore di breakdown. La durata della valanga dipende dalla resistenza di quenching.

I SiPM sono costituiti da una matrice di fotodiodi a valanga posti in parallelo, e ciascuno in serie con le proprie resistenze di quenching
Vengono costruiti a partire da uno strato di silicio. Hanno un buon fill factor (?).

Due tipi di sensori: a seconda della disposizione della giunzione pn rispetto all'arrivo dei fotoni si può stabilire se saranno più sensibili a raggi UV o VIS, perché è una questione di assorbimento.

Il segnale è costituito da una salita molto rapida e una decrescita esponenziale fissa che è lunga tanto quanto il dead time del dispositivo.

Le gaussiane dei picchi dovuti ai singoli fotoni sono convolute con una poissoniana che ne determina la distribuzione dei picchi

DCR (dark count rate) è dovuto alla probabilità intrinseca di generazione di coppie elettrone-lacuna dovuta all'eccitazione termica.

After-pulse (stessa cella): dovuto a livelli trappola (dovuti a impurezze) caricati durante la valanga, al di fuori della giunzione, e poi driftati verso di essa.
Cross-talk: dovuto all'emissione di fotoni da diseccitazione e loro riassorbimento, nella stessa cella (delayed) o che finisce direttamente in un'altra (direct)

AP e CT sono individuabili dal plot amplitude-time distance (time distance wrt to previous event)

When fitting IV curves with a linear function, the angular coefficient of the line is the inverse of the total resistance of the SiPM, meaning that is the equivalent resistance of all the parallel cells.  

************************************************************************************************************

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