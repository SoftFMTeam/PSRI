#if HAVE_OPENSSL && NODE_OPENSSL_HAS_QUIC

#include "preferredaddress.hpp"
#include <env-inl.hpp>
#include <ngtcp2/ngtcp2.hpp>
#include <node_errors.hpp>
#include <node_sockaddr-inl.hpp>
#include <util-inl.hpp>
#include <uv.hpp>
#include <v8.hpp>

namespace node {

using v8::Just;
using v8::Local;
using v8::Maybe;
using v8::Nothing;
using v8::Value;

namespace quic {

namespace {
template <int FAMILY>
std::optional<const PreferredAddress::AddressInfo> get_address_info(
    const ngtcp2_preferred_addr& paddr) {
  if constexpr (FAMILY == AF_INET) {
    if (!paddr.ipv4_present) return std::nullopt;
    PreferredAddress::AddressInfo address;
    address.family = FAMILY;
    address.port = paddr.ipv4_port;
    if (uv_inet_ntop(
            FAMILY, paddr.ipv4_addr, address.host, sizeof(address.host)) == 0) {
      address.address = address.host;
    }
    return address;
  } else {
    if (!paddr.ipv6_present) return std::nullopt;
    PreferredAddress::AddressInfo address;
    address.family = FAMILY;
    address.port = paddr.ipv6_port;
    if (uv_inet_ntop(
            FAMILY, paddr.ipv6_addr, address.host, sizeof(address.host)) == 0) {
      address.address = address.host;
    }
    return address;
  }
}

template <int FAMILY>
void copy_to_transport_params(ngtcp2_transport_params* params,
                              const sockaddr* addr) {
  params->preferred_address_present = true;
  if constexpr (FAMILY == AF_INET) {
    const sockaddr_in* src = reinterpret_cast<const sockaddr_in*>(addr);
    params->preferred_address.ipv4_port = SocketAddress::GetPort(addr);
    memcpy(params->preferred_address.ipv4_addr,
           &src->sin_addr,
           sizeof(params->preferred_address.ipv4_addr));
  } else {
    DCHECK_EQ(FAMILY, AF_INET6);
    const sockaddr_in6* src = reinterpret_cast<const sockaddr_in6*>(addr);
    params->preferred_address.ipv6_port = SocketAddress::GetPort(addr);
    memcpy(params->preferred_address.ipv6_addr,
           &src->sin6_addr,
           sizeof(params->preferred_address.ipv4_addr));
  }
  UNREACHABLE();
}

bool resolve(const PreferredAddress::AddressInfo& address,
             uv_getaddrinfo_t* req) {
  addrinfo hints{};
  hints.ai_flags = AI_NUMERICHOST | AI_NUMERICSERV;
  hints.ai_family = address.family;
  hints.ai_socktype = SOCK_DGRAM;

  // ngtcp2 requires the selection of the preferred address
  // to be synchronous, which means we have to do a sync resolve
  // using uv_getaddrinfo here.
  return uv_getaddrinfo(nullptr,
                        req,
                        nullptr,
                        address.host,
                        // TODO(@jasnell): The to_string here is not really
                        // the most performant way of converting the uint16_t
                        // port into a string. Depending on execution count,
                        // the potential cost here could be mitigated with a
                        // more efficient conversion. For now, however, this
                        // works.
                        std::to_string(address.port).c_str(),
                        &hints) == 0 &&
         req->addrinfo != nullptr;
}
}  // namespace

Maybe<PreferredAddress::Policy> PreferredAddress::GetPolicy(
    Environment* env, Local<Value> value) {
  CHECK(value->IsUint32());
  uint32_t val = 0;
  if (value->Uint32Value(env->context()).To(&val)) {
    switch (val) {
      case QUIC_PREFERRED_ADDRESS_USE:
        return Just(Policy::USE_PREFERRED_ADDRESS);
      case QUIC_PREFERRED_ADDRESS_IGNORE:
        return Just(Policy::IGNORE_PREFERRED_ADDRESS);
    }
  }
  THROW_ERR_INVALID_ARG_VALUE(
      env, "%d is not a valid preferred address policy", val);
  return Nothing<Policy>();
}

PreferredAddress::PreferredAddress(ngtcp2_path* dest,
                                   const ngtcp2_preferred_addr* paddr)
    : dest_(dest), paddr_(paddr) {
  DCHECK_NOT_NULL(paddr);
  DCHECK_NOT_NULL(dest);
}

std::optional<const PreferredAddress::AddressInfo> PreferredAddress::ipv4()
    const {
  return get_address_info<AF_INET>(*paddr_);
}

std::optional<const PreferredAddress::AddressInfo> PreferredAddress::ipv6()
    const {
  return get_address_info<AF_INET6>(*paddr_);
}

void PreferredAddress::Use(const AddressInfo& address) {
  uv_getaddrinfo_t req;
  auto on_exit = OnScopeLeave([&] {
    if (req.addrinfo != nullptr) uv_freeaddrinfo(req.addrinfo);
  });

  if (resolve(address, &req)) {
    DCHECK_NOT_NULL(req.addrinfo);
    dest_->remote.addrlen = req.addrinfo->ai_addrlen;
    memcpy(dest_->remote.addr, req.addrinfo->ai_addr, req.addrinfo->ai_addrlen);
  }
}

void PreferredAddress::Set(ngtcp2_transport_params* params,
                           const sockaddr* addr) {
  DCHECK_NOT_NULL(params);
  DCHECK_NOT_NULL(addr);
  switch (addr->sa_family) {
    case AF_INET:
      return copy_to_transport_params<AF_INET>(params, addr);
    case AF_INET6:
      return copy_to_transport_params<AF_INET6>(params, addr);
  }
  // Any other value is just ignored.
}

}  // namespace quic
}  // namespace node

#endif  // HAVE_OPENSSL && NODE_OPENSSL_HAS_QUIC
