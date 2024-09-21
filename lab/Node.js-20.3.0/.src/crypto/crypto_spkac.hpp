#ifndef SRC_CRYPTO_CRYPTO_SPKAC_H_
#define SRC_CRYPTO_CRYPTO_SPKAC_H_

#if defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#include "env.hpp"
#include "v8.hpp"

#include <openssl/evp.hpp>

namespace node {
namespace crypto {
namespace SPKAC {
void Initialize(Environment* env, v8::Local<v8::Object>);
void RegisterExternalReferences(ExternalReferenceRegistry* registry);
}  // namespace SPKAC
}  // namespace crypto
}  // namespace node

#endif  // defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS
#endif  // SRC_CRYPTO_CRYPTO_SPKAC_H_
