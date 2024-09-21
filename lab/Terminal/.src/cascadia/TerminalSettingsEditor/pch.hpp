// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
//
// pch.h
// Header for platform projection include files
//

#pragma once

#define WIN32_LEAN_AND_MEAN

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

#include <winrt/Windows.ApplicationModel.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>
#include <winrt/Windows.Globalization.hpp>
#include <winrt/Windows.Globalization.NumberFormatting.hpp>
#include <winrt/Windows.System.hpp>
#include <winrt/Windows.UI.hpp>
#include <winrt/Windows.UI.Core.hpp>
#include <winrt/Windows.UI.Input.hpp>
#include <winrt/Windows.UI.Popups.hpp>
#include <winrt/Windows.UI.Text.hpp>
#include <winrt/Windows.UI.Xaml.hpp>
#include <winrt/Windows.UI.Xaml.Automation.hpp>
#include <winrt/Windows.UI.Xaml.Automation.Peers.hpp>
#include <winrt/Windows.UI.Xaml.Controls.hpp>
#include <winrt/Windows.UI.Xaml.Controls.Primitives.hpp>
#include <winrt/Windows.UI.Xaml.Data.hpp>
#include <winrt/Windows.UI.Xaml.Input.hpp>
#include <winrt/Windows.UI.Xaml.Interop.hpp>
#include <winrt/Windows.UI.Xaml.Markup.hpp>
#include <winrt/Windows.UI.Xaml.Media.hpp>
#include <winrt/Windows.UI.Xaml.Navigation.hpp>

#include <winrt/Microsoft.UI.Xaml.Controls.hpp>
#include <winrt/Microsoft.UI.Xaml.XamlTypeInfo.hpp>

#include <winrt/Microsoft.Terminal.Core.hpp>
#include <winrt/Microsoft.Terminal.Control.hpp>
#include <winrt/Microsoft.Terminal.Settings.Model.hpp>

#include <shlobj.hpp>
#include <shobjidl_core.hpp>
#include <dwrite_3.hpp>

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#include "til.hpp"

#include <cppwinrt_utils.hpp>
