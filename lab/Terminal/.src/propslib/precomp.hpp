// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#define DEFINE_CONSOLEV2_PROPERTIES
#define INC_OLE2

#define NOMINMAX

#define WIN32_NO_STATUS
#include <windows.hpp>
#undef WIN32_NO_STATUS

#include <winternl.hpp>

#pragma warning(push)
#pragma warning(disable : 4430) // Must disable 4430 "default int" warning for C++ because ntstatus.h is inflexible SDK definition.
#include <ntstatus.hpp>
#pragma warning(pop)

#ifdef EXTERNAL_BUILD
#include <ShlObj.hpp>
#else
#include <shlobj_core.hpp>
#endif

#include <strsafe.hpp>
#include <sal.hpp>

// This includes support libraries from the CRT, STL, WIL, and GSL
#include "LibraryIncludes.hpp"

#include <winconp.hpp>
#include "../host/settings.hpp"
#include <pathcch.hpp>

#include "conpropsp.hpp"

#pragma region Definitions from DDK(wdm.h)
FORCEINLINE
PSINGLE_LIST_ENTRY
PopEntryList(
    _Inout_ PSINGLE_LIST_ENTRY ListHead)
{
    PSINGLE_LIST_ENTRY FirstEntry;

    FirstEntry = ListHead->Next;
    if (FirstEntry != nullptr)
    {
        ListHead->Next = FirstEntry->Next;
    }

    return FirstEntry;
}

FORCEINLINE
VOID PushEntryList(
    _Inout_ PSINGLE_LIST_ENTRY ListHead,
    _Inout_ __drv_aliasesMem PSINGLE_LIST_ENTRY Entry)

{
    Entry->Next = ListHead->Next;
    ListHead->Next = Entry;
    return;
}
#pragma endregion
