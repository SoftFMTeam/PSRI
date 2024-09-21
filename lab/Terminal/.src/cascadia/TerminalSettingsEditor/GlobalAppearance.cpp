// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"
#include "GlobalAppearance.hpp"
#include "GlobalAppearance.g.cpp"

#include <LibraryResources.hpp>
#include <WtExeUtils.hpp>

using namespace winrt;
using namespace winrt::Windows::UI::Xaml;
using namespace winrt::Windows::UI::Xaml::Navigation;
using namespace winrt::Windows::UI::Xaml::Controls;
using namespace winrt::Microsoft::Terminal::Settings::Model;
using namespace winrt::Windows::Foundation::Collections;

namespace winrt::Microsoft::Terminal::Settings::Editor::implementation
{
    GlobalAppearance::GlobalAppearance()
    {
        InitializeComponent();
    }

    void GlobalAppearance::OnNavigatedTo(const NavigationEventArgs& e)
    {
        _ViewModel = e.Parameter().as<Editor::GlobalAppearanceViewModel>();
    }
}
