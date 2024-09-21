#ifndef SRC_NODE_PROCESS_INL_H_
#define SRC_NODE_PROCESS_INL_H_

#if defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#include "node_process.hpp"
#include "v8.hpp"
#include "debug_utils-inl.hpp"

namespace node {

// Call process.emitWarning(str), fmt is a snprintf() format string
template <typename... Args>
inline v8::Maybe<bool> ProcessEmitWarning(Environment* env,
                                          const char* fmt,
                                          Args&&... args) {
  std::string warning = SPrintF(fmt, std::forward<Args>(args)...);

  return ProcessEmitWarningGeneric(env, warning.c_str());
}

}  // namespace node

#endif  // defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#endif  // SRC_NODE_PROCESS_INL_H_
