#include "test.h"
#include <assert.h>


void test_domain(){
    TElem m = createMed("Nurofen", 200, 20, 30);
    assert(strcmp(getName(m), "Nurofen") == 0);
    assert(getConcentration(m) == 200);
    assert(getQuantity(m) == 20);
    assert(getPrice(m) == 30);
}

void test_repo() {
    Repository* repo = createRepository(10);
    addmedicine(repo,"Nurofen", 200, 20, 30);
    assert(getLength(repo) == 1);
    assert(compareMeds(getMedAtPosition(repo, 0), m) == 1);
    destroyRepository(repo);
}

void test_controller() {
    Repository* repo = createRepository(10);
    addmedicine(repo, "Nurofen", 200, 20, 30);
    TElem m2 = createMed("Paracetamol", 100, 20, 30);
    addMedicine(repo, "Paracetamol", 100, 20, 30);
    assert(getLength(ctrl->repo) == 2);
    assert(compareMeds(getMedAtPosition(ctrl->repo, 1), m2) == 1);
    assert(0);
}

void test_dynamic_array() {
    DynamicArray* arr = createDynamicArray(10);
    TElem m = createMed("Nurofen", 200, 20, 30);
    add(arr, m);
    assert(getLength(arr) == 1);
    assert(compareMeds(getElement(arr, 0), m) == 1);
}

void testall() {
    test_domain();
    test_repo();
    test_controller();
    test_dynamic_array();
}
