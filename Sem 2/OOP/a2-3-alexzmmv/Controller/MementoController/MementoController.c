#include "MementoController.h"

int addMedicine(Repository* repo, char* name, int concentration, int quantity, float price){
    DynamicArray*undo_meds = getMeds(repo);
    addv(repo->undoStack,undo_meds);
    destroyv(repo->redoStack);
    repo->redoStack = createDynamicalVArray(10);
    return addmedicine(repo, name, concentration, quantity, price);
}

int removeMedicine(Repository* repo, char* name, int concentration){
    DynamicArray *undo_meds = getMeds(repo);
    addv(repo->undoStack,undo_meds);
    destroyv(repo->redoStack);
    repo->redoStack = createDynamicalVArray(10);
    return removemedicine(repo, name, concentration);
}

int updateMedicine(Repository* repo, char* name, int concentration, int quantity, float price){
    DynamicArray *undo_meds = getMeds(repo);
    addv(repo->undoStack,undo_meds);
    destroyv(repo->redoStack);
    repo->redoStack = createDynamicalVArray(10);
    return updatemedicine(repo, name, concentration, quantity, price);
}

int undo(Repository* repo){
    if (repo->undoStack->length <= 0)
        return 0;
    DynamicArray *next_meds = popv(repo->undoStack);
    addv(repo->redoStack,getMeds(repo));
    repo->meds = next_meds;
    free(next_meds);
    return 1;
}

int redo(Repository* repo){
    if(repo->redoStack->length <= 0)
        return 0;
    DynamicArray *curr_meds = getMeds(repo);
    addv(repo->undoStack,curr_meds);
    DynamicArray *redo_meds = popv(repo->redoStack);
    repo->meds = redo_meds;
    return 1;
}