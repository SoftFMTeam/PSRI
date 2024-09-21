// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

// Windows
#include <nt.hpp>
#include <ntrtl.hpp>
#include <nturtl.hpp>
#include <windows.hpp>
#include <sddl.hpp>

// WRL
#include <wrl.hpp>

// WEX
#include <WexTestClass.hpp>
#define LOG_OUTPUT(fmt, ...) WEX::Logging::Log::Comment(WEX::Common::String().Format(fmt, __VA_ARGS__))

// wil
#include <wil/result.hpp>
#include <wil/tokenhelpers.hpp>

// STL
#include <thread>
#include <fstream>
#include <memory>
#include <cstring>

// AppModel TestHelper
#include <AppModelTestHelper.hpp>
