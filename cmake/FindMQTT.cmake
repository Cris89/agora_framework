# - Check for the presence of MQTT
#
# The following variables are set when MQTT is found:
#  HAVE_MQTT       = Set to true, if all components of MQTT
#                          have been found.
#  MQTT_INCLUDES   = Include path for the header files of MQTT
#  MQTT_LIBRARIES  = Link these to use MQTT
#
# It first search in MQTT_ROOT

set( MQTT_ROOT $ENV{MQTT_ROOT})

## -----------------------------------------------------------------------------
## Check for the header files

find_path (MQTT_INCLUDES MQTTClient.h
  PATHS ${MQTT_ROOT}/include
  NO_DEFAULT_PATH
  )


find_path (MQTT_INCLUDES MQTTClient.h
	PATHS /usr/local/include /usr/include ${CMAKE_EXTRA_INCLUDES}
	)

## -----------------------------------------------------------------------------
## Check for the library

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

## -----------------------------------------------------------------------------
## Actions taken when all components have been found

if (MQTT_INCLUDES AND MQTT_LIBRARIES)
  set (HAVE_MQTT TRUE)
else (MQTT_INCLUDES AND MQTT_LIBRARIES)
  if (NOT MQTT_FIND_QUIETLY)
    if (NOT MQTT_INCLUDES)
      message (STATUS "Unable to find MQTT header files!")
    endif (NOT MQTT_INCLUDES)
    if (NOT MQTT_LIBRARIES)
      message (STATUS "Unable to find MQTT library files!")
    endif (NOT MQTT_LIBRARIES)
  endif (NOT MQTT_FIND_QUIETLY)
endif (MQTT_INCLUDES AND MQTT_LIBRARIES)

if (HAVE_MQTT)
  if (NOT MQTT_FIND_QUIETLY)
    message (STATUS "Found components for MQTT")
    message (STATUS "MQTT_INCLUDES .... = ${MQTT_INCLUDES}")
    message (STATUS "MQTT_LIBRARIES ... = ${MQTT_LIBRARIES}")
  endif (NOT MQTT_FIND_QUIETLY)
else (HAVE_MQTT)
  if (MQTT_FIND_REQUIRED)
    message (FATAL_ERROR "Could not find MQTT!")
  endif (MQTT_FIND_REQUIRED)
endif (HAVE_MQTT)

mark_as_advanced (
  HAVE_MQTT
  MQTT_LIBRARIES
  MQTT_INCLUDES
  )
