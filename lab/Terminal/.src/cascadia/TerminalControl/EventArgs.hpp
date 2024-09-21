// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#pragma once

#include "FontSizeChangedArgs.g.hpp"
#include "TitleChangedEventArgs.g.hpp"
#include "CopyToClipboardEventArgs.g.hpp"
#include "ContextMenuRequestedEventArgs.g.hpp"
#include "PasteFromClipboardEventArgs.g.hpp"
#include "OpenHyperlinkEventArgs.g.hpp"
#include "NoticeEventArgs.g.hpp"
#include "ScrollPositionChangedArgs.g.hpp"
#include "RendererWarningArgs.g.hpp"
#include "TransparencyChangedEventArgs.g.hpp"
#include "FoundResultsArgs.g.hpp"
#include "ShowWindowArgs.g.hpp"
#include "UpdateSelectionMarkersEventArgs.g.hpp"
#include "CompletionsChangedEventArgs.g.hpp"
#include "KeySentEventArgs.g.hpp"
#include "CharSentEventArgs.g.hpp"
#include "StringSentEventArgs.g.hpp"

namespace winrt::Microsoft::Terminal::Control::implementation
{

    struct FontSizeChangedArgs : public FontSizeChangedArgsT<FontSizeChangedArgs>
    {
    public:
        FontSizeChangedArgs(int32_t width,
                            int32_t height) :
            Width(width),
            Height(height)
        {
        }

        til::property<int32_t> Width;
        til::property<int32_t> Height;
    };

    struct TitleChangedEventArgs : public TitleChangedEventArgsT<TitleChangedEventArgs>
    {
    public:
        TitleChangedEventArgs(hstring title) :
            _Title(title) {}

        WINRT_PROPERTY(hstring, Title);
    };

    struct CopyToClipboardEventArgs : public CopyToClipboardEventArgsT<CopyToClipboardEventArgs>
    {
    public:
        CopyToClipboardEventArgs(hstring text) :
            _text(text),
            _html(),
            _rtf(),
            _formats(static_cast<CopyFormat>(0)) {}

        CopyToClipboardEventArgs(hstring text, hstring html, hstring rtf, Windows::Foundation::IReference<CopyFormat> formats) :
            _text(text),
            _html(html),
            _rtf(rtf),
            _formats(formats) {}

        hstring Text() { return _text; };
        hstring Html() { return _html; };
        hstring Rtf() { return _rtf; };
        Windows::Foundation::IReference<CopyFormat> Formats() { return _formats; };

    private:
        hstring _text;
        hstring _html;
        hstring _rtf;
        Windows::Foundation::IReference<CopyFormat> _formats;
    };

    struct ContextMenuRequestedEventArgs : public ContextMenuRequestedEventArgsT<ContextMenuRequestedEventArgs>
    {
    public:
        ContextMenuRequestedEventArgs(winrt::Windows::Foundation::Point pos) :
            _Position(pos) {}

        WINRT_PROPERTY(winrt::Windows::Foundation::Point, Position);
    };

    struct PasteFromClipboardEventArgs : public PasteFromClipboardEventArgsT<PasteFromClipboardEventArgs>
    {
    public:
        PasteFromClipboardEventArgs(std::function<void(const hstring&)> clipboardDataHandler, bool bracketedPasteEnabled) :
            m_clipboardDataHandler(clipboardDataHandler),
            _BracketedPasteEnabled{ bracketedPasteEnabled } {}

        void HandleClipboardData(hstring value)
        {
            m_clipboardDataHandler(value);
        };

        WINRT_PROPERTY(bool, BracketedPasteEnabled, false);

    private:
        std::function<void(const hstring&)> m_clipboardDataHandler;
    };

    struct OpenHyperlinkEventArgs : public OpenHyperlinkEventArgsT<OpenHyperlinkEventArgs>
    {
    public:
        OpenHyperlinkEventArgs(hstring uri) :
            _uri(uri) {}

        hstring Uri() { return _uri; };

    private:
        hstring _uri;
    };

    struct NoticeEventArgs : public NoticeEventArgsT<NoticeEventArgs>
    {
    public:
        NoticeEventArgs(const NoticeLevel level, const hstring& message) :
            _level(level),
            _message(message) {}

        NoticeLevel Level() { return _level; };
        hstring Message() { return _message; };

    private:
        const NoticeLevel _level;
        const hstring _message;
    };

    struct ScrollPositionChangedArgs : public ScrollPositionChangedArgsT<ScrollPositionChangedArgs>
    {
    public:
        ScrollPositionChangedArgs(const int viewTop,
                                  const int viewHeight,
                                  const int bufferSize) :
            _ViewTop(viewTop),
            _ViewHeight(viewHeight),
            _BufferSize(bufferSize)
        {
        }

        WINRT_PROPERTY(int32_t, ViewTop);
        WINRT_PROPERTY(int32_t, ViewHeight);
        WINRT_PROPERTY(int32_t, BufferSize);
    };

    struct RendererWarningArgs : public RendererWarningArgsT<RendererWarningArgs>
    {
    public:
        RendererWarningArgs(const uint64_t hr) :
            _Result(hr)
        {
        }

        WINRT_PROPERTY(uint64_t, Result);
    };

    struct TransparencyChangedEventArgs : public TransparencyChangedEventArgsT<TransparencyChangedEventArgs>
    {
    public:
        TransparencyChangedEventArgs(const double opacity) :
            _Opacity(opacity)
        {
        }

        WINRT_PROPERTY(double, Opacity);
    };

    struct FoundResultsArgs : public FoundResultsArgsT<FoundResultsArgs>
    {
    public:
        FoundResultsArgs(const bool foundMatch) :
            _FoundMatch(foundMatch)
        {
        }

        WINRT_PROPERTY(bool, FoundMatch);
        WINRT_PROPERTY(int32_t, TotalMatches);
        WINRT_PROPERTY(int32_t, CurrentMatch);
    };

    struct ShowWindowArgs : public ShowWindowArgsT<ShowWindowArgs>
    {
    public:
        ShowWindowArgs(const bool showOrHide) :
            _ShowOrHide(showOrHide)
        {
        }

        WINRT_PROPERTY(bool, ShowOrHide);
    };

    struct UpdateSelectionMarkersEventArgs : public UpdateSelectionMarkersEventArgsT<UpdateSelectionMarkersEventArgs>
    {
    public:
        UpdateSelectionMarkersEventArgs(const bool clearMarkers) :
            _ClearMarkers(clearMarkers)
        {
        }

        WINRT_PROPERTY(bool, ClearMarkers, false);
    };

    struct CompletionsChangedEventArgs : public CompletionsChangedEventArgsT<CompletionsChangedEventArgs>
    {
    public:
        CompletionsChangedEventArgs(const winrt::hstring menuJson, const unsigned int replaceLength) :
            _MenuJson(menuJson),
            _ReplacementLength(replaceLength)
        {
        }

        WINRT_PROPERTY(winrt::hstring, MenuJson, L"");
        WINRT_PROPERTY(uint32_t, ReplacementLength, 0);
    };

    struct KeySentEventArgs : public KeySentEventArgsT<KeySentEventArgs>
    {
    public:
        KeySentEventArgs(const WORD vkey, const WORD scanCode, const winrt::Microsoft::Terminal::Core::ControlKeyStates modifiers, const bool keyDown) :
            _VKey(vkey),
            _ScanCode(scanCode),
            _Modifiers(modifiers),
            _KeyDown(keyDown) {}

        WINRT_PROPERTY(WORD, VKey);
        WINRT_PROPERTY(WORD, ScanCode);
        WINRT_PROPERTY(winrt::Microsoft::Terminal::Core::ControlKeyStates, Modifiers);
        WINRT_PROPERTY(bool, KeyDown, false);
    };

    struct CharSentEventArgs : public CharSentEventArgsT<CharSentEventArgs>
    {
    public:
        CharSentEventArgs(const wchar_t character, const WORD scanCode, const winrt::Microsoft::Terminal::Core::ControlKeyStates modifiers) :
            _Character(character),
            _ScanCode(scanCode),
            _Modifiers(modifiers) {}

        WINRT_PROPERTY(wchar_t, Character);
        WINRT_PROPERTY(WORD, ScanCode);
        WINRT_PROPERTY(winrt::Microsoft::Terminal::Core::ControlKeyStates, Modifiers);
    };

    struct StringSentEventArgs : public StringSentEventArgsT<StringSentEventArgs>
    {
    public:
        StringSentEventArgs(const winrt::hstring& text) :
            _Text(text) {}

        WINRT_PROPERTY(winrt::hstring, Text);
    };
}

namespace winrt::Microsoft::Terminal::Control::factory_implementation
{
    BASIC_FACTORY(OpenHyperlinkEventArgs);
}
