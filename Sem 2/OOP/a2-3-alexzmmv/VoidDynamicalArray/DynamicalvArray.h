#pragma once
#include <stdlib.h>
typedef struct {
    void **elems;
    int length;
    int capacity;
} DynamicalVArray;

DynamicalVArray* createDynamicalVArray(int capacity);
void destroyv(DynamicalVArray *arr);
void addv(DynamicalVArray *arr, void* t);
void* popv(DynamicalVArray *arr);