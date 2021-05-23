import numpy as np
import pandas as pd

import datetime


LIMITE_BORNE_2 = 1000
UNITES = ("Esclaves", "Maîtres esclave", "Jeunes soldates", "Soldates", "Soldates d'élite", "Gardiennes",
          "Gardiennes d'élite", "Tirailleuses", "Tirailleuses d'élite", "Jeunes légionnaires", "Legionnaires",
          "Tanks", "Tanks d'élite", "Énigmas")


def min_deriv(tableau):
    res = tableau[1]-tableau[0]
    for i in range(2, len(tableau)):
        if tableau[i]-tableau[i-1] < res:
            res = tableau[i]-tableau[i-1]
    return res


def approx_fdf(tdc_arrivee, tdc_chasse):
    return 156 + 4.685644*(tdc_chasse**1.105944) + 0.466*tdc_arrivee*(tdc_chasse**0.1066647)


def calcul_fdf(nbr_unites, mandibule):
    fdf_unites = np.array([4, 6, 8, 11, 17, 1, 1, 32, 40, 45, 60, 80, 140, 260])
    return (fdf_unites*np.array(nbr_unites)).sum() * (1 + mandibule/20)


pd.options.display.float_format = '${:,.0f}'.format

reponse = True
while reponse:
    # Initialisation des variables
    tdc_chasse = -1
    nbr_unites = len(UNITES) * [""]
    l = LIMITE_BORNE_2

    # Paramétrage du simulateur par l'utilisateur
    TDCdepart = int(input("TDC au moment du lancement : "))
    if TDCdepart < 1:
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()

    tdc_arrivee = int(input("TDC au moment de l'arrivee des chasses : "))
    if tdc_arrivee < 1:
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()

    VT = int(input("Vitesse de traque : "))
    if VT < 0:
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()

    nbr_chasses = int(input("Nombre de chasse à lancer (entre 1 et " + str(VT + 1) + ") : "))
    if nbr_chasses > VT + 1 or nbr_chasses < 1:
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()
    fdf_chasse = np.zeros(nbr_chasses, dtype=np.int64)

    mandibule = int(input("\nNiveau de mandibule : "))
    if mandibule < 0:
        print("\n\nErreur lors de l'encodage des valeurs !\n\n")
        exit()

    nbr_unites = np.zeros(len(UNITES))
    for i in range(len(UNITES)):
        nbr_unites[i] = int(input("Nombre de " + str(UNITES[i]) + " : "))
        if nbr_unites[i] < 0:
            print("\n\nErreur lors de l'encodage des valeurs !\n\n")
            exit()

    fdf_chasse[-1] = calcul_fdf(nbr_unites, mandibule)
    print("=> Force de frappe = {:,}".format(fdf_chasse[-1]))

    print("\n\n\nCalcul en cours")

    while (min(fdf_chasse) < 0 or min_deriv(fdf_chasse) < 0 or tdc_chasse < 0) and l > 0:

        print(l)

        # Initialisation des variables
        tdc_chasse = 100
        l -= 1  # l est le nombre maximum d'itérations restantes de la boucle

        # calcul des tdc_chasse et des fdf_chasse
        # j est le numéro des chasses (la boucle fonctionne en partant de la dernière)
        for j in range(nbr_chasses - 1, -1, -1):
            i = 0
            eq = [0, 0, 0]
            borne = [0, 1_000_000_000_000, 100]
            if j == nbr_chasses - 1:
                tdc_chasse = 0

            while abs(tdc_chasse - borne[2]) >= 1:
                tdc_chasse = borne[2]

                memory = 0
                for k in range(j + 1):
                    memory += approx_fdf(tdc_arrivee + k * borne[0], borne[0])
                eq[0] = memory - fdf_chasse[j]

                memory = 0
                for k in range(j + 1):
                    memory += approx_fdf(tdc_arrivee + k * borne[1], borne[1])
                eq[1] = memory - fdf_chasse[j]

                if eq[0] > 0 > eq[1]:
                    eq[0], eq[1] = eq[1], eq[0]

                borne[2] = (borne[0] + borne[1]) / 2

                memory = 0
                for k in range(j + 1):
                    memory += approx_fdf(tdc_arrivee + k * borne[2], borne[2])
                eq[2] = memory - fdf_chasse[j]

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

                # print("dif =", abs(tdc_chasse-borne[2]), "\n")

            for k in range(j):
                fdf_chasse[j - 1] += approx_fdf(tdc_arrivee + k * borne[2], borne[2])
            if j == 0:
                fdf_chasse[0] = approx_fdf(tdc_arrivee, borne[2])

    if l <= 0:
        print("\n\n\nErreur lors du calcul des/de la chasse(s) !\n\n\n")
        exit()

    # remove cumulative sum
    for i in range(1, len(fdf_chasse)):
        fdf_chasse[i] -= fdf_chasse[:i].sum()

    # Affichage des fdf par chasse*
    historique_chasses = pd.DataFrame({"TDC à chasser": [int(tdc_chasse)]*nbr_chasses,
                                       "Fdf à envoyer": fdf_chasse, 
                                       "Fdf totale": np.cumsum(fdf_chasse)},
                                      dtype=np.int64)
    print(historique_chasses)

    print("\nTOTAL TDC : {:,} cm²\n".format(int(tdc_chasse * nbr_chasses)))

    # Affichage unités à envoyer
    for i in range(nbr_chasses):
        chasse_ok = ""
        while chasse_ok.upper() != 'OK':
            chasse_ok = input("\n\nEcris 'ok' pour voir la chasse suivante: ")

        partial_fdf = historique_chasses.at[historique_chasses.index[i], "Fdf à envoyer"]
        print("\n- Chasse numéro {} (fdf: {})".format(i+1, partial_fdf))

        fraction_armee = partial_fdf / historique_chasses.loc[:, "Fdf à envoyer"].sum()
        print(pd.DataFrame({"Unité": UNITES,
                            "Nombre d'unites à envoyer": (nbr_unites*fraction_armee).astype(int)}))

    print("\nTOTAL TDC : {:,} cm²\n".format(int(tdc_chasse * nbr_chasses)))

    # calcul duree des chasses
    tps_chasse = (60 + TDCdepart/10 + tdc_chasse/2) / (1 + VT/10)
    tps_chasse = datetime.timedelta(seconds=tps_chasse)
    print("Duree des chasses : {}\n\n\n".format(tps_chasse))

    reponse = input("Voulez-vous relancer le programme ? (O/N)\n")[0].upper() == 'O'
    print("\n\n\n\n")
