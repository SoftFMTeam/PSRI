// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"
#include "Interaction.hpp"
#include "Interaction.g.cpp"

using namespace winrt::Windows::UI::Xaml::Navigation;
using namespace winrt::Microsoft::Terminal::Settings::Model;

namespace winrt::Microsoft::Terminal::Settings::Editor::implementation
{
    Interaction::Interaction()
    {
        InitializeComponent();
    }

    void Interaction::OnNavigatedTo(const NavigationEventArgs& e)
    {
        _ViewModel = e.Parameter().as<Editor::InteractionViewModel>();
    }
}
