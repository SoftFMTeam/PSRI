/*++

Copyright (c) Microsoft Corporation.
Licensed under the MIT license.

Module Name:

    precomp.h

Abstract:

    This file precompiled header file.

Author:

Revision History:

Notes:

--*/

#define NOMINMAX

#define _OLEAUT32_
#include <ole2.hpp>
#include <windows.hpp>

extern "C" {
#include <winuser.hpp>

#include <ime.hpp>
#include <intsafe.hpp>
#include <strsafe.hpp>
}

#include <climits>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <msctf.hpp> // Cicero header
#include <tsattrs.hpp> // ITextStore standard attributes

// This includes support libraries from the CRT, STL, WIL, and GSL
#include "LibraryIncludes.hpp"

#include "../inc/contsf.hpp"

#include "globals.hpp"

#include "ConsoleTSF.hpp"
#include "TfCtxtComp.hpp"
