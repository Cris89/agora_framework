# Check for the presence of the agora framework
#
# The following variables are set when agora is found:
# 	HAVE_AGORA		= Set to true, if agora have been found.
# 	AGORA_INCLUDES  	= Include path for the header files of agora
# 	AGORA_LIBRARIES		= Link these to use agora

## -----------------------------------------------------------------------------
## Check for the header files

set( AGORA_SOURCE_PATH /home/cris/agora )
set( AGORA_BINARY_PATH /home/cris/agora/build )
set( AGORA_INSTALL_PATH /usr/local )
set( MQTT_ROOT $ENV{MQTT_ROOT})

# check for the header of the agoraLocalAppHandler module
find_path (AGORA_AGORALOCALAPPHANDLER_INCLUDES agora/framework.hpp
  PATHS ${AGORA_INSTALL_PATH}/include ${AGORA_SOURCE_PATH}/include
  NO_DEFAULT_PATH
  )


find_path (AGORA_AGORALOCALAPPHANDLER_INCLUDES agora/framework.hpp
  PATHS /usr/local/include /usr/include ${CMAKE_EXTRA_INCLUDES}
  )



# check for MQTT
find_path (AGORA_MQTT_INCLUDES MQTTClient.h
  PATHS ${MQTT_ROOT}/include
  NO_DEFAULT_PATH
  )


find_path (AGORA_MQTT_INCLUDES MQTTClient.h
  PATHS /usr/local/include /usr/include ${CMAKE_EXTRA_INCLUDES}
  )

# compose the real list of paths
set( AGORA_INCLUDES ${AGORA_AGORALOCALAPPHANDLER_INCLUDES} ${AGORA_MQTT_INCLUDES} )

list( REMOVE_DUPLICATES AGORA_INCLUDES )

## -----------------------------------------------------------------------------
## Check for the libraries

# check for the agoraLocalAppHandler library
find_library( AGORALOCALAPPHANDLER_LIBRARIES libagora_agoraLocalAppHandler.a libagora_agoraLocalAppHandler.so agora_agoraLocalAppHandler
	PATHS ${AGORA_BINARY_PATH}/framework/agoraLocalAppHandler ${AGORA_INSTALL_PATH}/lib
	NO_DEFAULT_PATH
	)
if( NOT AGORALOCALAPPHANDLER_LIBRARIES )
	find_library( MQTT_LIBRARIES libagora_agoraLocalAppHandler.a libagora_agoraLocalAppHandler.so agora_agoraLocalAppHandler
		PATHS /usr/local/lib /usr/lib /lib ${AGORALOCALAPPHANDLER_ROOT}
		)
endif( NOT AGORALOCALAPPHANDLER_LIBRARIES )

# check for the MQTT library
find_library (MQTT_LIBRARIES_A libpaho-mqtt3a.so libpaho-mqtt3as.so
  PATHS ${MQTT_ROOT}/lib ${MQTT_ROOT}/lib64
  NO_DEFAULT_PATH
  )

find_library (MQTT_LIBRARIES_C libpaho-mqtt3c.so libpaho-mqtt3cs.so
  PATHS ${MQTT_ROOT}/lib ${MQTT_ROOT}/lib64
  NO_DEFAULT_PATH
  )


find_library (MQTT_LIBRARIES_A libpaho-mqtt3a.so libpaho-mqtt3as.so
  PATHS /usr/local/lib /usr/lib /lib ${CMAKE_EXTRA_LIBRARIES}
  )

find_library (MQTT_LIBRARIES_C libpaho-mqtt3c.so libpaho-mqtt3cs.so
  PATHS /usr/local/lib /usr/lib /lib ${CMAKE_EXTRA_LIBRARIES}
  )

set( MQTT_LIBRARIES ${MQTT_LIBRARIES_A} ${MQTT_LIBRARIES_C})

# append the libraries
set( AGORA_LIBRARIES ${AGORALOCALAPPHANDLER_LIBRARIES} ${MQTT_LIBRARIES} )

list( REMOVE_DUPLICATES AGORA_LIBRARIES )










## -----------------------------------------------------------------------------
## Actions taken when all components have been found

if( AGORA_AGORALOCALAPPHANDLER_INCLUDES AND MQTT_LIBRARIES )
  set( HAVE_AGORA TRUE )
else( AGORA_AGORALOCALAPPHANDLER_INCLUDES AND MQTT_LIBRARIES )
  if( NOT AGORA_FIND_QUIETLY )
    if( NOT AGORA_AGORALOCALAPPHANDLER_INCLUDES )
      message( STATUS "Unable to find agora header files!" )
    endif( NOT AGORA_AGORALOCALAPPHANDLER_INCLUDES )
    if( NOT MQTT_LIBRARIES )
      message( STATUS "Unable to find MQTT library files!" )
    endif( NOT MQTT_LIBRARIES )
  endif( NOT AGORA_FIND_QUIETLY )
endif( AGORA_AGORALOCALAPPHANDLER_INCLUDES AND MQTT_LIBRARIES )

if( HAVE_AGORA )
  if( NOT AGORA_FIND_QUIETLY )
    message( STATUS "Found components for agora" )
    message( STATUS "AGORA_INCLUDES .... = ${AGORA_INCLUDES}" )
    message( STATUS "AGORA_LIBRARIES ... = ${AGORA_LIBRARIES}" )
  endif( NOT AGORA_FIND_QUIETLY )
else( HAVE_AGORA )
  if( AGORA_FIND_QUIETLY )
    message( FATAL_ERROR "Could not find agora!" )
  endif( AGORA_FIND_QUIETLY )
endif( HAVE_AGORA )

mark_as_advanced (
  HAVE_AGORA
  AGORA_INCLUDES
  AGORA_LIBRARIES
  )
