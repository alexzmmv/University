cmake_minimum_required(VERSION 3.27)
project(oop_a10_alexzmmv)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)


include_directories(Domain)
include_directories(Repo)
include_directories(Controller)
include_directories(UI)
include_directories(sqlite3)
include_directories(UserPlanner)
include_directories(test)
include_directories(UI/Planner_gui_things)

set(CMAKE_PREFIX_PATH "D:/Qti/6.5.3/mingw_64")

find_package(Qt6 COMPONENTS
        Core
        Gui
        Widgets
        Charts
        REQUIRED)

add_executable(oop_a10_alexzmmv
        Domain/Activity.cpp
        Domain/Activity.h
        Domain/DateTime.cpp
        Domain/DateTime.h
        Repo/Repository.cpp
        Repo/Repository.h
        run.cpp
        UserPlanner/UserPlanner.h
        UserPlanner/UserPlanner.cpp
        Controller/Controller.h
        Controller/Controller.cpp
        UI/Console_ui.h
        UI/Console_ui.cpp
        Repo/DataBaseRepo.h
        Repo/DataBaseRepo.cpp
        sqlite3/sqlite3.h
        sqlite3/sqlite3.c
        Repo/FileRepo.h
        Repo/FileRepo.cpp
        UserPlanner/csvUserPlanner.h
        UserPlanner/csvUserPlanner.cpp
        UserPlanner/htmlUserPlanner.h
        UserPlanner/htmlUserPlanner.cpp
        test/test.h
        test/test.cpp
        UI/graphical_ui.cpp
        UI/graphical_ui.h
        UI/graphical_ui.ui
        Controller/CrudeCommands.h
        UI/Planner_gui_things/UserPlannerModelForGui.h
        UI/Planner_gui_things/UserPlannerModel.cpp
)


target_link_libraries(oop_a10_alexzmmv
        PRIVATE
        Qt::Core
        Qt::Gui
        Qt::Widgets
        Qt::Charts
)


if (WIN32 AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(DEBUG_SUFFIX)
    if (MSVC AND CMAKE_BUILD_TYPE MATCHES "Debug")
        set(DEBUG_SUFFIX "d")
    endif ()
    set(QT_INSTALL_PATH "${CMAKE_PREFIX_PATH}")
    if (NOT EXISTS "${QT_INSTALL_PATH}/bin")
        set(QT_INSTALL_PATH "${QT_INSTALL_PATH}/..")
        if (NOT EXISTS "${QT_INSTALL_PATH}/bin")
            set(QT_INSTALL_PATH "${QT_INSTALL_PATH}/..")
        endif ()
    endif ()
    if (EXISTS "${QT_INSTALL_PATH}/plugins/platforms/qwindows${DEBUG_SUFFIX}.dll")
        add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E make_directory
                "$<TARGET_FILE_DIR:${PROJECT_NAME}>/plugins/platforms/")
        add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                "${QT_INSTALL_PATH}/plugins/platforms/qwindows${DEBUG_SUFFIX}.dll"
                "$<TARGET_FILE_DIR:${PROJECT_NAME}>/plugins/platforms/")
    endif ()
    foreach (QT_LIB Core Gui Widgets)
        add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                "${QT_INSTALL_PATH}/bin/Qt6${QT_LIB}${DEBUG_SUFFIX}.dll"
                "$<TARGET_FILE_DIR:${PROJECT_NAME}>")
    endforeach (QT_LIB)
endif ()
