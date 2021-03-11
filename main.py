import fonctions
from time import process_time

# Fonction de test pour la Q6

def testGSEtu():
    for i in range(200,2001,200):
        sumtime = 0
        for j in range(10):
            
            pref_etu = fonctions.generePrefEtu(i)
            pref_spe = fonctions.generePrefSpe(i)

            debut = process_time()
            fonctions.gsEtu(pref_etu,pref_spe)
            temps = process_time() - debut
            sumtime+=temps
        print("Moyenne pour "+ str(i) +" étudiants : " + str(sumtime/10) + " secondes.")

def testGSSpe():
    for i in range(200,2001,200):
        sumtime = 0
        for j in range(10):
            
            pref_etu = fonctions.generePrefEtu(i)
            pref_spe = fonctions.generePrefSpe(i)

            debut = process_time()
            fonctions.gsSpe(pref_etu,pref_spe)
            temps = process_time() - debut
            sumtime+=temps
        print("Moyenne pour "+ str(i) +" étudiants : " + str(sumtime/10) + " secondes.")

print("Temps de calcul côté étudiant")
print()
testGSEtu()
print()
print()
print("Temps de calcul côté master")
print()
testGSSpe()