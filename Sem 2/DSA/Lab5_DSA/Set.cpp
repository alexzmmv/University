#include <cstring>
#include "Set.h"
#include "SetITerator.h"


Set::Set() {
    /*
     * Complexity:
     * Tetha(1)
     */
    elements = new Node[8];
    capacity = 8;
    for(int i = 0; i < capacity; i++) {
        elements[i].next = i+1;
    }
    elements[capacity-1].next = -2;
    _size = 0;
    head = -1;
    firstEmpty = 0;
    last=-1;
}

void Set::resize() {
    /*
     * Complexity:
     * Tetha(capacity)
     */
    Node* newElements = new Node[capacity << 1];
    memcpy(newElements, elements, capacity * sizeof(Node));
    delete[] elements;

    elements = newElements;
    for(int i = capacity; i < capacity << 1; i++) {
        elements[i].next = i+1;
    }
    int current = firstEmpty;
    firstEmpty=capacity;
    elements[current].next = capacity;
    capacity <<= 1;
    elements[capacity-1].next = -2;
}

int Set::nextEmpty() {
    /*
     * Complexity:
     * Tetha(1)
     */
    int current=firstEmpty;
    firstEmpty = elements[firstEmpty].next;
    return current;
}

bool Set::add(TElem elem) {
    /*
     * Complexity:
     * O(n) amortized
     */
    if (_size == capacity-2) {
        resize();
    }
    // if the set is empty
    if (head == -1) {
        head = nextEmpty();
        elements[head].value = elem;
        elements[head].next = -1;
        last = head;
        _size++;
            return true;
    }
    // if the element is not already in the set
    if(!search(elem)) {
        elements[last].next = firstEmpty;
        last = nextEmpty();
        elements[last].value = elem;
        elements[last].next = -1;
        _size++;
        return true;
    }
    return false;
}


bool Set::remove(TElem elem) {
    /*
     * Complexity:
     * Tetha(n)
     */
    if (head == -1) {
        return false;
    }
    if (elements[head].value == elem) {
        // if the element is the head
        int toDelete = head;
        head = elements[head].next;
        elements[toDelete].next = firstEmpty;
        elements[toDelete].value = NULL_TELEM;
        firstEmpty = toDelete;
        _size--;
        return true;
    }
    // if the element is not the head
    int current = head;
    while (elements[current].next != -1) {
        if (elements[elements[current].next].value == elem) {
            int toDelete = elements[current].next;
            elements[current].next = elements[elements[current].next].next;
            elements[toDelete].next = firstEmpty;
            elements[toDelete].value = NULL_TELEM;
            firstEmpty = toDelete;
            _size--;
            return true;
        }
        current = elements[current].next;
    }
	return false;
}

bool Set::search(TElem elem) const {
    /*
     * Complexity:
     * Tetha(n)
     */
    int current = head;
    while (current != -1) {
        if (elements[current].value == elem) {
            return true;
        }
        current = elements[current].next;
    }
    return false;
}


int Set::size() const {
    return _size;
}


bool Set::isEmpty() const {
    return _size == 0;
}


Set::~Set() {
    delete[] elements;
}

void Set::filter(Condition cond) {
    /*
     * Complexity:
     * Tetha(n)
     */
    auto current=head;
    while(current!=-1){
        if(!cond(elements[current].value)){
            if(current==head){
                head=elements[current].next;
                elements[current].next=firstEmpty;
                firstEmpty=current;
                current=head;
            }
            else{
                auto prev=head;
                while(elements[prev].next!=current){
                    prev=elements[prev].next;
                }
                elements[prev].next=elements[current].next;
                elements[current].next=firstEmpty;
                firstEmpty=current;
                current=elements[prev].next;
            }
            _size--;
        }
        else{
            current=elements[current].next;
        }
    }
}

SetIterator Set::iterator() const {
	return SetIterator(*this);
}