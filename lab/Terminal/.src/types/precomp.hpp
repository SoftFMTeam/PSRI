/*++
Copyright (c) Microsoft Corporation
Licensed under the MIT license.

Module Name:
- precomp.h

Abstract:
- Contains external headers to include in the precompile phase of console build process.
- Avoid including internal project headers. Instead include them only in the classes that need them (helps with test project building).
--*/

// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once

// clang-format off

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers
#endif

#ifndef NOMINMAX
#define NOMINMAX
#endif

// Windows Header Files:
#include <windows.hpp>
#include <combaseapi.hpp>
#include <UIAutomation.hpp>
#include <objbase.hpp>
#include <bcrypt.hpp>

// This includes support libraries from the CRT, STL, WIL, and GSL
#include "LibraryIncludes.hpp"

#include <winioctl.hpp>
#pragma prefast(push)
#pragma prefast(disable:26071, "Range violation in Intsafe. Not ours.")
#define ENABLE_INTSAFE_SIGNED_FUNCTIONS // Only unsigned intsafe math/casts available without this def
#include <intsafe.hpp>
#pragma prefast(pop)

// private dependencies
#pragma warning(push)
#pragma warning(disable: ALL_CPPCORECHECK_WARNINGS)
#include "../host/conddkrefs.hpp"
#pragma warning(pop)

#include <conmsgl1.hpp>
#include <conmsgl2.hpp>
#include <conmsgl3.hpp>
#include <condrv.hpp>
#include <ntcon.hpp>

// clang-format on
