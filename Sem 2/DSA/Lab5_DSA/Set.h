#pragma once
//DO NOT INCLUDE SETITERATOR

#define NULL_TELEM -111111
typedef int TElem;
typedef bool(*Condition)(TElem);
//DO NOT CHANGE THIS PART
class SetIterator;

class Set {
	friend class SetIterator;

    private:
        struct Node {
            TElem value=NULL_TELEM;
            int next=-2;
        };
        Node* elements;
        int capacity;
        int _size;
        int head;
        int firstEmpty;
        int last;
        void resize();
        int nextEmpty();
    public:
        //implicit constructor
        Set();

        //adds an element to the set
		//returns true if the element was added, false otherwise (if the element was already in the set and it was not added)
        bool add(TElem e);

        //removes an element from the set
		//returns true if e was removed, false otherwise
        bool remove(TElem e);

        //checks whether an element belongs to the set or not
        bool search(TElem elem) const;

        //returns the number of elements;
        int size() const;

        //check whether the set is empty or not;
        bool isEmpty() const;

        //return an iterator for the set
        SetIterator iterator() const;

        //keeps in the set only elements that respect the given condition
        void filter(Condition cond);
        // destructor
        ~Set();

};





