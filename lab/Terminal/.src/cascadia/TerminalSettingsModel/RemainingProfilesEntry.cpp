// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"
#include "RemainingProfilesEntry.hpp"
#include "NewTabMenuEntry.hpp"
#include "JsonUtils.hpp"

#include "RemainingProfilesEntry.g.cpp"

using namespace Microsoft::Terminal::Settings::Model;
using namespace winrt::Microsoft::Terminal::Settings::Model::implementation;

RemainingProfilesEntry::RemainingProfilesEntry() noexcept :
    RemainingProfilesEntryT<RemainingProfilesEntry, ProfileCollectionEntry>(NewTabMenuEntryType::RemainingProfiles)
{
}

winrt::com_ptr<NewTabMenuEntry> RemainingProfilesEntry::FromJson(const Json::Value&)
{
    return winrt::make_self<RemainingProfilesEntry>();
}
