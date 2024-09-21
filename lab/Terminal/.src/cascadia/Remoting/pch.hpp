// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
//
// pch.h
// Header for platform projection include files
//

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
#include <LibraryIncludes.hpp>
// This is inexplicable, but for whatever reason, cppwinrt conflicts with the
//      SDK definition of this function, so the only fix is to undef it.
// from WinBase.h
// Windows::UI::Xaml::Media::Animation::IStoryboard::GetCurrentTime
#ifdef GetCurrentTime
#undef GetCurrentTime
#endif

#include <wil/cppwinrt.hpp>

#include <hstring.hpp>

#include <winrt/Windows.ApplicationModel.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>

#include <winrt/Windows.System.hpp>

// Including TraceLogging essentials for the binary
#include <TraceLoggingProvider.hpp>
#include <winmeta.hpp>
TRACELOGGING_DECLARE_PROVIDER(g_hRemotingProvider);
#include <telemetry/ProjectTelemetry.hpp>
#include <TraceLoggingActivity.hpp>

#include <shellapi.hpp>

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#include "til.hpp"

#include <cppwinrt_utils.hpp>
#include <til/winrt.hpp>
