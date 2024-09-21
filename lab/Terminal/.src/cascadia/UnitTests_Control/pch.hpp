/*++
Copyright (c) Microsoft Corporation
Licensed under the MIT license.
--*/

#pragma once

// Block minwindef.h min/max macros to prevent <algorithm> conflict
#define NOMINMAX

#define WIN32_LEAN_AND_MEAN
#define NOMCX
#define NOHELP
#define NOCOMM

#include <unknwn.hpp>
#include <ShObjIdl.hpp>

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#define BLOCK_TIL
// This includes support libraries from the CRT, STL, WIL, and GSL
#include "LibraryIncludes.hpp"
// This is inexplicable, but for whatever reason, cppwinrt conflicts with the
//      SDK definition of this function, so the only fix is to undef it.
// from WinBase.h
// Windows::UI::Xaml::Media::Animation::IStoryboard::GetCurrentTime
#ifdef GetCurrentTime
#undef GetCurrentTime
#endif

#include <wil/cppwinrt.hpp>
#include <unknwn.hpp>
#include <hstring.hpp>

#include <WexTestClass.hpp>
#include "consoletaeftemplates.hpp"

#include <winrt/Windows.ApplicationModel.Resources.Core.hpp>
#include <winrt/Windows.system.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>

#include <winrt/Microsoft.Terminal.Core.hpp>
#include <winrt/Microsoft.Terminal.Control.hpp>
#include <winrt/Microsoft.Terminal.TerminalConnection.hpp>

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#include "til.hpp"
#include <til/mutex.hpp>
#include <til/winrt.hpp>

#include "ThrottledFunc.hpp"

// Common includes for most tests:
#include "../../inc/conattrs.hpp"
#include "../../types/inc/utils.hpp"
#include "../../inc/DefaultSettings.hpp"

#include <cppwinrt_utils.hpp>
