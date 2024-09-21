// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include <windows.hpp>
#include <cstdlib>
#include <cstdio>
#include <appmodel.hpp>
#include <strsafe.hpp>

#include "util.hpp"

#pragma optimize("", off)
#pragma warning(disable : 4748)

int __cdecl wmain(int /*argc*/, __in_ecount(argc) PCWSTR* /*argv*/)
{
    TestLibFunc();

    return 0;
}
