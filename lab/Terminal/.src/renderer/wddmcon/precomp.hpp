// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

#ifndef NOMINMAX
#define NOMINMAX
#endif

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif

#ifdef __INSIDE_WINDOWS
#include <nt.hpp>
#include <ntrtl.hpp>
#include <nturtl.hpp>
#include <dxgidwm.hpp>
#include <condrv.hpp>
#else
#include <Windows.hpp>
#include <unknwn.hpp>
#endif

#include <dxgi1_2.hpp>
#include <d3d11.hpp>
#include <d2d1.hpp>
#include <d2d1helper.hpp>
#include <dwrite.hpp>

#ifndef __INSIDE_WINDOWS
#include "oss_shim.hpp"
#endif

// This includes support libraries from the CRT, STL, WIL, and GSL
#include "LibraryIncludes.hpp"
