// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from turtlesim_msgs:srv/Spawn.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "turtlesim_msgs/srv/detail/spawn__functions.h"
#include "turtlesim_msgs/srv/detail/spawn__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace turtlesim_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _Spawn_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Spawn_Request_type_support_ids_t;

static const _Spawn_Request_type_support_ids_t _Spawn_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Spawn_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Spawn_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Spawn_Request_type_support_symbol_names_t _Spawn_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, turtlesim_msgs, srv, Spawn_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, turtlesim_msgs, srv, Spawn_Request)),
  }
};

typedef struct _Spawn_Request_type_support_data_t
{
  void * data[2];
} _Spawn_Request_type_support_data_t;

static _Spawn_Request_type_support_data_t _Spawn_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Spawn_Request_message_typesupport_map = {
  2,
  "turtlesim_msgs",
  &_Spawn_Request_message_typesupport_ids.typesupport_identifier[0],
  &_Spawn_Request_message_typesupport_symbol_names.symbol_name[0],
  &_Spawn_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Spawn_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Spawn_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &turtlesim_msgs__srv__Spawn_Request__get_type_hash,
  &turtlesim_msgs__srv__Spawn_Request__get_type_description,
  &turtlesim_msgs__srv__Spawn_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace turtlesim_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<turtlesim_msgs::srv::Spawn_Request>()
{
  return &::turtlesim_msgs::srv::rosidl_typesupport_cpp::Spawn_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, turtlesim_msgs, srv, Spawn_Request)() {
  return get_message_type_support_handle<turtlesim_msgs::srv::Spawn_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "turtlesim_msgs/srv/detail/spawn__functions.h"
// already included above
// #include "turtlesim_msgs/srv/detail/spawn__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace turtlesim_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _Spawn_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Spawn_Response_type_support_ids_t;

static const _Spawn_Response_type_support_ids_t _Spawn_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Spawn_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Spawn_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Spawn_Response_type_support_symbol_names_t _Spawn_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, turtlesim_msgs, srv, Spawn_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, turtlesim_msgs, srv, Spawn_Response)),
  }
};

typedef struct _Spawn_Response_type_support_data_t
{
  void * data[2];
} _Spawn_Response_type_support_data_t;

static _Spawn_Response_type_support_data_t _Spawn_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Spawn_Response_message_typesupport_map = {
  2,
  "turtlesim_msgs",
  &_Spawn_Response_message_typesupport_ids.typesupport_identifier[0],
  &_Spawn_Response_message_typesupport_symbol_names.symbol_name[0],
  &_Spawn_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Spawn_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Spawn_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &turtlesim_msgs__srv__Spawn_Response__get_type_hash,
  &turtlesim_msgs__srv__Spawn_Response__get_type_description,
  &turtlesim_msgs__srv__Spawn_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace turtlesim_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<turtlesim_msgs::srv::Spawn_Response>()
{
  return &::turtlesim_msgs::srv::rosidl_typesupport_cpp::Spawn_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, turtlesim_msgs, srv, Spawn_Response)() {
  return get_message_type_support_handle<turtlesim_msgs::srv::Spawn_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "turtlesim_msgs/srv/detail/spawn__functions.h"
// already included above
// #include "turtlesim_msgs/srv/detail/spawn__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace turtlesim_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _Spawn_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Spawn_Event_type_support_ids_t;

static const _Spawn_Event_type_support_ids_t _Spawn_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Spawn_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Spawn_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Spawn_Event_type_support_symbol_names_t _Spawn_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, turtlesim_msgs, srv, Spawn_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, turtlesim_msgs, srv, Spawn_Event)),
  }
};

typedef struct _Spawn_Event_type_support_data_t
{
  void * data[2];
} _Spawn_Event_type_support_data_t;

static _Spawn_Event_type_support_data_t _Spawn_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Spawn_Event_message_typesupport_map = {
  2,
  "turtlesim_msgs",
  &_Spawn_Event_message_typesupport_ids.typesupport_identifier[0],
  &_Spawn_Event_message_typesupport_symbol_names.symbol_name[0],
  &_Spawn_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Spawn_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Spawn_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &turtlesim_msgs__srv__Spawn_Event__get_type_hash,
  &turtlesim_msgs__srv__Spawn_Event__get_type_description,
  &turtlesim_msgs__srv__Spawn_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace turtlesim_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<turtlesim_msgs::srv::Spawn_Event>()
{
  return &::turtlesim_msgs::srv::rosidl_typesupport_cpp::Spawn_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, turtlesim_msgs, srv, Spawn_Event)() {
  return get_message_type_support_handle<turtlesim_msgs::srv::Spawn_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "turtlesim_msgs/srv/detail/spawn__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace turtlesim_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _Spawn_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Spawn_type_support_ids_t;

static const _Spawn_type_support_ids_t _Spawn_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Spawn_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Spawn_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Spawn_type_support_symbol_names_t _Spawn_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, turtlesim_msgs, srv, Spawn)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, turtlesim_msgs, srv, Spawn)),
  }
};

typedef struct _Spawn_type_support_data_t
{
  void * data[2];
} _Spawn_type_support_data_t;

static _Spawn_type_support_data_t _Spawn_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Spawn_service_typesupport_map = {
  2,
  "turtlesim_msgs",
  &_Spawn_service_typesupport_ids.typesupport_identifier[0],
  &_Spawn_service_typesupport_symbol_names.symbol_name[0],
  &_Spawn_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t Spawn_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Spawn_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<turtlesim_msgs::srv::Spawn_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<turtlesim_msgs::srv::Spawn_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<turtlesim_msgs::srv::Spawn_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<turtlesim_msgs::srv::Spawn>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<turtlesim_msgs::srv::Spawn>,
  &turtlesim_msgs__srv__Spawn__get_type_hash,
  &turtlesim_msgs__srv__Spawn__get_type_description,
  &turtlesim_msgs__srv__Spawn__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace turtlesim_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<turtlesim_msgs::srv::Spawn>()
{
  return &::turtlesim_msgs::srv::rosidl_typesupport_cpp::Spawn_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, turtlesim_msgs, srv, Spawn)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<turtlesim_msgs::srv::Spawn>();
}

#ifdef __cplusplus
}
#endif
