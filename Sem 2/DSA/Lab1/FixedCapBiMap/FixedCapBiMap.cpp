#include "FixedCapBiMap.h"
#include "FixedCapBiMapIterator.h"
#include <exception>
using namespace std;

#define key first
#define value second

FixedCapBiMap::FixedCapBiMap(int capacity) {
    if(capacity<1)
        throw std::exception();
    elements = new TElem[capacity];
    this->capacity=capacity;
    this->MapSize=0;
}

FixedCapBiMap::~FixedCapBiMap() {
	    delete[] elements;
}

bool FixedCapBiMap::add(TKey c, TValue v){
	if(this->isFull())
        throw exception();
    int count=0;
    int index=0;
    while(count<2 and index<MapSize) {
        if (this->elements[index].key == c)
            count++;
    index++;
    }
    if(count==2)
        return false;
    elements[MapSize].key=c;
    elements[MapSize++].value=v;
    return true;
}

ValuePair FixedCapBiMap::search(TKey c) const{
	ValuePair res;
    res.first=res.second=NULL_TVALUE;
    int nrfound=0;
    int index=-1;
    while(++index<MapSize and nrfound<2)
        if(elements[index].first==c)
            if(nrfound==0){
                res.first=elements[index].second;
                nrfound++;
            }else{
                res.second=elements[index].second;
                nrfound++;
            }
	return res;
}

bool FixedCapBiMap::remove(TKey c, TValue v){
	TElem s=TElem (c,v);
    int i1=-1,i2=-1;
    for(int i=0;i<MapSize;i++)
        if(elements[i]==s){
            elements[i]=elements[--MapSize];
            return true;
        }
	return false;
}


int FixedCapBiMap::size() const {
	return this->MapSize;
}

bool FixedCapBiMap::isEmpty() const{
	return MapSize==0;
}

bool FixedCapBiMap::isFull() const {
	return MapSize==capacity;
}

FixedCapBiMapIterator FixedCapBiMap::iterator() const {
	return FixedCapBiMapIterator(*this);
}