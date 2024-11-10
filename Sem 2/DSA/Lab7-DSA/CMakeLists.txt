cmake_minimum_required(VERSION 3.27)
project(Lab7)

set(CMAKE_CXX_STANDARD 17)

add_executable(Lab7 app.cpp
        SortedIndexeList.cpp
        SortedIndexedList.h
        ListIterator.cpp
        ListIterator.h
        ShortTest.cpp
        ShortTest.h
        ExtendedTest.cpp
        ExtendedTest.h
)
