#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

#define LIMITE_CHASSE 30
#define LIMITE_BORNE_2 10000

long long min(long long tableau[], int borne);
long long min2(long long tableau[], int borne);
long long approxFdf(int TDCarrivee, int borne);
long long calculFdf(long long nbrUnites[], int mandibule);
char* espaceurDeMillier(long long nombre);

int main()
{
    int i = 0, j = 0, k = 0, l = 0;
    int TDCarrivee = 0, TDCdepart = 0, TDCchasse[LIMITE_CHASSE];
    long long fdfChasse[LIMITE_CHASSE];
    long long borne1 = 0, borne2 = LIMITE_BORNE_2*TDCarrivee, borne3 = 0;
    long long eq1 = 0, eq2 = 0, eq3 = 0, memory = 0;
    int nbrChasses = 1, jour = 0, heure = 0, minute = 0, seconde = 0;
    long long nbrUnites[14];
    int mandibule = -1, VT = -1;
    char unites[14][30] = {"esclaves", "maitre esclaves", "jeunes soldates", "soldates", "soldates d'elite", "gardiennes", "gardiennes d'elite", "tirailleuses", "tirailleuses d'elite", "jeunes legionnaires", "legionnaires", "tanks", "tanks d'elite", "enigmas"};
    char memoryStr[20] = "", reponse = 'O', chasseOk = ' ';
    double fractionArmee = 0.0;


    while(toupper(reponse) == 'O') {

        // Initialisation des variables
        for(i = 0 ; i < LIMITE_CHASSE ; i++){
            TDCchasse[i] = 100;
            fdfChasse[i] = 0;
        }
        for(i = 0 ; i < 14 ; i++)
            nbrUnites[i] = 0;
        TDCdepart = 0;
        VT = -1;
        TDCarrivee = 0;
        nbrChasses = 0;
        l = LIMITE_BORNE_2;

        // Récupération des valeurs-mères
        printf("TDC au moment du lancement : ");
        scanf("%d", &TDCdepart);
        if(TDCdepart < 1){
            printf("\n\nErreur lors de l'encodage des valeurs !\n\n");
            return 0;
        }

        printf("TDC au moment de l'arrivee des chasses : ");
        scanf("%d", &TDCarrivee);
        if(TDCarrivee < 1){
            printf("\n\nErreur lors de l'encodage des valeurs !\n\n");
            return 0;
        }

        printf("Vitesse de traque : ");
        scanf("%d", &VT);
        if(VT < 0){
            printf("\n\nErreur lors de l'encodage des valeurs !\n\n");
            return 0;
        }

        printf("Nombre de chasse a lancer (entre 1 et %d) : ", LIMITE_CHASSE);
        scanf("%d", &nbrChasses);
        if(nbrChasses > LIMITE_CHASSE || nbrChasses < 1){
            printf("\n\nErreur lors de l'encodage des valeurs !\n\n");
            return 0;
        }

        printf("\nNiveau de mandibule : ");
        scanf("%d", &mandibule);
        if(mandibule < 0){
            printf("\n\nErreur lors de l'encodage des valeurs !\n\n");
            return 0;
        }

        for(i = 0 ; i < 14 ; i++){
            printf("Nombre de %s : ", unites[i]);
            scanf("%I64d", &nbrUnites[i]);
            if(nbrUnites[i] < 0){
                printf("\n\nErreur lors de l'encodage des valeurs !\n\n");
                return 0;
            }
        }
        fdfChasse[nbrChasses-1] = calculFdf(nbrUnites, mandibule);
        printf("=> Force de frappe = %s", espaceurDeMillier(fdfChasse[nbrChasses-1]));


        printf("\n\n\nCalcul en cours");

        do {
            printf(".");

            // Initialisation des variables
            for(i = 0 ; i < LIMITE_CHASSE ; i++){
                TDCchasse[i] = 100;
                if(i != nbrChasses-1)
                    fdfChasse[i] = 0;
            }
            l--;



            // calcul des TDCchasse et des fdfChasse
            for(j = nbrChasses-1 ; j >= 0 ; j--) {

                i = 0;
                eq1 = 0;
                eq2 = 0;
                eq3 = 0;
                borne1 = 0;
                borne2 = l*TDCarrivee;
                borne3 = 100;
                TDCchasse[j] = borne3;

                do {
                    TDCchasse[j] = borne3;

                    i++;

                    memory = 0;
                    for(k = 0 ; k <= j ; k++)
                        memory += approxFdf(TDCarrivee+k*borne1, borne1);
                    eq1 = memory - fdfChasse[j];

                    memory = 0;
                    for(k = 0 ; k <= j ; k++)
                        memory += approxFdf(TDCarrivee+k*borne2, borne2);
                    eq2 = memory - fdfChasse[j];

                    if(eq1 > 0 && eq2 < 0){
                        memory = eq1;
                        eq1 = eq2;
                        eq2 = memory;
                    }

                    borne3 = (borne1+borne2)/2;

                    memory = 0;
                    for(k = 0 ; k <= j ; k++)
                        memory += approxFdf(TDCarrivee+k*borne3, borne3);
                    eq3 = memory - fdfChasse[j];

                    if(eq3 > 0)
                        borne2 = borne3;
                    else if(eq3 < 0)
                        borne1 = borne3;

                    /*printf("eq1 = %I64d\n", eq1);
                    printf("eq2 = %I64d\n", eq2);
                    printf("eq3 = %I64d\n", eq3);
                    printf("borne1 = %I64d\n", borne1);
                    printf("borne2 = %I64d\n", borne2);
                    printf("borne3 = %I64d\n", borne3);

                    printf("dif = %d\n\n",abs(TDCchasse[j]-borne3));*/
                } while(abs(TDCchasse[j]-borne3) >= 1) ;

                if(j == nbrChasses-1)
                    TDCchasse[j] = borne3;
                else
                    TDCchasse[j] = TDCchasse[nbrChasses-1];

                memory = 0;
                for(k = 0 ; k < j ; k++)
                    fdfChasse[j-1] += approxFdf(TDCarrivee+k*borne3, borne3);
                if(j == 0)
                    fdfChasse[0] = approxFdf(TDCarrivee, borne3);
            }
        } while((min(fdfChasse, LIMITE_CHASSE) < 0 || min2(fdfChasse, nbrChasses-1) < 0 || TDCchasse[nbrChasses-1] < 0) && l > 0) ;


        if(l > 0) {
            // Affichage des résultats
            printf("\n\n\nNum | TDC a chasser | Fdf a envoyer    | Fdf totale\n");
            for(i = 0 ; i < nbrChasses ; i++) {

                printf("%d", i+1);
                sprintf(memoryStr, "%d", i+1);
                for(j = 0 ; j < 4-strlen(memoryStr) ; j++)
                    printf(" ");

                printf("| %s", espaceurDeMillier(TDCchasse[nbrChasses-i-1]));
                sprintf(memoryStr, "%s", espaceurDeMillier(TDCchasse[nbrChasses-i-1]));
                for(j = 0 ; j < 14-strlen(memoryStr) ; j++)
                    printf(" ");

                if (i != 0){
                    printf("| %s", espaceurDeMillier(fdfChasse[i]-fdfChasse[i-1]));
                    sprintf(memoryStr, "%s", espaceurDeMillier(fdfChasse[i]-fdfChasse[i-1]));
                }
                else{
                    printf("| %s", espaceurDeMillier(fdfChasse[i]-0));
                    sprintf(memoryStr, "%s", espaceurDeMillier(fdfChasse[i]-0));
                }
                for(j = 0 ; j < 17-strlen(memoryStr) ; j++)
                    printf(" ");

                printf("| %s\n", espaceurDeMillier(fdfChasse[i]));
            }


            for(i = 0 ; i < nbrChasses ; i++){
                do{
                    printf("\n\nEcris 'ok' pour voir la chasse suivante: ");
                    while (getchar() != '\n');
                    scanf("%c", &chasseOk); }
                while(tolower(chasseOk) != 'o');

                if (i != 0)
                    printf("\n- Chasse numero %d (fdf: %s)", i+1, espaceurDeMillier(fdfChasse[i]-fdfChasse[i-1]));
                else
                    printf("\n- Chasse numero %d (fdf: %s)", i+1, espaceurDeMillier(fdfChasse[i]-0));
                printf("\nUnite                | nombre d'unites a envoyer\n");

                for(j = 0 ; j < 14 ; j++) {

                    printf("%s", unites[j]);
                    for(k = 0 ; k < 21-strlen(unites[j]) ; k++)
                        printf(" ");

                    if (i != 0){
                        fractionArmee = ((double)(fdfChasse[i]-fdfChasse[i-1])/(double)(fdfChasse[nbrChasses-1]));
                        }
                    else{
                        fractionArmee =  ((double)(fdfChasse[i]-0)/(double)(fdfChasse[nbrChasses-1]));
                        }
                    printf("| %s\n", espaceurDeMillier((long long)(fractionArmee*nbrUnites[j])));
                }
            }


            printf("\n\nTOTAL TDC : %s cm2\n", espaceurDeMillier(TDCchasse[0]*nbrChasses));

            // calcul duree des chasses
            jour = (int)(((TDCchasse[0]+TDCdepart)*pow(0.9, VT))/86400);
            heure = (int)(((TDCchasse[0]+TDCdepart)*pow(0.9, VT))/3600 - jour*24);
            minute = (int)(((TDCchasse[0]+TDCdepart)*pow(0.9, VT))/60 - jour*1440 - heure *60);
            seconde = (int)(((TDCchasse[0]+TDCdepart)*pow(0.9, VT)) - jour*86400 - heure *3600 - minute*60 + 0.5);
            printf("Duree des chasses : %dJ %dH %dMin %dS\n\n\n", jour, heure, minute, seconde);
        }
        else
            printf("\n\n\nErreur lors du calcul des/de la chasse(s) !\n\n\n");

        printf("Voulez-vous relancer le programme ? (O/N)\n");
        while (getchar() != '\n');
        scanf("%c", &reponse);
        printf("\n\n\n\n");
    }

    return 0;
}


long long min(long long tableau[], int borne){
    long long min = tableau[borne];
    int i = 0;

    for(i = 0 ; i < borne ; i++){
        if(tableau[i] < min)
            min = tableau[i];
    }

    return min;
}


long long min2(long long tableau[], int borne){
    long long min = tableau[borne]-tableau[borne-1];
    int i = 0;

    for(i = 1 ; i < borne ; i++){
        if(tableau[i]-tableau[i-1] < min)
            min = tableau[i]-tableau[i-1];
    }

    return min;
}


long long approxFdf(int TDCarrivee, int borne){
    double pente = 2.3939*pow(10.0, -7)*borne + 2.15;
    return (long long)(0.85*((pente*TDCarrivee + 17.0*borne) *TDCarrivee) / (TDCarrivee + 30000));
}


long long calculFdf(long long nbrUnites[], int mandibule){
    int fdfUnites[14] = {4, 6, 8, 11, 17, 1, 1, 32, 40, 45, 60, 80, 140, 260};
    long long fdf = 0;
    int i = 0;

    for (i = 0 ; i < 14 ; i++)
        fdf += fdfUnites[i]*nbrUnites[i];

    fdf = (long long)(fdf*(10+(long long)(mandibule))/10);

    return fdf;
}

char* espaceurDeMillier(long long nombre){
    char nombreChar[100] = "";
    sprintf(nombreChar, "%I64d", nombre);
    int i = 0;
    char nombreEspaces[100] = "";
    char memoryStr[100] = "";

    for(i = strlen(nombreChar)-1 ; i >= 0 ; i--){
        sprintf(nombreEspaces, "%c%s", nombreChar[i], memoryStr);
        sprintf(memoryStr, "%s", nombreEspaces);

        if((strlen(nombreChar)-i)%3 == 0 && i != 0){
            sprintf(nombreEspaces, "%c%s", ' ', memoryStr);
            sprintf(memoryStr, "%s", nombreEspaces);
        }
    }
    return nombreEspaces;
}
