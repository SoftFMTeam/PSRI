/*++
Copyright (c) Microsoft Corporation
Licensed under the MIT license.

Module Name:
- precomp.h

Abstract:
- Contains external headers to include in the precompile phase of console build process.
- Avoid including internal project headers. Instead include them only in the classes that need them (helps with test project building).

Author(s):
- Carlos Zamora (cazamor) April 2019
--*/

#pragma once

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
#include <json.hpp>
#include "consoletaeftemplates.hpp"
#include "winrtTaefTemplates.hpp"

#include <winrt/Windows.ApplicationModel.Resources.Core.hpp>
#include "winrt/Windows.UI.Xaml.Markup.hpp"
#include <winrt/Windows.system.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>
#include <winrt/windows.ui.core.hpp>
#include <winrt/Windows.ui.input.hpp>
#include <winrt/Windows.UI.Xaml.Controls.hpp>
#include <winrt/Windows.UI.Xaml.Controls.Primitives.hpp>
#include <winrt/Windows.UI.Xaml.Data.hpp>
#include <winrt/Windows.ui.xaml.media.hpp>
#include <winrt/Windows.ui.xaml.input.hpp>
#include <winrt/Windows.UI.Xaml.Markup.hpp>
#include <winrt/Windows.UI.Xaml.Documents.hpp>

#include <windows.ui.xaml.media.dxinterop.hpp>

#include <winrt/windows.applicationmodel.core.hpp>

#include <winrt/Microsoft.Terminal.TerminalConnection.hpp>
#include <winrt/Microsoft.Terminal.Settings.Model.hpp>

#include <winrt/Microsoft.UI.Xaml.Controls.hpp>

#include <regex>
#include <CLI11/CLI11.hpp>

#include <shobjidl_core.hpp>

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#include "til.hpp"

#include <SafeDispatcherTimer.hpp>

// Common includes for most tests:
#include "../../inc/conattrs.hpp"
#include "../../types/inc/utils.hpp"
#include "../../inc/DefaultSettings.hpp"

#include <cppwinrt_utils.hpp>

#include <til/winrt.hpp>
