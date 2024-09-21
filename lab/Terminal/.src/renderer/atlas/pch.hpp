// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

#define NOMINMAX
#define WIN32_LEAN_AND_MEAN

#include <array>
#include <filesystem>
#include <optional>
#include <shared_mutex>
#include <span>
#include <sstream>
#include <string_view>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include <d2d1_3.hpp>
#include <d3d11_2.hpp>
#include <d3dcompiler.hpp>
#include <dcomp.hpp>
#include <dwrite_3.hpp>
#include <dxgi1_3.hpp>
#include <dxgidebug.hpp>
#include <VersionHelpers.hpp>

#include <gsl/gsl_util>
#include <gsl/pointers>
#include <wil/com.hpp>
#include <wil/filesystem.hpp>
#include <wil/result_macros.hpp>
#include <wil/stl.hpp>
#include <wil/win32_helpers.hpp>

// Dynamic Bitset (optional dependency on LibPopCnt for perf at bit counting)
// Variable-size compressed-storage header-only bit flag storage library.
#pragma warning(push)
#pragma warning(disable : 4702) // unreachable code
#include <dynamic_bitset.hpp>
#pragma warning(pop)

// Chromium Numerics (safe math)
#pragma warning(push)
#pragma warning(disable : 4100) // '...': unreferenced formal parameter
#pragma warning(disable : 26812) // The enum type '...' is unscoped. Prefer 'enum class' over 'enum' (Enum.3).
#include <base/numerics/safe_math.hpp>
#pragma warning(pop)

#include <til.hpp>
#include <til/bit.hpp>
