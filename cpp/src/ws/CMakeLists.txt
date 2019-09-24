file(GLOB SOURCES "*cc")
add_library(ws STATIC ${SOURCES})
target_include_directories(ws PUBLIC)
target_link_libraries(ws)
