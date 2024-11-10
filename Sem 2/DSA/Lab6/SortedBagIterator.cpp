#include "SortedBagIterator.h"
#include "SortedBag.h"
#include <exception>
#include <algorithm>

using namespace std;

void Merge(TComp* elements, int left, int middle, int right, Relation r) {
    int i, j, k;
    int n1 = middle - left + 1;
    int n2 = right - middle;

    TComp* L = new TComp[n1];
    TComp* R = new TComp[n2];

    for (i = 0; i < n1; i++)
        L[i] = elements[left + i];
    for (j = 0; j < n2; j++)
        R[j] = elements[middle + 1 + j];

    i = 0;
    j = 0;
    k = left;
    while (i < n1 && j < n2) {
        if (r(L[i], R[j])) {
            elements[k] = L[i];
            i++;
        }
        else {
            elements[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        elements[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        elements[k] = R[j];
        j++;
        k++;
    }
}

void MergeSort (TComp* elements, int left, int right, Relation r) {
    if (left < right) {
        int middle = left + (right - left) / 2;
        MergeSort(elements, left, middle, r);
        MergeSort(elements, middle + 1, right, r);
        Merge(elements, left, middle, right, r);
    }
}
SortedBagIterator::SortedBagIterator(const SortedBag& b) : bag(b) {
    elements = new TComp[b.capacityOfArray];
    this->eIn=0;
    for(int i=0;i<b.capacityOfArray;i++) {
        if(b.elements[i].data!=NULL_TCOMP)
            elements[eIn++]=b.elements[i].data;
    }
    current_index=0;

    MergeSort(elements, 0, eIn-1, b.r);
}

TComp SortedBagIterator::getCurrent() {
    if(valid())
        return elements[current_index];
    throw std::exception();
}

bool SortedBagIterator::valid() {
    return current_index<eIn;
}

void SortedBagIterator::next() {
    if(valid())
        current_index++;
    else
        throw std::exception();
}

void SortedBagIterator::first() {
	    current_index=0;
}

