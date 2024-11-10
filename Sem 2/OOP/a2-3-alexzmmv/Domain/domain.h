#pragma once

typedef struct {
    char name[40];
    int concentration;
    int quantity;
    float price;
}Med;

#define NULL_TElem createMed("",0,0,0)


//TElem=generic element used later for better understanding
typedef Med TElem;


//creates a new medicine
TElem createMed(char* name, int concentration, int quantity, float price);
//getters
void getMedName(TElem med, char* name);
int getMedConcentration(TElem med);
int getMedQuantity(TElem med);
float getMedPrice(TElem med);

//setters
void setMedName(TElem* med, char* name);
void setMedConcentration(TElem* med, int concentration);
void setMedQuantity(TElem* med, int quantity);
void setMedPrice(TElem* med, float price);

//utility functions
int compareMeds(TElem med1, TElem med2);
int compareMedToGivenNC(TElem med1,char *name, int concentration);

void medToString(TElem med, char* s);