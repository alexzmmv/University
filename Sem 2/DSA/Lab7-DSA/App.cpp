#include <iostream>

#include "ShortTest.h"
#include "ExtendedTest.h"

int main(){
    testAll();
    testAllExtended();
    std::cout<<"Finished all Tests!"<<std::endl;
	system("pause");
}