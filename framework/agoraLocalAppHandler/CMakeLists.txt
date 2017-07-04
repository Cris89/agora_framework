###############################################
##      Compiling the framework module       ##
###############################################

set( AGORALOCALAPPHANDLER_LIB_NAME "agoraLocalAppHandler" )


# -------- Defining the source/header files
set( AGORALOCALAPPHANDLER_SRC_PATH ${CMAKE_CURRENT_SOURCE_DIR}/src )
set( AGORALOCALAPPHANDLER_HDR_PATH ${CMAKE_CURRENT_SOURCE_DIR}/include )

set( AGORALOCALAPPHANDLER_HEADERS ${AGORALOCALAPPHANDLER_HDR_PATH}/agora/appStruct.hpp
				    ${AGORALOCALAPPHANDLER_HDR_PATH}/agora/framework.hpp
				    ${AGORALOCALAPPHANDLER_HDR_PATH}/agora/mqtt.hpp
				    ${AGORALOCALAPPHANDLER_HDR_PATH}/agora/topics.hpp
				    ${AGORALOCALAPPHANDLER_HDR_PATH}/agora/OPs.hpp
   )

set( AGORALOCALAPPHANDLER_SOURCES ${AGORALOCALAPPHANDLER_SRC_PATH}/appStruct.cpp
				    ${AGORALOCALAPPHANDLER_SRC_PATH}/framework.cpp
				    ${AGORALOCALAPPHANDLER_SRC_PATH}/mqtt.cpp
				    ${AGORALOCALAPPHANDLER_SRC_PATH}/topics.cpp
				    ${AGORALOCALAPPHANDLER_SRC_PATH}/OPs.cpp
   )

# --------  Build the module
include_directories( ${AGORALOCALAPPHANDLER_HDR_PATH} ${MQTT_INCLUDES})

if( LIB_STATIC )
	add_library( ${AGORALOCALAPPHANDLER_LIB_NAME} STATIC ${AGORALOCALAPPHANDLER_SOURCES} ${AGORALOCALAPPHANDLER_HEADERS} )
else( LIB_STATIC )
        add_library( ${AGORALOCALAPPHANDLER_LIB_NAME} SHARED ${AGORALOCALAPPHANDLER_SOURCES} ${AGORALOCALAPPHANDLER_HEADERS} )
endif( LIB_STATIC )

target_link_libraries( ${AGORALOCALAPPHANDLER_LIB_NAME} ${MQTT_LIBRARIES} )

# ------ Install the module
install( TARGETS ${AGORALOCALAPPHANDLER_LIB_NAME} DESTINATION lib )
install( FILES ${AGORALOCALAPPHANDLER_HEADERS} DESTINATION include/agora )
