# Check for the presence of the MQTT framework
#
# The following variables are set when MQTT is found:
# 	HAVE_MQTT	= Set to true, if MQTT have been found.
# 	MQTT_INCLUDES  	= Include path for the header files of MQTT
# 	MQTT_LIBRARIES	= Link these to use agora

## -----------------------------------------------------------------------------
## Check for the header files

# check for the header of the client module
find_path( MQTT_INCLUDES MQTTClient.h PATHS
                    /usr/local/include
                    /usr/include
                    ${MQTT_ROOT}/include
          )

## -----------------------------------------------------------------------------
## Check for the libraries

# check for the MQTT library
find_library( MQTT_LIBRARIES libpaho-mqtt3a.so libpaho-mqtt3as.so lib/libpaho-mqtt3c.so libpaho-mqtt3cs.so
	PATHS ${MQTT_ROOT}/lib
	NO_DEFAULT_PATH
	)
if( NOT MQTT_LIBRARIES )
	find_library( MQTT_LIBRARIES libpaho-mqtt3a.so libpaho-mqtt3as.so lib/libpaho-mqtt3c.so libpaho-mqtt3cs.so
		PATHS /usr/local/lib /usr/lib /lib
		)
endif( NOT MQTT_LIBRARIES )









## -----------------------------------------------------------------------------
## Actions taken when all components have been found

if( MQTT_INCLUDES AND MQTT_LIBRARIES )
  set( HAVE_MQTT TRUE )
else( MQTT_INCLUDES AND MQTT_LIBRARIES )
  if( NOT MQTT_FIND_QUIETLY )
    if( NOT MQTT_INCLUDES )
      message( STATUS "Unable to find MQTT header files!" )
    endif( NOT MQTT_INCLUDES )
    if( NOT MQTT_LIBRARIES )
      message( STATUS "Unable to find MQTT library files!" )
    endif( NOT MQTT_LIBRARIES )
  endif( NOT MQTT_FIND_QUIETLY )
endif( MQTT_INCLUDES AND MQTT_LIBRARIES )

if( HAVE_MQTT )
  if( NOT MQTT_FIND_QUIETLY )
    message( STATUS "Found components for MQTT" )
    message( STATUS "MQTT_INCLUDES .... = ${MQTT_INCLUDES}" )
    message( STATUS "MQTT_LIBRARIES ... = ${MQTT_LIBRARIES}" )
  endif( NOT MQTT_FIND_QUIETLY )
else( HAVE_MQTT )
  if( MQTT_FIND_QUIETLY )
    message( FATAL_ERROR "Could not find MQTT!" )
  endif( MQTT_FIND_QUIETLY )
endif( HAVE_MQTT )

mark_as_advanced (
  HAVE_MQTT
  MQTT_INCLUDES
  MQTT_LIBRARIES
  )
