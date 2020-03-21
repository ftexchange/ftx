file(GLOB SOURCES "*cc")
add_library(util STATIC ${SOURCES})
target_include_directories(util PUBLIC)

target_link_libraries(util OpenSSL::SSL OpenSSL::Crypto)
