#pragma once

#include "../Controller.h"
#include "../../VoidDynamicalArray/DynamicalvArray.h"

int addMedicine(Repository* repo, char* name, int concentration, int quantity, float price);
int removeMedicine(Repository* repo, char* name, int concentration);
int updateMedicine(Repository* repo, char* name, int concentration, int quantity, float price);
int undo(Repository* repo);
int redo(Repository* repo);