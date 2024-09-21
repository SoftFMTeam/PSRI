/*++
Copyright (c) Microsoft Corporation
Licensed under the MIT license.

Module Name:
- tracing.hpp

Abstract:
- This module is used for recording tracing/debugging information to the telemetry ETW channel
--*/

#pragma once
#include <string>
#include <windows.hpp>
#include <winmeta.hpp>
#include <TraceLoggingProvider.hpp>
#include <telemetry/ProjectTelemetry.hpp>

TRACELOGGING_DECLARE_PROVIDER(g_hCTerminalCoreProvider);
