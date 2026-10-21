cmake_minimum_required(VERSION 3.20)
project(tqod CXX)
set(CMAKE_CXX_STANDARD 20)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# fmtownskit's runtime (the submodule; a kit being worked on: -DFMT_RUNTIME=.../fmtownskit/runtime)
set(FMT_RUNTIME ${CMAKE_CURRENT_SOURCE_DIR}/fmtownskit/runtime CACHE PATH "fmtownskit's runtime/")
# the game's and TBIOS's code, recompiled (python -m fmtownskit.recomp --out build/game ...)
set(RECOMP_DIR ${CMAKE_CURRENT_SOURCE_DIR}/build/game CACHE PATH "the recompiler's output")

include(${FMT_RUNTIME}/towns.cmake)

file(GLOB RECOMP_SRC ${RECOMP_DIR}/p_*.cpp)
add_library(game_recomp STATIC ${RECOMP_SRC})
target_include_directories(game_recomp PUBLIC ${FMT_RUNTIME})
target_compile_options(game_recomp PRIVATE -Wno-unused-label -Wno-unused-variable)

add_executable(tqod src/main.cpp ${RECOMP_DIR}/modules.cpp)
target_link_libraries(tqod game_recomp fmt_towns)
if(MINGW)
  target_link_options(tqod PRIVATE -static-libgcc -static-libstdc++)
endif()
