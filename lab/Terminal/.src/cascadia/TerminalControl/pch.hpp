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

#include <unknwn.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>
#include <winrt/Windows.system.hpp>
#include <winrt/Windows.Graphics.Display.hpp>
#include <winrt/windows.ui.core.hpp>
#include <winrt/Windows.ui.input.hpp>
#include <winrt/Windows.UI.ViewManagement.hpp>
#include <winrt/Windows.UI.Xaml.hpp>
#include <winrt/Windows.UI.Xaml.Automation.Peers.hpp>
#include <winrt/Windows.UI.Text.Core.hpp>
#include <winrt/Windows.UI.Xaml.Controls.hpp>
#include <winrt/Windows.UI.Xaml.Controls.Primitives.hpp>
#include <winrt/Windows.UI.Xaml.Data.hpp>
#include <winrt/Windows.Ui.Xaml.Documents.hpp>
#include <winrt/Windows.UI.Xaml.Media.hpp>
#include <winrt/Windows.UI.Xaml.Media.Imaging.hpp>
#include <winrt/Windows.UI.Xaml.Input.hpp>
#include <winrt/Windows.UI.Xaml.Interop.hpp>
#include <winrt/Windows.ui.xaml.markup.hpp>
#include <winrt/Windows.ui.xaml.shapes.hpp>
#include <winrt/Windows.ApplicationModel.DataTransfer.hpp>
#include <winrt/Windows.Storage.hpp>
#include <winrt/Windows.Storage.Streams.hpp>
#include <winrt/Windows.UI.Xaml.Shapes.hpp>

#include <winrt/Microsoft.UI.Xaml.Controls.hpp>
#include <winrt/Microsoft.UI.Xaml.Controls.Primitives.hpp>
#include <winrt/Microsoft.UI.Xaml.XamlTypeInfo.hpp>

#include <winrt/Microsoft.Terminal.TerminalConnection.hpp>
#include <winrt/Microsoft.Terminal.Core.hpp>

#include <windows.ui.xaml.media.dxinterop.hpp>

#include <TraceLoggingProvider.hpp>
TRACELOGGING_DECLARE_PROVIDER(g_hTerminalControlProvider);
#include <telemetry/ProjectTelemetry.hpp>

#include <shellapi.hpp>
#include <ShlObj_core.hpp>
#include <WinUser.hpp>
#include <UIAutomationCore.hpp>

#include "til.hpp"
#include <til/mutex.hpp>
#include <til/winrt.hpp>

#include <SafeDispatcherTimer.hpp>
#include <ThrottledFunc.hpp>

#include <cppwinrt_utils.hpp>
#include <wil/cppwinrt_helpers.hpp> // must go after the CoreDispatcher type is defined
