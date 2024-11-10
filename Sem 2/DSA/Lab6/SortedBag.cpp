#include <iostream>
#include <cstring>
#include "SortedBag.h"

#include "SortedBagIterator.h"

SortedBag::SortedBag(Relation r) {
    this->r=r;
    capacityOfArray=200;
    elements=new Node[capacityOfArray];
    firstEmpty=0;
    sizeOfBag=0;
}

int SortedBag::hash(TComp e)const{
    if (e<0) {
        e=-e;
    }
    return e%capacityOfArray;
}
void SortedBag::setNextEmpty() {
    if(elements[firstEmpty].data==NULL_TCOMP) {
        return;
    }
    for(int i=0;i<capacityOfArray;i++) {
        if (elements[i].data==NULL_TCOMP) {
            firstEmpty=i;
            return;
        }
    }
}
void SortedBag::resize() {
    capacityOfArray <<= 1;
    int localFirstEmpty = 0;
    Node *newElements = new Node[capacityOfArray];
    for (int i = 0; i < capacityOfArray; i++) {
        newElements[i].data = NULL_TCOMP;
        newElements[i].next = -1;
    }
    for (int i = 0; i < capacityOfArray >> 1; i++) {
        int index = hash(elements[i].data);
        if (elements[i].data != NULL_TCOMP) {
            if (newElements[index].data == NULL_TCOMP) {
                newElements[index].data = elements[i].data;
                newElements[index].next = -1;
                //set the first empty position
                for(int j=firstEmpty;j<capacityOfArray;j++) {
                    if (newElements[j].data==NULL_TCOMP) {
                        localFirstEmpty=j;
                        break;
                    }
                }
            } else {
                int current = index;
                while (newElements[current].next != -1) {
                    current = newElements[current].next;
                }
                newElements[current].next = localFirstEmpty;
                newElements[localFirstEmpty].data = elements[i].data;
                newElements[localFirstEmpty].next = -1;
                for(int j=firstEmpty;j<capacityOfArray;j++) {
                    if (newElements[j].data==NULL_TCOMP) {
                        localFirstEmpty=j;
                        break;
                    }
                }
                for(int j=0;j<capacityOfArray;j++) {
                    if (elements[j].data == elements[i].data) {
                        elements[j].next = -1;
                        break;
                    }
                }
            }
        }
    }

    elements = newElements;
    firstEmpty = localFirstEmpty;
}

void SortedBag::add(TComp e) {
    int index=hash(e);
    sizeOfBag++;
    if (1.0*sizeOfBag/capacityOfArray>0.75) {
        resize();
    }
    //if the element position is empty just add it
    if (elements[index].data==NULL_TCOMP) {
        elements[index].data=e;
        setNextEmpty();
        return;
    }
    //if the element is already in the bag
    //add it to the first empty position then link it to the previous element
    int current=index;
    while (elements[current].next!=-1)
        current=elements[current].next;

    //extra stuff
    if(firstEmpty!=NULL_TCOMP)
        setNextEmpty();

    elements[firstEmpty].data=e;
    elements[firstEmpty].next=-1;
    elements[current].next=firstEmpty;
    setNextEmpty();
}


bool SortedBag::remove(TComp e) {
    //tried to remove an element from an empty bag
    //it works, but not completely
    //tried to copy the code from the lecture
    //it doesn't work at all
    int index=hash(e);
    //if the element is the first and the only one in the list with that hash, just remove it
    if(elements[index].data==NULL_TCOMP) {
        return false;
    }
    if(elements[index].data==e && elements[index].next==-1) {
        elements[index].data=NULL_TCOMP;
        elements[index].next=-1;
        sizeOfBag--;
        if(index<firstEmpty)
            firstEmpty=index;
        return true;
    }
    struct{
        int prev;
        int current;
    }e1,e2;
    //e1, e2 positions with previos and current element

    //search for the element
    e1.current=index;
    e1.prev=-1;
    while(e1.current!=-1 && elements[e1.current].data!=e) {
        e1.prev=e1.current;
        e1.current=elements[e1.current].next;
    }
    //if the element is not in the list
    if(e1.current==-1) {
        return false;
    }
    //element is in the list on the position e1.current

    e2.prev=e1.current;
    e2.current=elements[e1.current].next;
    //search another element with the same hash value as e
    bool over=false;
    do{
        e2.prev=e1.current;
        e2.current=elements[e1.current].next;
        while(e2.current!=-1 && hash(elements[e2.current].data)!=index) {
            e2.prev=e2.current;
            e2.current=elements[e2.current].next;
        }
        //if there is no other element with the same hash value as e
        if(e2.current==-1) {
            over=true;
            break;
        }
        //there is another element with the same hash value as e
        elements[e1.current].data=elements[e2.current].data;
        e1=e2;
    }while (!over);

    elements[e1.current].data=NULL_TCOMP;
    elements[e1.current].next=-1;
    if(e1.current<firstEmpty)
        firstEmpty=e1.current;
    sizeOfBag--;
    return true;

}


bool SortedBag::search(TComp elem) const {
    int index=hash(elem);
    while(index!=-1) {
        if (elements[index].data==elem) {
            return true;
        }
        index=elements[index].next;
    }
    return false;
}



int SortedBag::nrOccurrences(TComp elem) const {
    int index=hash(elem);
    int count=0;
    while(index!=-1) {
        if (elements[index].data==elem) {
            count++;
        }
        index=elements[index].next;
    }
    return count;
}



int SortedBag::size() const {
    return sizeOfBag;
}


bool SortedBag::isEmpty() const {
    return sizeOfBag==0;
}


SortedBagIterator SortedBag::iterator() const {
    return SortedBagIterator(*this);
}


SortedBag::~SortedBag() {
}
