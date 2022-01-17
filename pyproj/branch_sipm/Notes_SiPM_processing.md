# Notes, lecture 30/11

Revision of process_claro and a look at the SiPm data in G:\Il mio Drive\Corsi\Object_Oriented_Programming\Dati_SiPM\

## SiPM data

- guarda che tipo di dati hai
- devi ottenere un dataframe con le I (intensità di corrente), V (voltaggi) e il nome del file da cui provengono
- devi calcolare la tensione di breakdown con i passaggi descritti sotto
- devi calcolare anche la resistenza di quenching
- ricorda che la resistenza di quenching si trova per il forward, mentre la tensione di breakdown con il reversed (you sure?)
- devi definire a mano la threshold per fittare i dati sia per il fwd lineare che per il rvd polinomiale

Use Polynomial.fit (function of numpy)
You have to convert the function to make the fit to fit the actual data
Polynomial.fit restitutes z,zz that are the parameters of the fit (minimized by chisquared) --> check documentation

Polynomial(z.convert().coef)

Resistenza di quenching = 1/z.convert().coef[1]
Questa è la resistenza di quenching equivalente di ca. 11k celle, perciò per trovare quella della singola bisogna considerare che sono tutte poste in parallelo.

Tensione di breakdown: si trova calcolando la derivata (discreta) della tensione rispetto alla corrente, moltiplicandola per il reciproco della corrente e trovando il massimo (fittando) del plot che viene fuori.

np.diff() serve per fare array di differenze tra dati discreti

To fit the data, define MANUALLY (but then you will have to do it automatically) the range of data on which to fit
