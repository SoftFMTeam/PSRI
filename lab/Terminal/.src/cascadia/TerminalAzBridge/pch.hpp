/*++
Copyright (c) Microsoft Corporation
Licensed under the MIT license.

Module Name:
- pch.h

Abstract:
- Contains external headers to include in the precompile phase of console build process.
- Avoid including internal project headers. Instead include them only in the classes that need them (helps with test project building).
--*/

#pragma once

// Ignore checked iterators warning from VC compiler.
#define _SCL_SECURE_NO_WARNINGS

// Block minwindef.h min/max macros to prevent <algorithm> conflict
#define NOMINMAX

#define WIN32_LEAN_AND_MEAN
#define NOMCX
#define NOHELP
#define NOCOMM
#include <unknwn.hpp>

#include <windows.hpp>

#include "../inc/LibraryIncludes.hpp"

#include <wil/cppwinrt.hpp>

#include <winrt/Windows.system.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>

#include <wil/resource.hpp>
#include <wil/win32_helpers.hpp>

#include <cppwinrt_utils.hpp>
