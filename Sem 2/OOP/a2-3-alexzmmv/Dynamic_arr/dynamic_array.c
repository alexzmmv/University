#include <stdlib.h>
#include "dynamic_array.h"


DynamicArray* createDynamicArray(int capacity){
    DynamicArray* arr = (DynamicArray*)malloc(sizeof(DynamicArray));
    arr->capacity = capacity;
    arr->length = 0;
    arr->elems = (TElem*)malloc(sizeof(TElem) * capacity);
    return arr;
}

void destroy(DynamicArray *arr){
    if(arr == NULL || arr->elems == NULL)
        return;

    free(arr->elems);
    free(arr);
}

void resize(DynamicArray* arr){
    if (arr == NULL)
        return;
    arr->capacity *= 2;
    TElem* aux = realloc(arr->elems, arr->capacity * sizeof(TElem));
    if (aux == NULL)
        return; //
    arr->elems = aux;
}

void add(DynamicArray *arr, TElem t){
    if(arr == NULL || arr->elems == NULL)
        return;
    if (arr->length == arr->capacity)
        resize(arr);
    arr->elems[arr->length++] = t;
}

void delete(DynamicArray *arr, int pos){
    if(arr == NULL || arr->elems == NULL)
        return;
    DynamicArray *newArr = createDynamicArray(arr->capacity);
    for(int i = 0; i < arr->length; i++)
        if(i != pos)
            add(newArr, arr->elems[i]);
    arr->length--;
    arr->elems = newArr->elems;
    arr->capacity = newArr->capacity;
    free(newArr);
}

void update(DynamicArray *arr, int pos, TElem t){
    if(arr == NULL || arr->elems == NULL)
        return;
    arr->elems[pos] = t;
}

int getLength(DynamicArray *arr){
    if(arr == NULL)
        return -1;
    return arr->length;
}

TElem getElement(DynamicArray *arr, int pos) {
    if (arr == NULL || arr->elems == NULL || pos < 0 || pos >= arr->length)
        return NULL_TElem;
    return arr->elems[pos];
}
