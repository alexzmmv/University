#include "DynamicalvArray.h"

DynamicalVArray* createDynamicalVArray(int capacity) {
    DynamicalVArray * arr = (DynamicalVArray *)malloc(sizeof(DynamicalVArray));
    arr->capacity = capacity;
    arr->length = 0;
    arr->elems = (void**)malloc(sizeof(void*) * capacity);
    return arr;
}

void resizev(DynamicalVArray* arr) {
    if (arr == NULL)
        return;
    arr->capacity *= 2;
    void** aux = realloc(arr->elems, arr->capacity * sizeof(void*));
    if (aux == NULL)
        return; //
    arr->elems = aux;
}

void destroyv(DynamicalVArray *arr) {
    if (arr == NULL || arr->elems == NULL)
        return;
    free(arr->elems);
    free(arr);
}

void addv(DynamicalVArray *arr, void* t) {
    if (arr == NULL || arr->elems == NULL)
        return;
    if (arr->length == arr->capacity)
        resizev(arr);
    arr->elems[arr->length++] = t;
}

void* popv(DynamicalVArray *arr) {
    if (arr == NULL || arr->elems == NULL)
        return NULL;
    arr->length--;
    return arr->elems[arr->length];
}