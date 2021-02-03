from copy import deepcopy

#   Fonctions utilitaires

def exists(L,p):
	if len(L)==0:
		return False
	for i in L:
		if p(i):
			return True
	return False

def isntEmpty(L):
    return L!=[]

def indexFirstOcc(el,L):
    cpt = 0
    for e in L:
        if e == el:
            return cpt
        cpt+=1
    return 100000000 # rang trop grand pour être comparable si l'élément n'est pas dans la liste

def existenceEtuLibNoProp(L,dict):
    cpt=0
    for cpt in range(len(L)):
        if cpt not in dict:
            if isntEmpty(cpt):
                return True
    return False

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
    return res

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
    return res

def gsEtu(matEtu, matSpe):
    matEtuTmp = deepcopy(matEtu)    # matrice représentant les préférences des étudiants
    matSpeTmp = deepcopy(matSpe)    # matrice représentant les préférences des masters
    nbEtu = matEtuTmp[0]    # nombre d'étudiants
    nbSpe = matSpeTmp[0]    # nombre de places en master
    if nbSpe != nbEtu :
        print("Il n'y a pas autant de places que d'étudiants, on ne peut donc pas appliquer l'algorithme de Gale-Shapley.")
        return dict()
    speCapacity = matSpeTmp[1]  # liste des capacités des masters
    speCapacity.pop(0)  # on retire le "cap"
    matSpeTmp.pop(0)    # on retire le ligne contenant le nombre de places au total, car la valeur est désormais stockée
    matSpeTmp.pop(0)    # Idem pour les capacités
    matEtuTmp.pop(0)    # on retire donc la ligne qui contient le nombre d'étudiants
    for el in matSpeTmp:    # on retire maintenant le numéro et le nom des masters, car le numéro = l'index dans la liste matSpeTmp et que le nom est inutile
        del el[0]
        del el[0]
    for el in matEtuTmp:    # on fait de même avec les étudiants
        del el[0]
        del el[0]
    affectations=dict() # on créé un dictionnaire qui contiendra les affectations
    while existenceEtuLibNoProp(matEtuTmp,affectations): # tant qu'il existe un étudiant qui n'a
        cpt=0
        while (cpt in affectations) or matEtuTmp[cpt] == []:
                cpt+=1
        choiceEtu = matEtuTmp[cpt].pop(0)
        if speCapacity[choiceEtu] != 0 :    # Si il y a de la place dans le master, on affecte l'étudiant
            affectations[cpt] = choiceEtu
            speCapacity[choiceEtu]-=1
        else:                               # Sinon, on regarde le(s) affecté(s) et on regarde leur(s) numéro(s)
            affList=[]
            for etu,spe in affectations.items():    # On génère donc une liste des numéros du ou des affecté(s) au master
                if spe == choiceEtu:                # Si une personne est dans le master désiré, alors son numéro est ajouté à la liste
                    affList.append(etu)
            prefListSpe = [ (el,indexFirstOcc(el,matSpeTmp[choiceEtu])) for el in affList]   # On créé une liste de tuples (num étudiant, index de l'occurence de du num dans les préférences du master)
            prefListSpe.sort(key = lambda x:x[1])
            if prefListSpe[0][1] > indexFirstOcc(cpt,matSpeTmp[choiceEtu]):
                del affectations[prefListSpe[0][0]]
                affectations[cpt] = choiceEtu
    return sorted(affectations.items())