// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

#define NOMINMAX

#include "windows.hpp"
#include "wincon.hpp"
#include "windowsx.hpp"

#include "WexTestClass.hpp"

// This includes support libraries from the CRT, STL, WIL, and GSL
#include "LibraryIncludes.hpp"

#include <conio.hpp>

// Extension API set presence checks.
#ifdef __INSIDE_WINDOWS
#include <messageext.hpp>
#include <windowext.hpp>
#include <sysparamsext.hpp>
#endif

#define CM_SET_KEY_STATE (WM_USER + 18)
#define CM_SET_KEYBOARD_LAYOUT (WM_USER + 19)

#include "OneCoreDelay.hpp"

// Include our common helpers
#include "common.hpp"

#include "resource.hpp"
