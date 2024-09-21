// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"
#include "Profiles_Advanced.hpp"
#include "Profiles_Advanced.g.cpp"
#include "ProfileViewModel.hpp"

#include "EnumEntry.hpp"
#include <LibraryResources.hpp>
#include "..\WinRTUtils\inc\Utils.hpp"

using namespace winrt::Windows::UI::Xaml::Navigation;

namespace winrt::Microsoft::Terminal::Settings::Editor::implementation
{
    Profiles_Advanced::Profiles_Advanced()
    {
        InitializeComponent();
    }

    void Profiles_Advanced::OnNavigatedTo(const NavigationEventArgs& e)
    {
        _Profile = e.Parameter().as<Editor::ProfileViewModel>();
    }

    void Profiles_Advanced::OnNavigatedFrom(const NavigationEventArgs& /*e*/)
    {
        _ViewModelChangedRevoker.revoke();
    }
}
