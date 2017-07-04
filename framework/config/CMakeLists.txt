###############################################
##           Configuration file              ##
###############################################

message( STATUS "" )
message( STATUS "*********************************" )
message( STATUS "**        CONFIG STATUS        **" )
message( STATUS "*********************************" )
message( STATUS "Install prefix..................: ${CMAKE_INSTALL_PREFIX}" )

# --- print the result of the configuration
if( LIB_STATIC )
        message( STATUS "Library type....................: STATIC" )
else( LIB_STATIC )
        message( STATUS "Library type....................: DYNAMIC" )
endif( LIB_STATIC )

# check if we are going to build the test executable
if( HAVE_MQTT )
        message( STATUS  "MQTT library.......: FOUND" )
else( HAVE_MQTT )
        message( STATUS  "MQTT library.......: NOT FOUND! ( please, install MQTT )" )
endif( HAVE_MQTT )

message( STATUS "" )










###############################################################
##           FindAGORALOCALAPPHANDLER cmake file             ##
###############################################################

# customizing the FindCLIENT.cmake file for the integration with external applications
configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/FindAGORALOCALAPPHANDLER.cmake.in"
  "${PROJECT_SOURCE_DIR}/cmake/FindAGORALOCALAPPHANDLER.cmake"
  @ONLY
  )

# install the config file
install( FILES "${PROJECT_SOURCE_DIR}/cmake/FindAGORALOCALAPPHANDLER.cmake" DESTINATION lib/cmake )
