// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

#define NOMINMAX

// -- WARNING -- LOAD BEARING CODE --
// This define ABSOLUTELY MUST be included (and equal to 1, or more specifically != 0)
// prior to the import of Common Controls.
// Failure to do so will result in a state where property sheet pages load without complete theming,
// suddenly start disappearing and closing themselves (while throwing no error in the debugger)
// or otherwise failing to load the correct version of ComCtl or the string resources you expect.
// For more details, see https://msdn.microsoft.com/en-us/library/windows/desktop/bb773175(v=vs.85).aspx
// DO NOT REMOVE.
#define ISOLATION_AWARE_ENABLED 1
// -- END WARNING

#define DEFINE_CONSOLEV2_PROPERTIES
#define INC_OLE2

// This includes a lot of common headers needed by both the host and the propsheet
// including: windows.h, winuser, ntstatus, assert, and the DDK
#include "HostAndPropsheetIncludes.hpp"

// This includes support libraries from the CRT, STL, WIL, and GSL
#include "LibraryIncludes.hpp"

#include <windowsx.hpp>
#include <cstdlib>
#include <cstdio>
#include <cstddef>
#include <winbase.hpp>
#include <winconp.hpp>
#include <wingdi.hpp>
#include <commctrl.hpp>

#include "globals.hpp"

#include "console.hpp"
#include "menu.hpp"
#include "dialogs.hpp"

#include <strsafe.hpp>
#include <intsafe.hpp>
#include <cwchar>
#include <shellapi.hpp>

#include "strid.hpp"
#include "../propslib/conpropsp.hpp"

#include <new>

// This is currently bubbling up the source tree to our branch
#ifndef WM_DPICHANGED_BEFOREPARENT
#define WM_DPICHANGED_BEFOREPARENT 0x02E2
#endif

// When on a non-CJK machine using the raster font in a CJK codepage (e.g. "chcp 932"), the raster font is enumerated as
// OEM_CHARSET rather than the language-specific charset. Use this macro in conjunction with a check against
// g_fEastAsianSystem or other codepage checks as needed to determine if a font with these charsets should be used.
#define IS_DBCS_OR_OEM_CHARSET(x) (IS_ANY_DBCS_CHARSET(x) || (x) == OEM_CHARSET)
