// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
//
// pch.h
// Header for platform projection include files
//

#pragma once

// Needs to be defined or we get redeclaration errors
#define WIN32_LEAN_AND_MEAN
#define NOMCX
#define NOHELP
#define NOCOMM

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#define BLOCK_TIL
#include <LibraryIncludes.hpp>

// Must be included before any WinRT headers.
#include <unknwn.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <wil/cppwinrt.hpp>

#include "winrt/Windows.Security.Credentials.hpp"
#include "winrt/Windows.Foundation.Collections.hpp"
#include "winrt/Windows.Web.Http.hpp"
#include "winrt/Windows.Web.Http.Headers.hpp"
#include "winrt/Windows.Data.Json.hpp"
#include <Windows.hpp>

#include <winhttp.hpp>
#include <wil/resource.hpp>

#include <TraceLoggingProvider.hpp>
TRACELOGGING_DECLARE_PROVIDER(g_hTerminalConnectionProvider);
#include <telemetry/ProjectTelemetry.hpp>

#include "til.hpp"

#include <cppwinrt_utils.hpp>
