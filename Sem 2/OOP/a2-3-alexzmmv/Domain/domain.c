#include <string.h>
#include <strsafe.h>

#include "domain.h"

//creates a new medicine
TElem createMed(char* name, int concentration, int quantity, float price) {
    TElem med;
    setMedName(&med, name);
    setMedConcentration(&med, concentration);
    setMedQuantity(&med, quantity);
    setMedPrice(&med, price);
    return med;
}

//getter functions

void getMedName(TElem med, char *name) {
    strcpy_s(name, 40, med.name);
}

int getMedConcentration(TElem med) {
    return med.concentration;
}

int getMedQuantity(TElem med) {
    return med.quantity;
}

float getMedPrice(TElem med) {
    return med.price;
}

//setter functions

void setMedName(TElem* med, char* name) {
    strcpy_s(med->name, 40, name);
}

void setMedConcentration(TElem* med, int concentration) {
    med->concentration = concentration;
}

void setMedQuantity(TElem* med, int quantity) {
    med->quantity = quantity;
}

void setMedPrice(TElem* med, float price) {
    med->price = price;
}
//utility functions

int compareMeds(TElem med1, TElem med2) {
    if (strcmp(med1.name, med2.name) == 0 && med1.concentration == med2.concentration) {
        return 1;
    }
    return 0;
}

int compareMedToGivenNC(TElem med1, char* name, int concentration) {
    if (strcmp(med1.name, name) == 0 && med1.concentration == concentration) {
        return 1;
    }
    return 0;
}

void medToString(TElem med, char* s) {
    //create a string
    StringCchPrintf(s, 120, "Name: %s, Concentration: %d, Quantity: %d, Price: %.2f", med.name, med.concentration, med.quantity, med.price);
}

