LIMITE_BORNE_2 = 1000
UNITES = ("Esclaves", "Maîtres esclave", "Jeunes soldates", "Soldates", "Soldates d'élite", "Gardiennes",
          "Gardiennes d'élite", "Tirailleuses", "Tirailleuses d'élite", "Jeunes légionnaires", "Legionnaires",
          "Tanks", "Tanks d'élite", "Énigmas")


def approxFdf(TDCarrivee, TDCchasse):
    m = 0.54*TDCchasse**0.11
    p = 10**(-6.79)*TDCchasse**2 + 15.5*TDCchasse
    return int(m*TDCarrivee+p)
    # pente = 2.3939*10**(-7)*TDCchasse + 2.15
    # fdf = (0.85*((pente*TDCarrivee + 17*TDCchasse) *TDCarrivee) / (TDCarrivee + 30000))
    # return int(fdf)


def calculFdf(nbrUnites, mandibule):
    fdfUnites = [4, 6, 8, 11, 17, 1, 1, 32, 40, 45, 60, 80, 140, 260]
    fdf = 0
    for i in range(len(UNITES)):
        fdf += fdfUnites[i]*nbrUnites[i]
    return int(fdf*(10+mandibule)/10)


def espaceur(nombre):
    nombre = str(int(nombre))
    string = ""
    for i in range(len(nombre)):
        string = nombre[len(nombre)-i-1] + string
        if (i+1) % 3 == 0 and i != len(nombre)-1:
            string = " " + string
    return string


def minDeriv(tableau):
    res = tableau[1]-tableau[0]
    for i in range (2, len(tableau)):
        if(tableau[i]-tableau[i-1] < res):
            res = tableau[i]-tableau[i-1]
    return res


reponse = 'O'
while reponse.upper() == 'O':
    # Initialisation des variables
    TDCchasse = -1
    nbrUnites = len(UNITES)*[""]
    l = LIMITE_BORNE_2
    
    # Paramétrage du simulateur par l'utilisateur
    TDCdepart = int(input("TDC au moment du lancement : "))
    if(TDCdepart < 1):
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()

    TDCarrivee = int(input("TDC au moment de l'arrivee des chasses : "))
    if(TDCarrivee < 1):
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()

    VT = int(input("Vitesse de traque : "))
    if(VT < 0):
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()

    nbrChasses = int(input("Nombre de chasse à lancer (entre 1 et "+str(VT+1)+") : "))
    if nbrChasses > VT+1 or nbrChasses < 1:
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()
    fdfChasse = [0]*nbrChasses
    
    mandibule = int(input("\nNiveau de mandibule : "))
    if mandibule < 0:
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()
    
    for i in range(len(UNITES)):
        nbrUnites[i] = int(input("Nombre de "+str(UNITES[i])+" : "))
        if nbrUnites[i] < 0:
            print("\n\nErreur lors de l'encodage des valeurs !\n\n")
            exit()
    
    fdfChasse[len(fdfChasse)-1] = calculFdf(nbrUnites, mandibule)
    print("=> Force de frappe =", espaceur(fdfChasse[len(fdfChasse)-1]))

    print("\n\n\nCalcul en cours")

    while (min(fdfChasse) < 0 or minDeriv(fdfChasse) < 0 or TDCchasse < 0) and l > 0:
        
        print(l)

        # Initialisation des variables
        TDCchasse = 100
        l -= 1 # l est le nombre maximum d'itérations restantes de la boucle

        # calcul des TDCchasse et des fdfChasse
        # j est le numéro des chasses (la boucle fonctionne en partant de la dernière)
        for j in range(nbrChasses-1, -1, -1):
            i = 0
            eq = [0, 0, 0]
            borne = [0, 1000000000000, 100]
            if j == nbrChasses-1:
                TDCchasse = 0

            while abs(TDCchasse-borne[2]) >= 1:
                TDCchasse = borne[2]

                memory = 0
                for k in range(j+1):
                    memory += approxFdf(TDCarrivee+k*borne[0], borne[0])
                eq[0] = memory - fdfChasse[j]

                memory = 0
                for k in range(j+1):
                    memory += approxFdf(TDCarrivee+k*borne[1], borne[1])
                eq[1] = memory - fdfChasse[j]

                if eq[0] > 0 and eq[1] < 0:
                    eq[0], eq[1] = eq[1], eq[0]

                borne[2] = (borne[0]+borne[1])/2

                memory = 0
                for k in range(j+1):
                    memory += approxFdf(TDCarrivee+k*borne[2], borne[2])
                eq[2] = memory - fdfChasse[j]

                if eq[2] > 0:
                    borne[1] = borne[2]
                elif eq[2] < 0:
                    borne[0] = borne[2]

                # print("eq1 =", eq[0])
                # print("eq2 =", eq[1])
                # print("eq3 =", eq[2])
                # print("borne1 =", borne[0])
                # print("borne2 =", borne[0])
                # print("borne3 =", borne[0])

                # print("dif =", abs(TDCchasse-borne[2]), "\n")

            for k in range(j):
                fdfChasse[j-1] += approxFdf(TDCarrivee+k*borne[2], borne[2])
            if j == 0:
                fdfChasse[0] = approxFdf(TDCarrivee, borne[2])

    if l > 0:
        # Affichage des fdf par chasse
        print("\n\n\nNum | TDC à chasser | Fdf à envoyer    | Fdf totale")
        for i in range(nbrChasses):

            print(i+1, " "*(3-len(str(i+1))), end="")

            print("|", espaceur(TDCchasse), " "*(13-len(espaceur(TDCchasse))), end="")

            if i != 0:
                print("|", espaceur(fdfChasse[i]-fdfChasse[i-1]), end="")
                print(" "*(17-len(espaceur(fdfChasse[i]-fdfChasse[i-1]))), end="")
            else:
                print("|", espaceur(fdfChasse[i]-0), end="")
                print(" "*(17-len(espaceur(fdfChasse[i]-0))), end="")

            print("|", espaceur(fdfChasse[i]))

        print("\nTOTAL TDC :", espaceur(TDCchasse*nbrChasses), "cm²\n")

        # Affichage unités à envoyer
        for i in range(nbrChasses):
            chasseOk = ""
            while chasseOk.upper() != 'OK':
                chasseOk = input("\n\nEcris 'ok' pour voir la chasse suivante: ")

            if i != 0:
                print("\n- Chasse numero", i+1, "(fdf: " +str(espaceur(fdfChasse[i]-fdfChasse[i-1]))+ ")", end="")
            else:
                print("\n- Chasse numero", i+1, "(fdf: " +str(espaceur(fdfChasse[i]-0))+ ")", end="")
            print("\nUnite                | Nombre d'unites à envoyer")

            for j in range(len(UNITES)):
                print(UNITES[j], " "*(20-len(UNITES[j])), end="")

                if i != 0:
                    fractionArmee = (fdfChasse[i]-fdfChasse[i-1])/fdfChasse[nbrChasses-1]
                else:
                    fractionArmee =  (fdfChasse[i]-0)/fdfChasse[nbrChasses-1]
                print("|", espaceur(fractionArmee*nbrUnites[j]))

        print("\n\nTOTAL TDC :", espaceur(TDCchasse*nbrChasses), "cm²\n")

        # calcul duree des chasses
        jour = int(((TDCchasse+TDCdepart)*(0.9**VT))/86400)
        heure = int(((TDCchasse+TDCdepart)*(0.9**VT))/3600 - jour*24)
        minute = int(((TDCchasse+TDCdepart)*(0.9**VT))/60 - jour*1440 - heure *60)
        seconde = int(((TDCchasse+TDCdepart)*(0.9**VT)) - jour*86400 - heure *3600 - minute*60)
        print("Duree des chasses :", espaceur(jour), "J", espaceur(heure), "H", espaceur(minute), "Min",
              espaceur(seconde), "S\n\n\n")
    else:
        print("\n\n\nErreur lors du calcul des/de la chasse(s) !\n\n\n")

    reponse = input("Voulez-vous relancer le programme ? (O/N)\n")[0]
    print("\n\n\n\n")
