// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"
#include "VsSetupConfiguration.hpp"

using namespace winrt::Microsoft::Terminal::Settings::Model;

std::vector<VsSetupConfiguration::VsSetupInstance> VsSetupConfiguration::QueryInstances()
{
    std::vector<VsSetupInstance> instances;

    // SetupConfiguration is only registered if Visual Studio is installed
    ComPtrSetupQuery pQuery{ wil::CoCreateInstanceNoThrow<SetupConfiguration, ISetupConfiguration2>() };
    if (pQuery == nullptr)
    {
        return instances;
    }

    // Enumerate all valid instances of Visual Studio
    wil::com_ptr<IEnumSetupInstances> e;
    THROW_IF_FAILED(pQuery->EnumInstances(&e));

    for (ComPtrSetupInstance rgpInstance; S_OK == THROW_IF_FAILED(e->Next(1, &rgpInstance, nullptr));)
    {
        instances.emplace_back(pQuery, std::move(rgpInstance));
    }

    // Sort instances based on version and install date from latest to oldest.
    std::sort(instances.begin(), instances.end(), [](const VsSetupInstance& a, const VsSetupInstance& b) {
        const auto aVersion = a.GetComparableVersion();
        const auto bVersion = b.GetComparableVersion();

        if (aVersion == bVersion)
        {
            return a.GetComparableInstallDate() > b.GetComparableInstallDate();
        }

        return aVersion > bVersion;
    });

    return instances;
}

/// <summary>
/// Takes a relative path under a Visual Studio installation and returns the absolute path.
/// </summary>
std::wstring VsSetupConfiguration::ResolvePath(ISetupInstance* pInst, std::wstring_view relativePath)
{
    wil::unique_bstr bstrAbsolutePath;
    THROW_IF_FAILED(pInst->ResolvePath(relativePath.data(), &bstrAbsolutePath));
    return bstrAbsolutePath.get();
}

/// <summary>
/// Determines whether a Visual Studio installation version falls within a specified range.
/// The range is specified as a string, ex: "[15.0.0.0,)", "[15.0.0.0, 16.7.0.0)
/// </summary>
bool VsSetupConfiguration::InstallationVersionInRange(ISetupConfiguration2* pQuery, ISetupInstance* pInst, std::wstring_view range)
{
    const auto helper = wil::com_query<ISetupHelper>(pQuery);

    // VS versions in a string format such as "16.3.0.0" can be easily compared
    // by parsing them into 64-bit unsigned integers using the stable algorithm
    // provided by ParseVersion and ParseVersionRange

    unsigned long long minVersion{ 0 };
    unsigned long long maxVersion{ 0 };
    THROW_IF_FAILED(helper->ParseVersionRange(range.data(), &minVersion, &maxVersion));

    wil::unique_bstr bstrVersion;
    THROW_IF_FAILED(pInst->GetInstallationVersion(&bstrVersion));

    unsigned long long ullVersion{ 0 };
    THROW_IF_FAILED(helper->ParseVersion(bstrVersion.get(), &ullVersion));

    return ullVersion >= minVersion && ullVersion <= maxVersion;
}

std::wstring VsSetupConfiguration::GetInstallationVersion(ISetupInstance* pInst)
{
    wil::unique_bstr bstrInstallationVersion;
    THROW_IF_FAILED(pInst->GetInstallationVersion(&bstrInstallationVersion));
    return bstrInstallationVersion.get();
}

std::wstring VsSetupConfiguration::GetInstallationPath(ISetupInstance* pInst)
{
    wil::unique_bstr bstrInstallationPath;
    THROW_IF_FAILED(pInst->GetInstallationPath(&bstrInstallationPath));
    return bstrInstallationPath.get();
}

/// <summary>
/// The instance id is unique for each Visual Studio installation on a system.
/// The instance id is generated by the Visual Studio setup engine and varies from system to system.
/// </summary>
std::wstring VsSetupConfiguration::GetInstanceId(ISetupInstance* pInst)
{
    wil::unique_bstr bstrInstanceId;
    THROW_IF_FAILED(pInst->GetInstanceId(&bstrInstanceId));
    return bstrInstanceId.get();
}

unsigned long long VsSetupConfiguration::GetInstallDate(ISetupInstance* pInst)
{
    FILETIME ftInstallDate{ 0 };
    THROW_IF_FAILED(pInst->GetInstallDate(&ftInstallDate));
    return wil::filetime::to_int64(ftInstallDate);
}

std::wstring VsSetupConfiguration::GetStringProperty(ISetupPropertyStore* pProps, std::wstring_view name)
{
    if (pProps == nullptr)
    {
        return std::wstring{};
    }

    wil::unique_variant var;
    if (FAILED(pProps->GetValue(name.data(), &var)) || var.vt != VT_BSTR)
    {
        return std::wstring{};
    }

    return var.bstrVal;
}
