#include "repository.h"
#include <stdlib.h>

Repository* createRepository(int capacity){
    Repository* repo = (Repository*)malloc(sizeof(Repository));
    repo->meds = createDynamicArray(capacity);
    repo->undoStack = createDynamicalVArray(capacity);
    repo->redoStack = createDynamicalVArray(capacity);
    return repo;
}

void destroyRepository(Repository* repo){
    if(repo == NULL)
        return;
    destroy(repo->meds);
    free(repo);
}

int findMed(Repository* repo, TElem med){
    if(repo == NULL)
        return -1;
    for(int i = 0; i < getLength(repo->meds); i++){
        if(compareMeds(getElement(repo->meds, i), med))
            return i;
    }
    return -1;
}

int findMedToGivenNC(Repository* repo, char* name, int concentration){
    if(repo == NULL)
        return -1;
    for(int i = 0; i < getLength(repo->meds); i++){
        if(compareMedToGivenNC(getElement(repo->meds, i), name, concentration))
            return i;
    }
    return -1;
}

void addMed(Repository* repo, TElem med){
    if(repo == NULL)
        return;

    if (findMed(repo, med) == -1) {
        add(repo->meds, med);
        return;
    }

    int pos = findMed(repo, med);
    TElem oldMed = getElement(repo->meds, pos);
    setMedQuantity(&oldMed, getMedQuantity(oldMed) + getMedQuantity(med));
    update(repo->meds, pos, oldMed);
}

void deleteMed(Repository* repo, int pos){
    if(repo == NULL)
        return;
    delete(repo->meds, pos);
}

void updateMed(Repository* repo, int pos, TElem med){
    if(repo == NULL)
        return;
    update(repo->meds, pos, med);
}

int getLengthRepo(Repository* repo){
    if(repo == NULL)
        return -1;
    return getLength(repo->meds);
}

TElem getMed(Repository* repo, int pos){
    if(repo == NULL)
        return NULL_TElem;
    return getElement(repo->meds, pos);
}

DynamicArray *getMeds(Repository* repo){
    if(repo == NULL)
        return NULL;
    DynamicArray *copy = createDynamicArray(getLength(repo->meds));
    for(int i = 0; i < getLength(repo->meds); i++)
        add(copy, getElement(repo->meds, i));
    return copy;
}