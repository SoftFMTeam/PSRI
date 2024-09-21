// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"
#include "SeparatorEntry.hpp"
#include "JsonUtils.hpp"

#include "SeparatorEntry.g.cpp"

using namespace Microsoft::Terminal::Settings::Model;
using namespace winrt::Microsoft::Terminal::Settings::Model::implementation;

SeparatorEntry::SeparatorEntry() noexcept :
    SeparatorEntryT<SeparatorEntry, NewTabMenuEntry>(NewTabMenuEntryType::Separator)
{
}

winrt::com_ptr<NewTabMenuEntry> SeparatorEntry::FromJson(const Json::Value&)
{
    return winrt::make_self<SeparatorEntry>();
}
