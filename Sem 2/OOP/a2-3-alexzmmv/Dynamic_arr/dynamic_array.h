#pragma once

#include "../Domain/domain.h"

//dynamic array of meds
typedef struct {
    TElem *elems;
    int length;
    int capacity;
} DynamicArray;

//creates/destroy a new dynamic array
DynamicArray* createDynamicArray(int capacity);
void destroy(DynamicArray *arr);

//adds a new element to the dynamic array
void add(DynamicArray *arr, TElem t);

void resize(DynamicArray* arr);

void delete(DynamicArray *arr, int pos);

void update(DynamicArray *arr, int pos, TElem t);

//returns the length of the dynamic array
int getLength(DynamicArray *arr);

//returns the element from a given position
TElem getElement(DynamicArray *arr, int pos);
