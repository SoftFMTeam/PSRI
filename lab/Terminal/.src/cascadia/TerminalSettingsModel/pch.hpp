// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
//
// pch.h
// Header for platform projection include files
//

#pragma once

#define WIN32_LEAN_AND_MEAN
#define NOMCX
#define NOHELP
#define NOCOMM

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#define BLOCK_TIL
#include <LibraryIncludes.hpp>
// This is inexplicable, but for whatever reason, cppwinrt conflicts with the
//      SDK definition of this function, so the only fix is to undef it.
// from WinBase.h
// Windows::UI::Xaml::Media::Animation::IStoryboard::GetCurrentTime
#ifdef GetCurrentTime
#undef GetCurrentTime
#endif

#include <wil/cppwinrt.hpp>

#include <winrt/Windows.ApplicationModel.AppExtensions.hpp>
#include <winrt/Windows.ApplicationModel.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Graphics.Imaging.hpp>
#include <Windows.Graphics.Imaging.Interop.hpp>
#include <winrt/Windows.Storage.hpp>
#include <winrt/Windows.Storage.Streams.hpp>
#include <winrt/Windows.System.hpp>
#include <winrt/Windows.UI.Core.hpp>
#include <winrt/Windows.UI.ViewManagement.hpp>
#include <winrt/Windows.UI.Xaml.Controls.hpp>
#include <winrt/Windows.UI.Xaml.Media.hpp>
#include <winrt/Windows.UI.Xaml.Media.Imaging.hpp>

#include <winrt/Microsoft.UI.Xaml.Controls.hpp>

#include <winrt/Microsoft.Terminal.Core.hpp>
#include <winrt/Microsoft.Terminal.Control.hpp>
#include <winrt/Microsoft.Terminal.TerminalConnection.hpp>

// Including TraceLogging essentials for the binary
#include <TraceLoggingProvider.hpp>
#include <winmeta.hpp>
TRACELOGGING_DECLARE_PROVIDER(g_hSettingsModelProvider);
#include <telemetry/ProjectTelemetry.hpp>
#include <TraceLoggingActivity.hpp>

// JsonCpp
#include <json.hpp>

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#include "til.hpp"
#include <til/winrt.hpp>

#include <til/mutex.hpp>
#include <til/throttled_func.hpp>

#include <cppwinrt_utils.hpp>
#include <wil/cppwinrt_helpers.hpp> // must go after the CoreDispatcher type is defined
