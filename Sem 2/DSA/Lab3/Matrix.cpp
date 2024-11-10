#include "Matrix.h"
#include <exception>
using namespace std;


Matrix::Matrix(int nrLines, int nrCols) {
    nr_Lines=nrLines;
    nr_Cols=nrCols;
    capacity=4;
    size=0;
    elems=new triple[capacity];
}


int Matrix::search(int i, int j) const {
    //do a binary search for the element based on the e1 first and e2 second  values
    int left=0,right=size-1;
    while(left<=right) {
        int mid = (left + right) / 2;
        if (elems[mid].e1 == i and elems[mid].e2 == j)
            return mid;
        if (elems[mid].e1 < i or (elems[mid].e1 == i and elems[mid].e2 < j))
            left=mid+1;
        else
            right=mid-1;
    }
    return -1;
}


int Matrix::nrLines() const {
	return nr_Lines;
}


int Matrix::nrColumns() const {
	return nr_Cols;
}

TElem Matrix::element(int i, int j) const {
	if(i<0 or i>nr_Lines or j<0 or j>nr_Cols) {
        throw exception();
        return NULL_TELEM;
    }
    int pos=search(i,j);
    if(pos!=-1)
        return elems[pos].value;
    return NULL_TELEM;
}


TElem Matrix::modify(int i, int j, TElem e) {
    if(i<0 or i>nr_Lines or j<0 or j>nr_Cols)
        throw exception();
    int pos=search(i,j);
    auto old=elems[pos].value;
    if(pos!=-1) {
        if(e==NULL_TELEM)
            remove(pos);
        else
            elems[pos].value=e;
        return old;
    }
    auto newElem=triple{e,i,j};
    add(newElem);
    return NULL_TELEM;
}

void Matrix::update(int pos, triple element) {
    elems[pos]=element;
}
void Matrix::add(triple element) {
    if (size == capacity)
        resize();
    //add the element in order to keep the array sorted
    //search for the next smallest element with binary search and insert it
    int left = 0, right = size - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (elems[mid].e1 < element.e1 or (elems[mid].e1 == element.e1 and elems[mid].e2 < element.e2))
            left = mid + 1;
        else
            right = mid - 1;
    }
    for (int k = size; k > left; k--)
        elems[k] = elems[k - 1];
    elems[left] = element;
    size++;
}

void Matrix::remove(int pos) {
    for(int k=pos;k<size-1;k++)
        elems[k]=elems[k+1];
    size--;
}

void Matrix::resize() {
    //double the capacity
    capacity<<=1;
    triple *newElems;
    newElems = new triple[capacity];
    for(int i=0;i<size;i++)
        newElems[i]=elems[i];
    delete[] elems;
    elems=newElems;
}

