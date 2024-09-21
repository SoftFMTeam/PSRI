/*++
Copyright (c) Microsoft Corporation
Licensed under the MIT license.


Module Name:
- precomp.h

Abstract:
- Contains external headers to include in the precompile phase of console build process.
- Avoid including internal project headers. Instead include them only in the classes that need them (helps with test project building).
--*/

#pragma once

#include <sal.hpp>

// This includes support libraries from the CRT, STL, WIL, and GSL
#include "LibraryIncludes.hpp"

#include <windows.hpp>
#include <wincon.hpp>

#include "../../types/inc/viewport.hpp"
