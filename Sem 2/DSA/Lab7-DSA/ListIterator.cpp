#include "ListIterator.h"
#include "SortedIndexedList.h"
#include <iostream>

using namespace std;

ListIterator::ListIterator(const SortedIndexedList& list) : list(list) {
    stack = new int[list.size() + 1];
    first();
}

ListIterator::~ListIterator() {
    delete[] stack;
}

void ListIterator::first() {
    int current = list.root;
    top = 0;
    while (current != NULL_NODE) {
        stack[top++] = current;
        current = list.tree[current].left;
    }
}

void ListIterator::next() {
    if (!valid()) {
        throw exception();
    }
    int current = stack[--top];
    if (list.tree[current].right != NULL_NODE) {
        current = list.tree[current].right;
        while (current != NULL_NODE) {
            stack[top++] = current;
            current = list.tree[current].left;
        }
    }
}

bool ListIterator::valid() const{
    return top > 0;
}

TComp ListIterator::getCurrent() const{
    if (!valid()) {
        throw exception();
    }
    return list.tree[stack[top - 1]].value;
}

