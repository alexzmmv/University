#pragma once
#include "../Dynamic_arr/dynamic_array.h"
#include "../VoidDynamicalArray/DynamicalvArray.h"

typedef struct {
    DynamicArray* meds;
    DynamicalVArray *undoStack;
    DynamicalVArray *redoStack;
} Repository;

//creates a new repository
Repository* createRepository(int capacity);

//destroys the repository
void destroyRepository(Repository* repo);

//adds a new element to the repository
void addMed(Repository* repo, TElem med);

//deletes an element from the repository
void deleteMed(Repository* repo, int pos);

//updates an element from the repository
void updateMed(Repository* repo, int pos, TElem med);

//returns the length of the repository
int getLengthRepo(Repository* repo);

//returns the element from a given position
TElem getMed(Repository* repo, int pos);

//returns the dynamic array of the repository
DynamicArray* getMeds(Repository* repo);

//utility functions
int findMed(Repository* repo, TElem med);
int findMedToGivenNC(Repository* repo, char* name, int concentration);