// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

#ifdef __INSIDE_WINDOWS

#define NOMINMAX

#include <nt.hpp>
#include <ntrtl.hpp>
#include <nturtl.hpp>
#define WIN32_NO_STATUS
#include <windows.hpp>
#undef WIN32_NO_STATUS
#include "wchar.hpp"

// Extension presence detection
#include <sysparamsext.hpp>

#define _DDK_INCLUDED
#define NO_WINTERNL_INBOX_BUILD
#include "../../host/precomp.hpp"

#else

#include "../../host/precomp.hpp"

#endif
