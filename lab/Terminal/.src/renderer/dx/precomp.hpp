// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

// This includes support libraries from the CRT, STL, WIL, and GSL
#define BLOCK_TIL // We want to include it later, after DX.
#include "LibraryIncludes.hpp"

#include <windows.hpp>
#include <winmeta.hpp>

#include "../host/conddkrefs.hpp"
#include <condrv.hpp>

#include <cmath>

#include <exception>
#include <typeinfo>

#include <dcomp.hpp>

#include <dxgi.hpp>
#include <dxgi1_2.hpp>
#include <dxgi1_3.hpp>

#include <d3d11.hpp>
#include <d2d1.hpp>
#include <d2d1_1.hpp>
#include <d2d1_2.hpp>
#include <d2d1_3.hpp>
#include <d2d1helper.hpp>
#include <dwrite.hpp>
#include <dwrite_1.hpp>
#include <dwrite_2.hpp>
#include <dwrite_3.hpp>

// Re-include TIL at the bottom to gain DX superpowers.
#include "til.hpp"

#pragma hdrstop
