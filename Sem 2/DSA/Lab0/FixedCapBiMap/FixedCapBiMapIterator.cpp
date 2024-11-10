#include "FixedCapBiMap.h"
#include "FixedCapBiMapIterator.h"
#include <exception>
using namespace std;


FixedCapBiMapIterator::FixedCapBiMapIterator(const FixedCapBiMap& d) : map(d)
{
    this->size=d.MapSize;
    this->index=0;
}


void FixedCapBiMapIterator::first() {
	index=0;
}


void FixedCapBiMapIterator::next() {
	int a=valid();
    if(!a) {
        throw exception();
        return;
    }
    index+=a;
}


TElem FixedCapBiMapIterator::getCurrent(){
	if(valid())
        return map.elements[index];
	throw exception();
}


bool FixedCapBiMapIterator::valid() const {
	return index!=size;
}



