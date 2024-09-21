#include "connect_wrap.hpp"
#include "req_wrap-inl.hpp"

namespace node {

using v8::Local;
using v8::Object;

class Environment;

ConnectWrap::ConnectWrap(Environment* env,
    Local<Object> req_wrap_obj,
    AsyncWrap::ProviderType provider) : ReqWrap(env, req_wrap_obj, provider) {
}

}  // namespace node
