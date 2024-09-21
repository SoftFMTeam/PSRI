// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

#include <wrl.hpp>
#include <wrl/client.hpp>
#include <wrl/implements.hpp>

#include "IBoxDrawingEffect_h.hpp"

namespace Microsoft::Console::Render
{
    class BoxDrawingEffect : public ::Microsoft::WRL::RuntimeClass<::Microsoft::WRL::RuntimeClassFlags<::Microsoft::WRL::ClassicCom | ::Microsoft::WRL::InhibitFtmBase>, IBoxDrawingEffect>
    {
    public:
        BoxDrawingEffect() noexcept;
        HRESULT RuntimeClassInitialize(float verticalScale, float verticalTranslate, float horizontalScale, float horizontalTranslate) noexcept;

        [[nodiscard]] HRESULT STDMETHODCALLTYPE GetScale(BoxScale* scale) noexcept override;

    protected:
    private:
        BoxScale _scale;
#ifdef UNIT_TESTING
    public:
        friend class BoxDrawingEffectTests;
#endif
    };
}
