// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"
#include <LibraryResources.hpp>
#include "PaletteItem.hpp"
#include "PaletteItem.g.cpp"

using namespace winrt;
using namespace winrt::Windows::UI::Xaml;
using namespace winrt::Windows::UI::Core;
using namespace winrt::Microsoft::Terminal::Control;
using namespace winrt::Microsoft::Terminal::Settings::Model;
using namespace winrt::Windows::System;

namespace winrt::TerminalApp::implementation
{
    Controls::IconElement PaletteItem::ResolvedIcon()
    {
        const auto icon = IconPathConverter::IconWUX(Icon());
        icon.Width(16);
        icon.Height(16);
        return icon;
    }
}
