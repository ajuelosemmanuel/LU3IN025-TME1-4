import exemple # Pour pouvoir utiliser les methodes de exemple.py
import fonctions

#print("bonjour")

#print("LISTE DES ETU")
listeEtu=fonctions.lectureFichierEtu("PrefEtu.txt")
#print(listeEtu)

#print("LISTE DES SPE")
listeSpe=fonctions.lectureFichierSpe("PrefSpe.txt")
#print(listeSpe)
res = fonctions.gsEtu(listeEtu,listeSpe)
print(res)
#exemple.createFichierLP(maListe[0][0],int(maListe[1][0])) #Methode int(): transforme la chaine de caracteres en entier
