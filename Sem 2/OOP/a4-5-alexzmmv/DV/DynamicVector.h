#pragma once

#include <stdexcept>

template <class TElem>
class DynamicVector {
private:
    TElem* elems;
    int size;
    int capacity;

    void resize() {
        this->capacity <<= 1;
        auto newElems = new TElem[this->capacity];
        for (int i = 0; i < this->size; i++)
            newElems[i] = this->elems[i];
        delete[] this->elems;
        this->elems = newElems;
    }
public:
    class Citerator{
        private:
            TElem* ptr;
            TElem* begin;
            TElem* end;
        public:
            Citerator(TElem* p, TElem* end): ptr{p}, begin{p}, end(end){}
            Citerator operator++(){
                this->ptr++;
                if(this->ptr==end)
                    this->ptr=begin;
                return *this;
            }
            Citerator operator++(int){
                this->ptr++;
                if(this->ptr==end)
                    this->ptr=begin;
                return *this;
            }
            bool operator!=(const Citerator& it){
                return ptr!=it.ptr;
            }
            TElem& operator*(){
                return *ptr;
            }
    };
    class Iterator{
        private:
            TElem* ptr;
        public:
            Iterator(TElem* p): ptr{p}{}
            Iterator operator++(){
                this->ptr++;
                return *this;
            }
            Iterator operator++(int){
                this->ptr++;
                return *this;
            }
            bool operator!=(const Iterator& it){
                return ptr!=it.ptr;
            }
            TElem& operator*(){
                return *ptr;
            }
    };
    Iterator begin(){
        return Iterator{elems};
    }
    Iterator end(){
        return Iterator{elems+size};
    }
    DynamicVector(){
        size=0;
        capacity=8;
        elems=new TElem[capacity];
    }
    Citerator beginc(){
        return Citerator{elems, elems + size};
    }


    ~DynamicVector()=default;

    void push_back(TElem elem) {
        if (this->size == this->capacity)
            this->resize();
        this->elems[this->size++] = elem;
    }


    void erase(int pos) {
        for (int i = pos; i < this->size - 1; i++)
            this->elems[i] = this->elems[i + 1];
        this->size--;
    }

    void update(int pos, TElem elem) {
        this->elems[pos] = elem;
    }

    int getSize() {
        return this->size;
    }

    int search(TElem elem) {
        for (int i = 0; i < this->size; i++)
            if (this->elems[i] == elem)
                return i;
        return -1;
    }
    TElem& operator[](int i){
        return elems[i];
    }

    void sort(bool (*cmp)(TElem, TElem)){
        for(int i=0;i<size-1;i++)
            for(int j=i+1;j<size;j++)
                if(cmp(elems[i],elems[j])){
                    TElem aux=elems[i];
                    elems[i]=elems[j];
                    elems[j]=aux;}
    }
};