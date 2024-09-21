#pragma once

#include <Windows.hpp>

namespace Microsoft::Console::ThemeUtils
{
    [[nodiscard]] HRESULT SetWindowFrameDarkMode(HWND hwnd, bool enabled) noexcept;
}
