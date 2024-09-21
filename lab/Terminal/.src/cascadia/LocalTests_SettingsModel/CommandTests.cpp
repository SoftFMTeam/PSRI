// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "pch.hpp"

#include "../TerminalSettingsModel/CascadiaSettings.hpp"
#include "JsonTestClass.hpp"
#include "TestUtils.hpp"

using namespace Microsoft::Console;
using namespace winrt::Microsoft::Terminal::Settings::Model;
using namespace winrt::Microsoft::Terminal::Control;
using namespace winrt::Windows::Foundation::Collections;
using namespace WEX::Logging;
using namespace WEX::TestExecution;
using namespace WEX::Common;

namespace SettingsModelLocalTests
{
    // TODO:microsoft/terminal#3838:
    // Unfortunately, these tests _WILL NOT_ work in our CI. We're waiting for
    // an updated TAEF that will let us install framework packages when the test
    // package is deployed. Until then, these tests won't deploy in CI.

    class CommandTests : public JsonTestClass
    {
        // Use a custom AppxManifest to ensure that we can activate winrt types
        // from our test. This property will tell taef to manually use this as
        // the AppxManifest for this test class.
        // This does not yet work for anything XAML-y. See TabTests.cpp for more
        // details on that.
        BEGIN_TEST_CLASS(CommandTests)
            TEST_CLASS_PROPERTY(L"RunAs", L"UAP")
            TEST_CLASS_PROPERTY(L"UAP:AppXManifest", L"TestHostAppXManifest.xml")
        END_TEST_CLASS()

        TEST_METHOD(ManyCommandsSameAction);
        TEST_METHOD(LayerCommand);
        TEST_METHOD(TestSplitPaneArgs);
        TEST_METHOD(TestSplitPaneBadSize);
        TEST_METHOD(TestResourceKeyName);
        TEST_METHOD(TestAutogeneratedName);
        TEST_METHOD(TestLayerOnAutogeneratedName);

        TEST_METHOD(TestGenerateCommandline);
    };

    void CommandTests::ManyCommandsSameAction()
    {
        const std::string commands0String{ R"([ { "name":"action0", "command": "copy" } ])" };
        const std::string commands1String{ R"([ { "name":"action1", "command": { "action": "copy", "singleLine": false } } ])" };
        const std::string commands2String{ R"([
            { "name":"action2", "command": "paste" },
            { "name":"action3", "command": "paste" }
        ])" };

        const auto commands0Json = VerifyParseSucceeded(commands0String);
        const auto commands1Json = VerifyParseSucceeded(commands1String);
        const auto commands2Json = VerifyParseSucceeded(commands2String);

        auto commands = winrt::single_threaded_map<winrt::hstring, Command>();
        VERIFY_ARE_EQUAL(0u, commands.Size());
        {
            auto warnings = implementation::Command::LayerJson(commands, commands0Json);
            VERIFY_ARE_EQUAL(0u, warnings.size());
        }
        VERIFY_ARE_EQUAL(1u, commands.Size());

        {
            auto warnings = implementation::Command::LayerJson(commands, commands1Json);
            VERIFY_ARE_EQUAL(0u, warnings.size());
        }
        VERIFY_ARE_EQUAL(2u, commands.Size());

        {
            auto warnings = implementation::Command::LayerJson(commands, commands2Json);
            VERIFY_ARE_EQUAL(0u, warnings.size());
        }
        VERIFY_ARE_EQUAL(4u, commands.Size());
    }

    void CommandTests::LayerCommand()
    {
        // Each one of the commands in this test should layer upon the previous, overriding the action.
        const std::string commands0String{ R"([ { "name":"action0", "command": "copy" } ])" };
        const std::string commands1String{ R"([ { "name":"action0", "command": "paste" } ])" };
        const std::string commands2String{ R"([ { "name":"action0", "command": "newTab" } ])" };
        const std::string commands3String{ R"([ { "name":"action0", "command": null } ])" };

        const auto commands0Json = VerifyParseSucceeded(commands0String);
        const auto commands1Json = VerifyParseSucceeded(commands1String);
        const auto commands2Json = VerifyParseSucceeded(commands2String);
        const auto commands3Json = VerifyParseSucceeded(commands3String);

        auto commands = winrt::single_threaded_map<winrt::hstring, Command>();
        VERIFY_ARE_EQUAL(0u, commands.Size());
        {
            auto warnings = implementation::Command::LayerJson(commands, commands0Json);
            VERIFY_ARE_EQUAL(0u, warnings.size());
            VERIFY_ARE_EQUAL(1u, commands.Size());
            auto command = commands.Lookup(L"action0");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::CopyText, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<CopyTextArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
        }
        {
            auto warnings = implementation::Command::LayerJson(commands, commands1Json);
            VERIFY_ARE_EQUAL(0u, warnings.size());
            VERIFY_ARE_EQUAL(1u, commands.Size());
            auto command = commands.Lookup(L"action0");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::PasteText, command.ActionAndArgs().Action());
            VERIFY_IS_NULL(command.ActionAndArgs().Args());
        }
        {
            auto warnings = implementation::Command::LayerJson(commands, commands2Json);
            VERIFY_ARE_EQUAL(0u, warnings.size());
            VERIFY_ARE_EQUAL(1u, commands.Size());
            auto command = commands.Lookup(L"action0");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewTab, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewTabArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
        }
        {
            // This last command should "unbind" the action.
            auto warnings = implementation::Command::LayerJson(commands, commands3Json);
            VERIFY_ARE_EQUAL(0u, warnings.size());
            VERIFY_ARE_EQUAL(0u, commands.Size());
        }
    }

    void CommandTests::TestSplitPaneArgs()
    {
        // This is the same as KeyBindingsTests::TestSplitPaneArgs, but with
        // looking up the action and its args from a map of commands, instead
        // of from keybindings.

        const std::string commands0String{ R"([
            { "name": "command1", "command": { "action": "splitPane", "split": "vertical" } },
            { "name": "command2", "command": { "action": "splitPane", "split": "horizontal" } },
            { "name": "command4", "command": { "action": "splitPane" } },
            { "name": "command5", "command": { "action": "splitPane", "split": "auto" } },
            { "name": "command6", "command": { "action": "splitPane", "size": 0.25 } },
            { "name": "command7", "command": { "action": "splitPane", "split": "right" } },
            { "name": "command8", "command": { "action": "splitPane", "split": "left" } },
            { "name": "command9", "command": { "action": "splitPane", "split": "up" } },
            { "name": "command10", "command": { "action": "splitPane", "split": "down" } },
        ])" };

        const auto commands0Json = VerifyParseSucceeded(commands0String);

        auto commands = winrt::single_threaded_map<winrt::hstring, Command>();
        VERIFY_ARE_EQUAL(0u, commands.Size());
        auto warnings = implementation::Command::LayerJson(commands, commands0Json);
        VERIFY_ARE_EQUAL(0u, warnings.size());
        VERIFY_ARE_EQUAL(9u, commands.Size());

        {
            auto command = commands.Lookup(L"command1");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Right, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.5, realArgs.SplitSize());
        }
        {
            auto command = commands.Lookup(L"command2");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Down, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.5, realArgs.SplitSize());
        }
        {
            auto command = commands.Lookup(L"command4");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Automatic, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.5, realArgs.SplitSize());
        }
        {
            auto command = commands.Lookup(L"command5");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Automatic, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.5, realArgs.SplitSize());
        }
        {
            auto command = commands.Lookup(L"command6");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Automatic, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.25, realArgs.SplitSize());
        }
        {
            auto command = commands.Lookup(L"command7");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Right, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.5, realArgs.SplitSize());
        }
        {
            auto command = commands.Lookup(L"command8");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Left, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.5, realArgs.SplitSize());
        }
        {
            auto command = commands.Lookup(L"command9");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Up, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.5, realArgs.SplitSize());
        }
        {
            auto command = commands.Lookup(L"command10");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Down, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.5, realArgs.SplitSize());
        }
    }

    void CommandTests::TestSplitPaneBadSize()
    {
        const std::string commands0String{ R"([
            { "name": "command1", "command": { "action": "splitPane", "size": 0.25 } },
            { "name": "command2", "command": { "action": "splitPane", "size": 1.0 } },
            { "name": "command3", "command": { "action": "splitPane", "size": 0 } },
            { "name": "command4", "command": { "action": "splitPane", "size": 50 } },
        ])" };

        const auto commands0Json = VerifyParseSucceeded(commands0String);

        auto commands = winrt::single_threaded_map<winrt::hstring, Command>();
        VERIFY_ARE_EQUAL(0u, commands.Size());
        auto warnings = implementation::Command::LayerJson(commands, commands0Json);
        VERIFY_ARE_EQUAL(3u, warnings.size());
        VERIFY_ARE_EQUAL(1u, commands.Size());

        {
            auto command = commands.Lookup(L"command1");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Automatic, realArgs.SplitDirection());
            VERIFY_ARE_EQUAL(0.25, realArgs.SplitSize());
        }
    }

    void CommandTests::TestResourceKeyName()
    {
        // This test checks looking up a name from a resource key.

        const std::string commands0String{ R"([ { "name": { "key": "DuplicateTabCommandKey"}, "command": "copy" } ])" };
        const auto commands0Json = VerifyParseSucceeded(commands0String);

        auto commands = winrt::single_threaded_map<winrt::hstring, Command>();
        VERIFY_ARE_EQUAL(0u, commands.Size());
        {
            auto warnings = implementation::Command::LayerJson(commands, commands0Json);
            VERIFY_ARE_EQUAL(0u, warnings.size());
            VERIFY_ARE_EQUAL(1u, commands.Size());

            // NOTE: We're relying on DuplicateTabCommandKey being defined as
            // "Duplicate Tab" here. If that string changes in our resources,
            // this test will break.
            auto command = commands.Lookup(L"Duplicate tab");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::CopyText, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<CopyTextArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
        }
    }

    void CommandTests::TestAutogeneratedName()
    {
        // This test ensures that we'll correctly create commands for actions
        // that don't have given names, pursuant to the spec in GH#6532.

        // NOTE: The keys used to look up these commands are partially generated
        // from strings in our Resources.resw. If those string values should
        // change, it's likely that this test will break.

        const std::string commands0String{ R"([
            { "command": { "action": "splitPane", "split": null } },
            { "command": { "action": "splitPane", "split": "left" } },
            { "command": { "action": "splitPane", "split": "right" } },
            { "command": { "action": "splitPane", "split": "up" } },
            { "command": { "action": "splitPane", "split": "down" } },
            { "command": { "action": "splitPane", "split": "none" } },
            { "command": { "action": "splitPane" } },
            { "command": { "action": "splitPane", "split": "auto" } },
            { "command": { "action": "splitPane", "split": "foo" } }
        ])" };

        const auto commands0Json = VerifyParseSucceeded(commands0String);

        auto commands = winrt::single_threaded_map<winrt::hstring, Command>();
        VERIFY_ARE_EQUAL(0u, commands.Size());
        auto warnings = implementation::Command::LayerJson(commands, commands0Json);
        VERIFY_ARE_EQUAL(0u, warnings.size());

        // There are only 5 commands here: all of the `"none"`, `"auto"`,
        // `"foo"`, `null`, and <no args> bindings all generate the same action,
        // which will generate just a single name for all of them.
        VERIFY_ARE_EQUAL(5u, commands.Size());

        {
            auto command = commands.Lookup(L"Split pane");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Automatic, realArgs.SplitDirection());
        }
        {
            auto command = commands.Lookup(L"Split pane, split: left");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Left, realArgs.SplitDirection());
        }
        {
            auto command = commands.Lookup(L"Split pane, split: right");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Right, realArgs.SplitDirection());
        }
        {
            auto command = commands.Lookup(L"Split pane, split: up");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Up, realArgs.SplitDirection());
        }
        {
            auto command = commands.Lookup(L"Split pane, split: down");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Down, realArgs.SplitDirection());
        }
    }
    void CommandTests::TestLayerOnAutogeneratedName()
    {
        const std::string commands0String{ R"([
            { "command": { "action": "splitPane" } },
            { "name":"Split pane", "command": { "action": "splitPane", "split": "vertical" } },
        ])" };

        const auto commands0Json = VerifyParseSucceeded(commands0String);

        auto commands = winrt::single_threaded_map<winrt::hstring, Command>();
        VERIFY_ARE_EQUAL(0u, commands.Size());
        auto warnings = implementation::Command::LayerJson(commands, commands0Json);
        VERIFY_ARE_EQUAL(0u, warnings.size());
        VERIFY_ARE_EQUAL(1u, commands.Size());

        {
            auto command = commands.Lookup(L"Split pane");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::SplitPane, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<SplitPaneArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            // Verify the args have the expected value
            VERIFY_ARE_EQUAL(SplitDirection::Right, realArgs.SplitDirection());
        }
    }

    void CommandTests::TestGenerateCommandline()
    {
        const WEX::TestExecution::DisableVerifyExceptions disableExceptionsScope;

        const std::string commands0String{ R"([
            {
                "name":"action0",
                "command": { "action": "newWindow" }
            },
            {
                "name":"action1",
                "command": { "action": "newTab", "profile": "foo" }
            },
            {
                "name":"action2",
                "command": { "action": "newWindow", "profile": "foo" }
            },
            {
                "name":"action3",
                "command": { "action": "newWindow", "commandline": "bar.exe" }
            },
            {
                "name":"action4",
                "command": { "action": "newWindow", "commandline": "pop.exe ya ha ha" }
            },
            {
                "name":"action5",
                "command": { "action": "newWindow", "commandline": "pop.exe \"ya ha ha\"" }
            },
            {
                "name":"action6",
                "command": { "action": "newWindow", "startingDirectory":"C:\\foo", "commandline": "bar.exe" }
            },
            {
                "name":"action7_startingDirectoryWithTrailingSlash",
                "command": { "action": "newWindow", "startingDirectory":"C:\\", "commandline": "bar.exe" }
            },
            {
                "name":"action8_tabTitleEscaping",
                "command": { "action": "newWindow", "tabTitle":"\\\";foo\\" }
            }
        ])" };

        const auto commands0Json = VerifyParseSucceeded(commands0String);

        auto commands = winrt::single_threaded_map<winrt::hstring, Command>();
        VERIFY_ARE_EQUAL(0u, commands.Size());
        auto warnings = implementation::Command::LayerJson(commands, commands0Json);
        VERIFY_ARE_EQUAL(0u, warnings.size());
        VERIFY_ARE_EQUAL(9u, commands.Size());

        {
            auto command = commands.Lookup(L"action0");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewWindow, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewWindowArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            const auto& terminalArgs = realArgs.TerminalArgs();
            VERIFY_IS_NOT_NULL(terminalArgs);
            auto cmdline = terminalArgs.ToCommandline();
            VERIFY_ARE_EQUAL(L"", cmdline);
        }

        {
            auto command = commands.Lookup(L"action1");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewTab, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewTabArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            const auto& terminalArgs = realArgs.TerminalArgs();
            VERIFY_IS_NOT_NULL(terminalArgs);
            auto cmdline = terminalArgs.ToCommandline();
            VERIFY_ARE_EQUAL(L"--profile \"foo\"", cmdline);
        }

        {
            auto command = commands.Lookup(L"action2");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewWindow, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewWindowArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            const auto& terminalArgs = realArgs.TerminalArgs();
            VERIFY_IS_NOT_NULL(terminalArgs);
            auto cmdline = terminalArgs.ToCommandline();
            VERIFY_ARE_EQUAL(L"--profile \"foo\"", cmdline);
        }

        {
            auto command = commands.Lookup(L"action3");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewWindow, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewWindowArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            const auto& terminalArgs = realArgs.TerminalArgs();
            VERIFY_IS_NOT_NULL(terminalArgs);
            auto cmdline = terminalArgs.ToCommandline();
            VERIFY_ARE_EQUAL(L"-- \"bar.exe\"", cmdline);
        }

        {
            auto command = commands.Lookup(L"action4");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewWindow, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewWindowArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            const auto& terminalArgs = realArgs.TerminalArgs();
            VERIFY_IS_NOT_NULL(terminalArgs);
            auto cmdline = terminalArgs.ToCommandline();
            Log::Comment(NoThrowString().Format(
                L"cmdline: \"%s\"", cmdline.c_str()));
            VERIFY_ARE_EQUAL(L"-- \"pop.exe ya ha ha\"", terminalArgs.ToCommandline());
        }

        {
            auto command = commands.Lookup(L"action5");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewWindow, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewWindowArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            const auto& terminalArgs = realArgs.TerminalArgs();
            VERIFY_IS_NOT_NULL(terminalArgs);
            auto cmdline = terminalArgs.ToCommandline();
            Log::Comment(NoThrowString().Format(
                L"cmdline: \"%s\"", cmdline.c_str()));
            VERIFY_ARE_EQUAL(L"-- \"pop.exe \"ya ha ha\"\"", terminalArgs.ToCommandline());
        }

        {
            auto command = commands.Lookup(L"action6");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewWindow, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewWindowArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            const auto& terminalArgs = realArgs.TerminalArgs();
            VERIFY_IS_NOT_NULL(terminalArgs);
            auto cmdline = terminalArgs.ToCommandline();
            Log::Comment(NoThrowString().Format(
                L"cmdline: \"%s\"", cmdline.c_str()));
            VERIFY_ARE_EQUAL(L"--startingDirectory \"C:\\foo\" -- \"bar.exe\"", terminalArgs.ToCommandline());
        }

        {
            auto command = commands.Lookup(L"action7_startingDirectoryWithTrailingSlash");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewWindow, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewWindowArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            const auto& terminalArgs = realArgs.TerminalArgs();
            VERIFY_IS_NOT_NULL(terminalArgs);
            auto cmdline = terminalArgs.ToCommandline();
            Log::Comment(NoThrowString().Format(
                L"cmdline: \"%s\"", cmdline.c_str()));
            VERIFY_ARE_EQUAL(L"--startingDirectory \"C:\\\\\" -- \"bar.exe\"", terminalArgs.ToCommandline());
        }

        {
            auto command = commands.Lookup(L"action8_tabTitleEscaping");
            VERIFY_IS_NOT_NULL(command);
            VERIFY_IS_NOT_NULL(command.ActionAndArgs());
            VERIFY_ARE_EQUAL(ShortcutAction::NewWindow, command.ActionAndArgs().Action());
            const auto& realArgs = command.ActionAndArgs().Args().try_as<NewWindowArgs>();
            VERIFY_IS_NOT_NULL(realArgs);
            const auto& terminalArgs = realArgs.TerminalArgs();
            VERIFY_IS_NOT_NULL(terminalArgs);
            auto cmdline = terminalArgs.ToCommandline();
            Log::Comment(NoThrowString().Format(
                L"cmdline: \"%s\"", cmdline.c_str()));
            VERIFY_ARE_EQUAL(LR"-(--title "\\\"\;foo\\")-", terminalArgs.ToCommandline());
        }
    }
}
