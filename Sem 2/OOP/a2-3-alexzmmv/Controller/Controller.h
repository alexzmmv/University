#pragma once
#include "../Domain/domain.h"
#include "../Repo/repository.h"

int addmedicine(Repository* repo, char* name, int concentration, int quantity, float price);
int removemedicine(Repository* repo, char* name, int concentration);
int updatemedicine(Repository* repo, char* name, int concentration, int quantity, float price);

//filtering functions(b)
int filterByName(Repository* repo, Repository* newRepo, char* name);
int filterByPrice(Repository* repo, Repository* newRepo, float Price);
//short supply (c)
void shortSupply(Repository* repo, Repository* newRepo, int x);

//utilities
void sort_repo(Repository* repo, int(*cmp)(TElem, TElem));
//
//
int compare_by_name(TElem med1, TElem med2);
int compare_by_quantity(TElem med1, TElem med2);
int compare_by_price(TElem med1, TElem med2);