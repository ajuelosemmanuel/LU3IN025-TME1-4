from copy import deepcopy
from random import sample, randrange
from time import process_time

#Fonction qui convertit un dictionnaire en liste de liste
def convert_dict_list(dictionnaire):
    new_liste=[]
    for etu,master in dictionnaire:
        new_couple = [etu,master]
        new_liste.append(new_couple)
    return new_liste

#Fonction qui retrouve la valeur de la clé à partir d'une valeur
def find_key(dictionnaire,valeur):
    liste_keys = [] # un master peut avoir plusieurs etudiants (ici etudiant est key et master est value)
    for key,value in dictionnaire.items():
        if value == valeur :
            liste_keys.append(key)
    return liste_keys
    

# Fonctions demandées en exercice

def lectureFichierEtu(s): # Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
    monFichier = open(s, "r") # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines() # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
    monFichier.close() #Fermeture du fichier
    res=[]
    for e in contenu:
        e=e.replace("\t", "-")
        e=e.replace("\n", "")
        e=e.split("-")
        tmp=[]
        for el in e:
            if el.isdecimal():
                el = int(el)
            tmp.append(el)
        res.append(tmp)
    nbEtu = res.pop(0)[0]
    pref = [etu[2::]  for etu in res]
    return [nbEtu, pref]

def lectureFichierSpe(s): # Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
    monFichier = open(s, "r") # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines() # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
    monFichier.close() #Fermeture du fichier
    res=[]
    for e in contenu:
        e=e.replace("\t", "-")
        e=e.replace("\n", "")
        e=e.split("-")
        tmp=[]
        for el in e:
            if el.isdecimal():
                el = int(el)
            tmp.append(el)
        res.append(tmp)
    res[0][0]=int(res[0][0].replace("NbEtu ",""))
    res[1]=res[1][0].split()
    tmp=[]
    for el in res[1]:
        if el.isdecimal():
            el = int(el)
        tmp.append(el)
    res[1]=tmp
    nbPlaces = res.pop(0)[0]
    capList = res.pop(0)
    cap = [capList[i+1]  for i in range(len(capList[1::]))]
    pref = [ spe[2::]  for spe in res]
    return [nbPlaces, cap, pref]


# Fonction qui applique l'algorithme de Gale-Shapley côté étudiant dans le problème Etudiant / Master 
def gsEtu(matEtu, matSpe):
    # Initialisation
    nbEtu = matEtu[0]    # nombre d'étudiants
    nbSpe = matSpe[0]    # nombre de places en master
    if nbSpe != nbEtu :
        print("Il n'y a pas autant de places que d'étudiants, on ne peut donc pas appliquer l'algorithme de Gale-Shapley.")
        return dict()
    matEtuTmp = deepcopy(matEtu[1])    # matrice représentant les préférences des étudiants
    matSpeTmp = deepcopy(matSpe[2])    # matrice représentant les préférences des masters
    # Traitement des données Master et Etudiants
    speCapacity = matSpe[1]  # liste des capacités des masters
    affectations=dict() # on créé un dictionnaire qui contiendra les affectations
    Libres = [k for k in range(nbEtu)]             # liste des étudiants non-affectés
    # Application de l'algorithme de Gale-Shapley 
    while (len(Libres)!=0):  # tant qu'il existe un étudiant qui n'a pas fait toutes ses propositions
        # On sélectionne le premier étudiant de la liste Libres[] et on affecte à choiceEtu le 1er Master de sa liste
        Etu = Libres[0] # l'étudiant qu'on va suivre dans cette itération, le 1er de la liste des non-affectés 
        choiceEtu = matEtuTmp[Etu].pop(0) # pop(0) affecte à choiceEtu et enlève de matEtuTmp son 1er élément
        # Si on peut affecter l'étudiant au master
        if speCapacity[choiceEtu] != 0 :    # Si il y a de la place dans le master, on affecte l'étudiant
            affectations[Etu] = choiceEtu
            speCapacity[choiceEtu]-=1
            # On enlève choiceEtu de la liste Libres
            Libres.pop(0)
        # Sinon, on regarde le(s) affecté(s) et on regarde leur(s) numéro(s)
        else:                               
            # On génère donc une liste des numéros du ou des affecté(s) au master
            affList=[] 
            # Si une personne est dans le master désiré, alors son numéro est ajouté à la liste
            for etu,spe in affectations.items():    
                if spe == choiceEtu:                
                    affList.append(etu)
            affList.append(Etu) # On ajoute l'étudiant qui veut intégrer ce Master
            # Tri des préférences des Masters sur la liste des étudiants déjà affectés à ce dernier 
            affList_trie=[]
            for etudiant_pref in matSpeTmp[choiceEtu]: # On parcourt la liste des préférences du Master dans l'ordre 
                for etudiant_affectes in affList:
                     # On affecte lorsqu'on reconnait un étudiant -> tri par ordre de préférence
                    if etudiant_pref == etudiant_affectes:
                        affList_trie.append(etudiant_affectes)
            # Comparaison entre le dernier élément de la liste des affectés (l'étudiant le moins désiré) 
            # avec l'étudiant en cours Libres[0]
            if (affList_trie[-1]!=Etu): # Si le dernier élément de la liste n'est pas l'étudiant Etu
                Libres.append(affList_trie[-1]) # On ajoute cet étudiant à la liste des étudiants non-affectés
                del affectations[affList_trie[-1]] # On enlève l'affectation enregistrée de l'étudiant rejeté
                affectations[Etu] = choiceEtu # On affecte l'étudiant Etu au Master désiré 
                # On enlève choiceEtu de la liste Libres
                Libres.pop(0)
            # Sinon, on garde l'étudiant dans la liste et on continue à regarder la suite de sa liste de préférences     
    return sorted(affectations.items())


# Fonction qui applique l'algorithme de Gale-Shapley côté Master dans le problème Etudiant / Master 
def gsSpe(matEtu, matSpe):
    # Initialisation
    nbEtu = matEtu[0]    # nombre d'étudiants
    nbSpe = matSpe[0]    # nombre de places en master
    if nbSpe != nbEtu :
        print("Il n'y a pas autant de places que d'étudiants, on ne peut donc pas appliquer l'algorithme de Gale-Shapley.")
        return dict()
    matEtuTmp = deepcopy(matEtu[1])    # matrice représentant les préférences des étudiants
    matSpeTmp = deepcopy(matSpe[2])    # matrice représentant les préférences des masters
    # Traitement des données Master et Etudiants
    speCapacity = matSpe[1]  # liste des capacités des masters
    affectations=dict() # on créé un dictionnaire qui contiendra les affectations
    Libres = [] # liste des étudiants non-affectés
    for k in range(nbSpe):
        if len(Libres) != nbEtu:
            Libres += [k] * speCapacity[k]
        else : break
    affectations=dict() # on créé un dictionnaire qui contiendra les affectations

     # Application de l'algorithme de Gale-Shapley 
    while (len(Libres)!=0):  # tant qu'il existe un master qui n'a pas fait toutes ses propositions
    
        # On sélectionne le premier Master de la liste Libres[] et on affecte à choiceMaster le 1er étudiant de sa liste
        
        Master = Libres[0] # le master qu'on va suivre dans cette itération, le 1er de la liste des non-affectés 
        choiceMaster = matSpeTmp[Master].pop(0) # pop(0) affecte à choiceMaster et enlève de matSpeTmp son 1er élément
                
        # On traite les propositions des Masters aux étudiants                               
        # On génère donc une liste des propositions de master à l'étudiant choiceMaster 
        affList=[] 
        # Si une personne est dans le master désiré, alors son numéro est ajouté à la liste
        for etu,spe in affectations.items():    
            if etu == choiceMaster:                
                affList.append(spe)
        affList.append(Master) # On ajoute le master à la liste des propositions de master de l'étudiant  
                    
        # Tri des préférences des Masters sur la liste des étudiants déjà affectés à ce dernier 
        affList_trie=[]
        for master_pref in matEtuTmp[choiceMaster]: # On parcourt la liste des préférences de l'étudiant dans l'ordre 
            for master_affectes in affList:
                # On affecte lorsqu'on reconnait un master -> tri par ordre de préférence
                if master_pref == master_affectes:
                    affList_trie.append(master_affectes)
                        
        # Comparaison entre le dernier élément de la liste des affectés (le master le moins désiré) 
        # avec le Master en cours : Libres[0]
        if (choiceMaster not in affectations):
            affectations[choiceMaster] = Master
            Libres.pop(0)
        else:
            if (affList_trie[-1]!=Master): # Si le dernier élément de la liste n'est pas le Master qu'on étudie -> choiceMaster préfère le nouveau master à son ancien
                Libres.append(affList_trie[-1]) # On ajoute cet étudiant à la liste des étudiants non-affectés
                del affectations[choiceMaster] # On enlève l'affectation enregistrée de l'étudiant rejeté
                affectations[choiceMaster] = Master # On affecte l'étudiant Etu au Master désiré 
                # On enlève choiceEtu de la liste Libres
                Libres.pop(0)
            
            # Sinon, on garde le master dans la liste et on continue à regarder la suite de sa liste de préférences

    return sorted(affectations.items())


# Fonction qui retourne la liste des paires instables d'une affectation -> si retourne liste vide alors c'est un mariage stable 
def paires_instables(liste_affectation,matEtu,matSpe):
    
    #Initialisation
    matEtuTmp = deepcopy(matEtu)    # matrice représentant les préférences des étudiants
    matSpeTmp = deepcopy(matSpe)    # matrice représentant les préférences des masters
    liste_paires_instables = []     # liste des paires instables de liste_affectation
    new_liste_affectation = convert_dict_list(liste_affectation) # converti liste_affectation(dict) en new_liste_affectation(liste)
    
    # Traitement des données Master et Etudiants
    matSpeTmp.pop(0)    # on retire le ligne contenant le nombre de places au total, car la valeur est désormais stockée
    matSpeTmp.pop(0)    # Idem pour les capacités
    matEtuTmp.pop(0)    # on retire donc la ligne qui contient le nombre d'étudiants

    # On retire maintenant le numéro et le nom des masters, car le numéro = l'index dans la liste matSpeTmp et que le nom est inutile
    for el in matSpeTmp:
        del el[0]
        del el[0]
    for el in matEtuTmp:    # on fait de même avec les étudiants
        del el[0]
        del el[0]
        
    # Calcul des paires instables 
    for affectation in new_liste_affectation: # On parcourt tous les couples de liste_affectation
        etudiant1 = affectation[0]        # Le premier élément du couple est l'étudiant
        master1 = affectation[1]          # Le second élément est le master associé à l'étudiant
        liste_instable_etu1 = []           # liste des potentiels couples instables côté étudiant

        # On parcourt la liste de préférences de l'étudiant itéré pour créer une liste de masters au-dessus du master qu'il a actuellement
        # par rapport à son ordre de préférence 
        for pref in matEtuTmp[etudiant1]:               
            if (pref==master1):     # Si on a atteint le master qu'il a accepté, nous n'avons plus besoin de rester dans la boucle for 
                break
            else:                   # Sinon, on ajoute le master qui peut créer une paire instable
                liste_instable_etu1.append(pref)
        
        for master2 in liste_instable_etu1:
            liste_instable_master2 = []      # liste des potentiels couples instables côté master
            liste_etudiant2=[]            # liste des étudiants affectés au master2 
            for element in new_liste_affectation:
                if(element[1]==master2):
                    liste_etudiant2.append(element[0])
                
            #Tri de etudiant_instable
            liste_etudiant2_trie = []
            for pref in matSpeTmp[master2]:
               if pref in liste_etudiant2:
                   liste_etudiant2_trie.append(pref)
            
            # On parcourt la liste de préférences du master itéré pour créer une liste d'étudiants au-dessus de celui qu'il a actuellement 
            # et si on trouve etudiant1 parmi eux alors on crée une paire instable
            for i in matSpeTmp[master2]:
                if i == liste_etudiant2_trie[-1] : # Si on a atteint l'étudiant le moins désiré parmi les étudiants du master, on arrête 
                    break
                if i==etudiant1 :  # Si étudiant1, alors on a une paire instable
                    liste_instable_master2.append(i)
                    liste_paires_instables.append([etudiant1,master2])
    return liste_paires_instables


def generePrefEtu(nbEtu):
    return [nbEtu] + [[sample([x for x in range(9)], 9) for i in range(nbEtu)]]

def generePrefSpe(nbEtu):

    def _capGen(nbEtu):
        capPer = nbEtu//9
        cap = []
        for i in range(8):
            rndmC = 0
            while rndmC < 1 :
                rndmC = capPer + randrange(-(nbEtu//10)//2, (nbEtu//10)//2)
            cap.append(rndmC)
        cap.append(nbEtu- sum(cap))
        return cap
    
    cap = _capGen(nbEtu)
    while any(x<1 for x in cap) or any((nbEtu//6)<x for x in cap):
        cap = _capGen(nbEtu)
    
    return [nbEtu]+[sample(cap, 9)] + [[sample([x for x in range(nbEtu)], nbEtu) for i in range(9)]]

