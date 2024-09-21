// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

#include "ColorTableEntry.g.hpp"
#include "ColorSchemes.g.hpp"
#include "ColorSchemeViewModel.hpp"
#include "ColorSchemesPageViewModel.hpp"
#include "Utils.hpp"

namespace winrt::Microsoft::Terminal::Settings::Editor::implementation
{
    struct ColorSchemes : public HasScrollViewer<ColorSchemes>, ColorSchemesT<ColorSchemes>
    {
    public:
        ColorSchemes();

        void OnNavigatedTo(const winrt::Windows::UI::Xaml::Navigation::NavigationEventArgs& e);

        void AddNew_Click(const winrt::Windows::Foundation::IInspectable& sender, const winrt::Windows::UI::Xaml::RoutedEventArgs& e);
        void ListView_PreviewKeyDown(const winrt::Windows::Foundation::IInspectable& sender, const winrt::Windows::UI::Xaml::Input::KeyRoutedEventArgs& e);

        WINRT_PROPERTY(Model::ColorScheme, CurrentColorScheme, nullptr);
        WINRT_OBSERVABLE_PROPERTY(Editor::ColorSchemesPageViewModel, ViewModel, _PropertyChangedHandlers, nullptr);

        WINRT_CALLBACK(PropertyChanged, Windows::UI::Xaml::Data::PropertyChangedEventHandler);

    private:
        winrt::Windows::UI::Xaml::FrameworkElement::LayoutUpdated_revoker _layoutUpdatedRevoker;
    };
}

namespace winrt::Microsoft::Terminal::Settings::Editor::factory_implementation
{
    BASIC_FACTORY(ColorSchemes);
}
