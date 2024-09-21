#pragma once

#define WIN32_LEAN_AND_MEAN
// Manually include til after we include Windows.Foundation to give it winrt superpowers
#define BLOCK_TIL
#include <wil/cppwinrt.hpp>
#undef max
#undef min
#include "LibraryIncludes.hpp"

// This is inexplicable, but for whatever reason, cppwinrt conflicts with the
//      SDK definition of this function, so the only fix is to undef it.
// from WinBase.h
// Windows::UI::Xaml::Media::Animation::IStoryboard::GetCurrentTime
#ifdef GetCurrentTime
#undef GetCurrentTime
#endif

#include <Unknwn.hpp>
#include <winrt/Windows.Foundation.hpp>
#include <winrt/Windows.Foundation.Collections.hpp>

// Manually include til after we include Windows.Foundation to give it winrt superpowers
#include "til.hpp"

#include <conio.hpp>

#include <cppwinrt_utils.hpp>
