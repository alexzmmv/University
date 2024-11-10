#include "ListIterator.h"
#include "SortedIndexedList.h"
#include <iostream>
using namespace std;
#include <exception>

SortedIndexedList::SortedIndexedList(Relation r) : r(r) {
    length = 0;
    capacity = 100;
    tree = new Node[capacity];
    freeStack = new int[capacity];
    for (int i = 0; i < capacity; i++) {
        freeStack[i] = i;
    }
    freeStackTop = capacity - 1;
    root = NULL_NODE;
}

int SortedIndexedList::size() const {
    return length;
}

bool SortedIndexedList::isEmpty() const {
    return length == 0;
}

void SortedIndexedList::resize() {
    Node* newTree = new Node[capacity<<1];
    int* newFreeStack = new int[capacity<<1];
    for (int i = 0; i < capacity; i++) {
        newTree[i]=tree[i];
        newFreeStack[freeStackTop+1+i] = i+capacity;
    }
    delete[] tree;
    delete[] freeStack;
    tree = newTree;
    freeStack = newFreeStack;
    freeStackTop = freeStackTop+capacity;
    capacity <<= 1;
}

void SortedIndexedList::add(TComp e) {
    if(length==capacity-1)
        resize();
    if (root == NULL_NODE) {
        root = freeStack[freeStackTop--];
        tree[root].value = e;
        length++;
        return;
    }

    int current = root;
    int parent = NULL_NODE;
    while (current != NULL_NODE) {
        if (r(tree[current].value, e)) {
            parent = current;
            current = tree[current].right;
        }
        else {
            tree[current].leftCount++;
            parent = current;
            current = tree[current].left;
        }
    }

    int newNode = freeStack[freeStackTop--];
    tree[newNode].value = e;
    (r(tree[parent].value, e) ? tree[parent].right : tree[parent].left) = newNode;
    length++;
}

TComp SortedIndexedList::getElement(int i) const{
    if (i < 0 || i >= length) {
        throw exception();
    }

    int current = root;
    while (current != NULL_NODE) {
        if (tree[current].leftCount == i) return tree[current].value;
        if (tree[current].leftCount > i)
            current = tree[current].left;
        else {
            i -= tree[current].leftCount + 1;
            current = tree[current].right;
        }
    }

    return NULL_TCOMP;
}

TComp SortedIndexedList::remove(int i) {
    if (i < 0 || i >= length) {
        throw exception();
    }

    int current = root;
    int parent = NULL_NODE;
    while (current != NULL_NODE) {
        if (tree[current].leftCount == i) break;
        if (tree[current].leftCount > i) {
            tree[current].leftCount--;
            parent = current;
            current = tree[current].left;
        }
        else {
            i -= tree[current].leftCount + 1;
            parent = current;
            current = tree[current].right;
        }
    }

    TComp removed = tree[current].value;
    if (tree[current].left == NULL_NODE && tree[current].right == NULL_NODE) {
        if (parent == NULL_NODE) {
            root = NULL_NODE;
        }
        else {
            if (tree[parent].left == current) {
                tree[parent].left = NULL_NODE;
            }
            else {
                tree[parent].right = NULL_NODE;
            }
        }
        freeStack[++freeStackTop] = current;
    }
    else if (tree[current].left == NULL_NODE) {
        if (parent == NULL_NODE) {
            root = tree[current].right;
        }
        else {
            if (tree[parent].left == current) {
                tree[parent].left = tree[current].right;
            }
            else {
                tree[parent].right = tree[current].right;
            }
        }
        freeStack[++freeStackTop] = current;
    }
    else if (tree[current].right == NULL_NODE) {
        if (parent == NULL_NODE) {
            root = tree[current].left;
        }
        else {
            if (tree[parent].left == current) {
                tree[parent].left = tree[current].left;
            }
            else {
                tree[parent].right = tree[current].left;
            }
        }
        freeStack[++freeStackTop] = current;
    }
    else {
        int successor = tree[current].right;
        int successorParent = current;
        while (tree[successor].left != NULL_NODE) {
            tree[successor].leftCount--;
            successorParent = successor;
            successor = tree[successor].left;
        }
        tree[current].value = tree[successor].value;
        if (successorParent == current) {
            tree[current].right = tree[successor].right;
        }
        else {
            tree[successorParent].left = tree[successor].right;
        }
        freeStack[++freeStackTop] = successor;
    }
    length--;

    return removed;
}

int SortedIndexedList::search(TComp e) const {
    int current = root;
    int pos = 0;
    while (current != NULL_NODE) {
        if (tree[current].value == e) return pos + tree[current].leftCount;
        if (r(tree[current].value, e)) {
            pos += tree[current].leftCount + 1;
            current = tree[current].right;
        }
        else {
            current = tree[current].left;
        }
    }
    return -1;
}

ListIterator SortedIndexedList::iterator(){
    return ListIterator(*this);
}

//destructor
SortedIndexedList::~SortedIndexedList() {
    delete[] tree;
    delete[] freeStack;

}