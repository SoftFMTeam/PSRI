// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"
#include "Rendering.hpp"
#include "Rendering.g.cpp"

using namespace winrt::Windows::UI::Xaml::Navigation;

namespace winrt::Microsoft::Terminal::Settings::Editor::implementation
{
    Rendering::Rendering()
    {
        InitializeComponent();
    }

    void Rendering::OnNavigatedTo(const NavigationEventArgs& e)
    {
        _ViewModel = e.Parameter().as<Editor::RenderingViewModel>();
    }
}
