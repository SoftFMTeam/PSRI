// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

#include "precomp.hpp"

void InitSideBySide(_Out_writes_(ScratchBufferSize) PWSTR ScratchBuffer, __range(MAX_PATH, MAX_PATH) DWORD ScratchBufferSize);
void InitEnvironmentVariables();
