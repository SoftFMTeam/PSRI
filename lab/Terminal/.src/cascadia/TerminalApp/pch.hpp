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

#include <winrt/Windows.ApplicationModel.hpp>
#include <winrt/Windows.ApplicationModel.DataTransfer.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>
#include <winrt/Windows.Foundation.Metadata.hpp>
#include <winrt/Windows.Globalization.hpp>
#include <winrt/Windows.Graphics.Display.hpp>
#include <winrt/Windows.System.hpp>
#include <winrt/Windows.UI.Core.hpp>
#include <winrt/Windows.UI.Input.hpp>
#include <winrt/Windows.UI.Text.hpp>
#include <winrt/Windows.UI.ViewManagement.hpp>
#include <winrt/Windows.UI.Xaml.Automation.Peers.hpp>
#include <winrt/Windows.UI.Xaml.Controls.hpp>
#include <winrt/Windows.UI.Xaml.Controls.Primitives.hpp>
#include <winrt/Windows.UI.Xaml.Documents.hpp>
#include <winrt/Windows.UI.Xaml.Input.hpp>
#include <winrt/Windows.UI.Xaml.Markup.hpp>
#include <winrt/Windows.UI.Xaml.Media.hpp>
#include <winrt/Windows.UI.Xaml.Media.Imaging.hpp>
#include <winrt/Windows.UI.Xaml.Media.Animation.hpp>
#include <winrt/Windows.Media.hpp>
#include <winrt/Windows.Media.Core.hpp>
#include <winrt/Windows.Media.Playback.hpp>
#include <winrt/Windows.Management.Deployment.hpp>

#include <winrt/Microsoft.UI.Xaml.Controls.hpp>
#include <winrt/Microsoft.UI.Xaml.Controls.Primitives.hpp>
#include <winrt/Microsoft.UI.Xaml.XamlTypeInfo.hpp>

#include <winrt/Microsoft.Terminal.Core.hpp>
#include <winrt/Microsoft.Terminal.Control.hpp>
#include <winrt/Microsoft.Terminal.TerminalConnection.hpp>
#include <winrt/Microsoft.Terminal.Settings.Editor.hpp>
#include <winrt/Microsoft.Terminal.Settings.Model.hpp>
#include <winrt/Windows.Services.Store.hpp>
#include <winrt/Windows.Storage.hpp>
#include <winrt/Windows.Storage.Provider.hpp>
#include <winrt/Windows.Storage.Pickers.hpp>

#include <windows.ui.xaml.media.dxinterop.hpp>

// Including TraceLogging essentials for the binary
#include <TraceLoggingProvider.hpp>
#include <winmeta.hpp>
TRACELOGGING_DECLARE_PROVIDER(g_hTerminalAppProvider);
#include <telemetry/ProjectTelemetry.hpp>
#include <TraceLoggingActivity.hpp>

#include <msctf.hpp>
#include <shellapi.hpp>
#include <shobjidl_core.hpp>

#include <CLI11/CLI11.hpp>

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#include "til.hpp"

#include <SafeDispatcherTimer.hpp>

#include <cppwinrt_utils.hpp>
#include <wil/cppwinrt_helpers.hpp> // must go after the CoreDispatcher type is defined

#include <til/winrt.hpp>
