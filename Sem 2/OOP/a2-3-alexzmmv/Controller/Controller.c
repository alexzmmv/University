
#include <string.h>
#include "Controller.h"

int addmedicine(Repository* repo, char* name, int concentration, int quantity, float price) {
    TElem med = createMed(name, concentration, quantity, price);
    if (findMed(repo, med) != -1)
        return 0;
    addMed(repo, med);
    return 1;
}

int removemedicine(Repository* repo, char* name, int concentration) {
    int pos = findMedToGivenNC(repo, name, concentration);
    if (pos == -1)
        return 0;
    deleteMed(repo, pos);
    return 1;
}

int updatemedicine(Repository* repo, char* name, int concentration, int quantity, float price) {
    int pos = findMedToGivenNC(repo, name, concentration);
    if (pos == -1)
        return 0;
    TElem med = createMed(name, concentration, quantity, price);
    updateMed(repo, pos, med);
    return 1;
}

//filtering functions(b)
int filterByName(Repository* repo, Repository* newRepo, char* name) {
    for (int i = 0; i < getLengthRepo(repo); i++) {
        TElem med = getMed(repo, i);
        char medName[40];
        getMedName(med, medName);
        if (strstr(medName, name) != NULL)
            addMed(newRepo, med);
    }
    return 1;
}

int filterByPrice(Repository* repo, Repository* newRepo, float Price){
    for (int i = 0; i < getLengthRepo(repo); i++) {
        TElem med = getMed(repo, i);
        if (getMedPrice(med) <= Price)
            addMed(newRepo, med);
    }
    return 1;
}

//short supply (c)
void shortSupply(Repository* repo, Repository* newRepo, int x) {
    for (int i = 0; i < getLengthRepo(repo); i++) {
        TElem med = getMed(repo, i);
        if (getMedQuantity(med) <= x)
            addMed(newRepo, med);
    }
}



//utilities
void sort_repo(Repository* repo, int(*cmp)(TElem, TElem)) {
    for (int i = 0; i < getLengthRepo(repo) - 1; i++) {
        for (int j = i + 1; j < getLengthRepo(repo); j++) {
            TElem med1 = getMed(repo, i);
            TElem med2 = getMed(repo, j);
            if (cmp(med1, med2) > 0) {
                TElem aux = med1;
                updateMed(repo, i, med2);
                updateMed(repo, j, aux);
            }
        }
    }
}

int compare_by_name(TElem med1, TElem med2) {
    char name1[40], name2[40];
    getMedName(med1, name1);
    getMedName(med2, name2);
    return strcmp(name1, name2);
}

int compare_by_quantity(TElem med1, TElem med2) {
    return getMedQuantity(med1) - getMedQuantity(med2);
}

int compare_by_price(TElem med1, TElem med2) {
    return  getMedPrice(med1) - getMedPrice(med2)>0?1:-1;
}