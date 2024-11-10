#include "SMMIterator.h"
#include "SortedMultiMap.h"
#include <iostream>
#include <vector>
#include <exception>
using namespace std;

SortedMultiMap::SortedMultiMap(Relation r) {
    relation= r;
    sizeOfSMM= 0;
    head= nullptr;
    tail= nullptr;
}

void SortedMultiMap::add(TKey c, TValue v) {
    Node* newNode= new Node;
    newNode->elem= TElem {c, v};
    if (head == nullptr){
        head= newNode;
        tail= newNode;
        newNode->next= nullptr;
        newNode->prev= nullptr;
    }
    else{
        Node* current= head;
        while (current != nullptr && relation(current->elem.first, c)){
            current= current->next;
        }
        if (current == nullptr){
            tail->next= newNode;
            newNode->prev= tail;
            tail= newNode;
            newNode->next= nullptr;
        }
        else{
            if (current->prev == nullptr){
                head= newNode;
                newNode->prev= nullptr;
                newNode->next= current;
                current->prev= newNode;
            }
            else{
                current->prev->next= newNode;
                newNode->prev= current->prev;
                newNode->next= current;
                current->prev= newNode;
            }
        }
    }
    sizeOfSMM++;
}

vector<TValue> SortedMultiMap::search(TKey c) const {
    Node* current= head;
    vector<TValue> values;
    while (current != nullptr){
        if (current->elem.first == c){
            values.push_back(current->elem.second);
        }
        current= current->next;
    }
    return values;
}

bool SortedMultiMap::remove(TKey c, TValue v) {
    Node* current= head;
    while (current != nullptr){
        if (current->elem.first == c && current->elem.second == v){
            if (current->prev == nullptr && current->next == nullptr){
                head= nullptr;
                tail= nullptr;
            }
            else if (current->prev == nullptr){
                head= current->next;
                current->next->prev= nullptr;
            }
            else if (current->next == nullptr){
                tail= current->prev;
                current->prev->next= nullptr;
            }
            else{
                current->prev->next= current->next;
                current->next->prev= current->prev;
            }
            delete current;
            sizeOfSMM--;
            return true;
        }
        current= current->next;
    }
    return false;
}


int SortedMultiMap::size() const {
    return sizeOfSMM;
}

bool SortedMultiMap::isEmpty() const {
    return sizeOfSMM == 0;
}

SMMIterator SortedMultiMap::iterator() const {
	return SMMIterator(*this);
}

SortedMultiMap::~SortedMultiMap() {
	    Node* current= head;
    while (current != nullptr){
        Node* next= current->next;
        delete current;
        current= next;
    }
}
