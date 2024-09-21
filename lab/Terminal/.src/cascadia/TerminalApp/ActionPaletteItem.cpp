// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"
#include "ActionPaletteItem.hpp"
#include <LibraryResources.hpp>

#include "ActionPaletteItem.g.cpp"

using namespace winrt;
using namespace winrt::TerminalApp;
using namespace winrt::Windows::UI::Core;
using namespace winrt::Windows::UI::Xaml;
using namespace winrt::Windows::System;
using namespace winrt::Windows::Foundation;
using namespace winrt::Windows::Foundation::Collections;
using namespace winrt::Microsoft::Terminal::Settings::Model;

namespace winrt::TerminalApp::implementation
{
    ActionPaletteItem::ActionPaletteItem(const Microsoft::Terminal::Settings::Model::Command& command) :
        _Command(command)
    {
        Name(command.Name());
        KeyChordText(command.KeyChordText());
        Icon(command.IconPath());
    }
}
