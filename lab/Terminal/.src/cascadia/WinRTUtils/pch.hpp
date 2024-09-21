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

#include <hstring.hpp>

#include <winrt/Windows.ApplicationModel.Resources.Core.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>
#include <winrt/Windows.System.hpp>

#include <shlobj.hpp>
#include <shobjidl_core.hpp>

#include <cppwinrt_utils.hpp>
