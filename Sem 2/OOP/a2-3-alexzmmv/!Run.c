#include <crtdbg.h>
#include "UI/UI.h"
#include "tests/test.h"
#include <stdio.h>
void populate_repo(Repository *repo) {
    addmedicine(repo, "Paracetamol", 100, 100, 10);
    addmedicine(repo, "Nurofen", 200, 50, 15);
    addmedicine(repo, "Aspirin", 300, 30, 20);
    addmedicine(repo, "VitaminC", 400, 20, 25);
    addmedicine(repo, "VitaminD", 500, 10, 30);
    addmedicine(repo, "VitaminE", 600, 5, 35);
}

int main() {
    testall();
    Repository* repo = createRepository(10);
    populate_repo(repo);
    startUI(repo);
    destroyRepository(repo);
    _CrtDumpMemoryLeaks();
    return 0;
}
//Asig4 P5