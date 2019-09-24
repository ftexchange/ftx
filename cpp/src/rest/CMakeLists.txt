file(GLOB SOURCES "*cc")
add_library(rest STATIC ${SOURCES})
target_include_directories(rest PUBLIC)
target_link_libraries(rest)
