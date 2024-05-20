medicaments = {"m1":0,"m2":0,"m3":0,"m4":5,"m5":10}
symptomes   = {"diarhée":2,"fièvre":5,"infection urinaire":6,"s4":0,"s5":12}
effects = {
    "m1":[50,0,0,1,3],
    "m2":[0,1,0,2,3],
    "m3":[0,0,50,4,5],
    "m4":[1,50,1,5,6],
    "m5":[30,12,3,9,8]
}

def is_curable(medicaments,effects,symptomes):
    medocs = list(medicaments.keys())
    listeSympt = []
    for i in range(len(symptomes)):
        listeSympt.append(False)
    for i in range(len(symptomes)):
        for meds in medocs:
            if effects[meds][i] > 0: 
                listeSympt[i] = True
    return listeSympt
                   
def is_well(effects):
    is_not_sick = True
    for i in effects:
        if i>0:
            is_not_sick=False
            break
    return is_not_sick

def combinCure(dictMedicament,n):
    if n==0:
        return ['']
    cures = []
    for cure in combinCure(dictMedicament,n-1):
        for meds in dictMedicament:
            cures.append(meds+" "+cure)
    return cures


def get_price(listeCombinaisonMedicaments,medicaments):
    prices = []
    for liste in listeCombinaisonMedicaments:
        price = 0
        for nameMeds,nbreMeds in liste.items():
            price += medicaments[nameMeds]*nbreMeds
        prices.append(price)
    return prices

def get_indices_minimal(prices):
    minimal = min(prices)
    indices = []
    for i in range(len(prices)):
        if prices[i] <= minimal:
            indices = i
    return indices


def count_element(liste):
    result = {}
    ensemble = set(liste)
    for elt in ensemble:
        result[elt] = 0
        for i in liste:
            if i==elt:
                result[elt]+=1
    return result

def drop_double(liste):
    occurences = []
    for elt in liste:
        occurences.append(count_element(elt))
    result = []
    for i in occurences:
        if i not in result: result.append(i)
    return result

def effectsOnSymptomes(symptome,nbreMeds,effectsOfCure):
    sympt = []
    for i in range(len(symptome)):
        sympt.append(symptome[i] - nbreMeds *effectsOfCure[i])
    return sympt
    

def effectsCure(listeCombinaisonMedicaments,listeSymptome,effects):
    symptomes = []
    for liste in listeCombinaisonMedicaments:
        effectCure = listeSymptome
        for nameMeds,nbreMeds in liste.items():
            effectCure = effectsOnSymptomes(effectCure,nbreMeds,effects[nameMeds])
        symptomes.append(effectCure)
    return symptomes

def degree_symptome(symptome):
    is_sick = None
    for i in symptome:
        if i > 0:
            is_sick = True
            break
    return is_sick

def get_minimal_price_cure(medicaments,symptomes,effects):
# vérification si tous les symptômes sont curables
    curables = is_curable(medicaments,effects,symptomes)
    not_curable = False
    for i in curables:
        if not i:
            return "Our medicine can't cure the patient"
    symptDegree = list(symptomes.values())

# vérifie aussi si le patient est malade
    is_sick = degree_symptome(symptDegree)
    if not is_sick:
        return "This patient is well"

# initialisation de la plus longue longueur de médicaments possibles
# si n est trop grande, la liste de possibilité devient en très grande quantité
    longueur_max = 0
    for i in symptomes.values():
        longueur_max += i
    if longueur_max > 10:
        longueur_max = 10
    medics = list(medicaments.keys())
    
    listeMedocs = []
    tabFinal = []
    
# avoir la liste de médicaments possibles
    n = 1
    while( n < longueur_max):
        print("n:"+str(n))
        cureTmp = []
        tmp = combinCure(medicaments,n)
        for l in tmp:
            cureTmp.append(l.strip().split(" "))
        cureTmp = drop_double(cureTmp)
        stat = []
        effets = effectsCure(cureTmp,symptDegree,effects)
        for i in effets:
            stat.append(is_well(i))
        for i in range(len(cureTmp)):
            if stat[i]: 
                listeMedocs.append(cureTmp[i])
        n += 1
#     tabMedocs = []
#     for liste in listeMedocs:
#         for l in liste:
#             tabMedocs.append(l.strip().split(" "))
# # on efface de la liste de médicaments les médicaments qui reviennent plus d'une fois
#     listeMeds = drop_double(tabMedocs)

# on regarde l'effet de chaque combinaison de médicaments
    effetMeds = effectsCure(listeMedocs,symptDegree,effects)
# on regarde l'effet que peut avoir chaque combinaison de médicaments sur le symptôme du patient
    # tabStat = []
    # for i in effetMeds:
    #     tabStat.append(is_well(i))
# avoir le prix de chaque combinaison de médicaments
    prices = get_price(listeMedocs,medicaments)
# Pour la liste des médicaments qui ne réussit pas à guérir la maladie, on leur met un prix
# très élevé
    # for i in range(len(tabStat)):
    #     if not tabStat[i]:prices[i] = 10000000000
    indices_minimal = get_indices_minimal(prices)
    message = ""
    medoc = listeMedocs[indices_minimal]
    for k,v in medoc.items():
        message += f"\n- {v} {k}"
    return f"The patient need to buy :"+message+ f"\nCost:{min(prices)} Ar"
    #return listeMedocs[indices_minimal],min(prices)
    
    # # test sur 9 médicaments
    # meds9 = combinCure(medicaments,9)
    # tab9Medocs = []
    # for l in meds9:
    #     tab9Medocs.append(l.strip().split(" "))
    # tab9Medocs = drop_double(tab9Medocs)
    # prices = get_price(tab9Medocs,medicaments)
    # print(min(prices))


    #indices_minimal = get_indices_minimal(prices)
    #return listeMeds[indices_minimal],min(prices)

    

# def get_list_cures(medicaments,symptomes,effects):
# # initialisation de la longueur de chaque liste de médicaments dans la combinaison
#     n = 1
#     medics = list(medicaments.keys())
#     symptDegree = list(symptomes.values())
#     listes = []
#     stat = None
#     gueri = is_well(symptDegree)
# # on trouve la longueur approprié de la liste de medicaments pour guérir le patient
#     while(not gueri):
#         listeCombinMedicament = combinCure(medicaments,n)
#         for liste in listeCombinMedicament:
#             listes.append(liste.strip().split(" "))
# # on efface la liste de médicaments qui reviennent
#         listeMeds = drop_double(listes)
# # on regarde les effets de chaque liste de médicaments pour voir si le patient est guéri
#         effetMeds = effectsCure(listeMeds,symptDegree,effects)
#         tabsStat = []
#         for i in effetMeds:
#             if is_well(i):
#                 gueri = True
#                 tabsStat.append(True)
#             else:
#                 tabsStat.append(False)
#         n = n + 1
# # affiche la combinasion de médicaments s'il guérisse ou non
#     combinFinalMeds = listeMeds
#     stat = tabsStat
#     prices = get_price(combinFinalMeds,medicaments)
# # Pour la liste des médicaments qui ne réussit pas à guérir la maladie, on leur met un prix
# # très élevé
#     for i in range(len(stat)):
#         if not stat[i]:prices[i] = 10000000000
#     indices_minimal = get_indices_minimal(prices)
#     return combinFinalMeds[indices_minimal],min(prices)

        
    

if __name__=="__main__":
    print(get_minimal_price_cure(medicaments,symptomes,effects))
    #is_curable(medicaments,effects,symptomes)

