// Copyright Joyent, Inc. and other Node contributors.
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to permit
// persons to whom the Software is furnished to do so, subject to the
// following conditions:
//
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
// NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
// USE OR OTHER DEALINGS IN THE SOFTWARE.

#ifndef SRC_NODE_CRYPTO_H_
#define SRC_NODE_CRYPTO_H_

#if defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

// All of the crypto definitions previously contained in this header
// have been split across multiple headers in src/crypto. This header
// remains for convenience for any code that still imports it. New
// code should include the relevant src/crypto headers directly.
#include "crypto/crypto_aes.hpp"
#include "crypto/crypto_bio.hpp"
#include "crypto/crypto_cipher.hpp"
#include "crypto/crypto_context.hpp"
#include "crypto/crypto_dh.hpp"
#include "crypto/crypto_dsa.hpp"
#include "crypto/crypto_ec.hpp"
#include "crypto/crypto_hash.hpp"
#include "crypto/crypto_hkdf.hpp"
#include "crypto/crypto_hmac.hpp"
#include "crypto/crypto_keygen.hpp"
#include "crypto/crypto_keys.hpp"
#include "crypto/crypto_pbkdf2.hpp"
#include "crypto/crypto_random.hpp"
#include "crypto/crypto_rsa.hpp"
#include "crypto/crypto_scrypt.hpp"
#include "crypto/crypto_sig.hpp"
#include "crypto/crypto_spkac.hpp"
#include "crypto/crypto_timing.hpp"
#include "crypto/crypto_tls.hpp"
#include "crypto/crypto_util.hpp"
#include "crypto/crypto_x509.hpp"

#endif  // defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#endif  // SRC_NODE_CRYPTO_H_
