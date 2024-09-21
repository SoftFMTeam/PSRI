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
#include <UIAutomation.hpp>
#include <cstdlib>
#include <cstring>
#include <shellscalingapi.hpp>
#include <windowsx.hpp>
#include <ShObjIdl.hpp>

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#define BLOCK_TIL
#include "../inc/LibraryIncludes.hpp"

// This is inexplicable, but for whatever reason, cppwinrt conflicts with the
//      SDK definition of this function, so the only fix is to undef it.
// from WinBase.h
// Windows::UI::Xaml::Media::Animation::IStoryboard::GetCurrentTime
#ifdef GetCurrentTime
#undef GetCurrentTime
#endif

#include <wil/cppwinrt.hpp>

// Needed just for XamlIslands to work at all:
#include <winrt/Windows.System.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>
#include <winrt/Windows.UI.Xaml.Hosting.hpp>
#include <windows.ui.xaml.hpposting.desktopwindowxamlsource.hpp>

// Additional headers for various xaml features. We need:
//  * Core so we can resume_foreground with CoreDispatcher
//  * Controls for grid
//  * Media for ScaleTransform
//  * ApplicationModel for finding the path to wt.exe
//  * Primitives for Popup (used by GetOpenPopupsForXamlRoot)
#include <winrt/Windows.UI.Core.hpp>
#include <winrt/Windows.UI.Xaml.Controls.hpp>
#include <winrt/Windows.UI.Xaml.Controls.Primitives.hpp>
#include <winrt/Windows.UI.Xaml.Data.hpp>
#include <winrt/Windows.UI.Xaml.Media.hpp>
#include <winrt/Windows.ApplicationModel.hpp>
#include <winrt/Windows.ApplicationModel.Resources.Core.hpp>
#include <winrt/Windows.UI.Composition.hpp>

#include <winrt/TerminalApp.hpp>
#include <winrt/Microsoft.Terminal.Settings.Model.hpp>
#include <winrt/Microsoft.Terminal.Remoting.hpp>
#include <winrt/Microsoft.Terminal.Control.hpp>

#include <wil/resource.hpp>
#include <wil/win32_helpers.hpp>

// Including TraceLogging essentials for the binary
#include <TraceLoggingProvider.hpp>
#include <winmeta.hpp>
TRACELOGGING_DECLARE_PROVIDER(g_hWindowsTerminalProvider);
#include <telemetry/ProjectTelemetry.hpp>
#include <TraceLoggingActivity.hpp>

// For commandline argument processing
#include <shellapi.hpp>
#include <processenv.hpp>
#include <WinUser.hpp>

#include "til.hpp"
#include "til/mutex.hpp"

#include <SafeDispatcherTimer.hpp>

#include <cppwinrt_utils.hpp>
#include <wil/cppwinrt_helpers.hpp> // must go after the CoreDispatcher type is defined
