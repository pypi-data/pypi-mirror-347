"""CLI interaction functionality for TerminalAI."""
import os
import sys
import argparse
from terminalai.command_utils import run_shell_command, is_shell_command
from terminalai.command_extraction import is_stateful_command, is_risky_command
from terminalai.clipboard_utils import copy_to_clipboard

# Imports for rich components - from HEAD, as 021offshoot was missing some
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

# Imports for terminalai components - from HEAD, as 021offshoot was missing some
from terminalai.config import (
    load_config, save_config,
    get_system_prompt, DEFAULT_SYSTEM_PROMPT
)
from terminalai.shell_integration import (
    install_shell_integration, uninstall_shell_integration,
    check_shell_integration, get_system_context
)
from terminalai.ai_providers import get_provider
from terminalai.formatting import print_ai_answer_with_rich
# Use the more specific get_commands_interactive (alias for extract_commands) from 021offshoot
from terminalai.command_extraction import extract_commands as get_commands_interactive
from terminalai.__init__ import __version__

def parse_args():
    """Parse command line arguments."""
    description_text = """TerminalAI: Your command-line AI assistant.
Ask questions or request commands in natural language.

-----------------------------------------------------------------------
MODES OF OPERATION & EXAMPLES:
-----------------------------------------------------------------------
1. Direct Query: Ask a question directly, get a response, then exit.
   Syntax: ai [flags] "query"
   Examples:
     ai "list files ending in .py"
     ai -v "explain the concept of inodes"
     ai -y "show current disk usage"
     ai -y -v "create a new directory called 'test_project' and enter it"

2. Single Interaction: Enter a prompt, get one response, then exit.
   Syntax: ai [flags]
   Examples:
     ai
       AI:(provider)> your question here
     ai -l
       AI:(provider)> explain git rebase in detail

3. Persistent Chat: Keep conversation history until 'exit'/'q'.
   Syntax: ai --chat [flags]  OR  ai -c [flags]
   Examples:
     ai --chat
     ai -c -v  (start chat in verbose mode)

-----------------------------------------------------------------------
COMMAND HANDLING:
-----------------------------------------------------------------------
- Confirmation:  Commands require [Y/n] confirmation before execution.
                 Risky commands (rm, sudo) require explicit 'y'.
- Stateful cmds: Commands like 'cd' or 'export' that change shell state
                 will prompt to copy to clipboard [Y/n].
- Integration:   If Shell Integration is installed (via 'ai setup'):
                   Stateful commands *only* in Direct Query mode (ai "...")
                   will execute directly in the shell after confirmation.
                   Interactive modes (ai, ai --chat) still use copy.

-----------------------------------------------------------------------
AVAILABLE FLAGS:
-----------------------------------------------------------------------
  [query]           Your question or request (used in Direct Query mode).
  -h, --help        Show this help message and exit.
  -y, --yes         Auto-confirm execution of non-risky commands.
                     Effective in Direct Query mode or with Shell Integration.
                     Example: ai -y "show disk usage"
  -v, --verbose     Request a more detailed response from the AI.
                     Example: ai -v "explain RAID levels"
                     Example (chat): ai -c -v
  -l, --long        Request a longer, more comprehensive response from AI.
                     Example: ai -l "explain git rebase workflow"
  --setup           Run the interactive setup wizard.
  --version         Show program's version number and exit.

-----------------------------------------------------------------------
AI FORMATTING EXPECTATIONS:
-----------------------------------------------------------------------
- Provide commands in separate ```bash code blocks.
- Keep explanations outside code blocks."""
    epilog_text = """For full configuration, run 'ai setup'.
Project: https://github.com/coaxialdolor/terminalai"""
    parser = argparse.ArgumentParser(
        description=description_text,
        epilog=epilog_text,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "query",
        nargs="?",
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        "-l", "--long",
        action="store_true",
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        "--setup",
        action="store_true",
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        "--eval-mode",
        action="store_true",
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        "--chat",
        action="store_true",
        help=argparse.SUPPRESS
    )

    return parser.parse_args()

def handle_commands(commands, auto_confirm=False, eval_mode=False, rich_to_stderr=False):
    """Handle extracted commands, prompting the user and executing if confirmed."""
    console = Console(file=sys.stderr if rich_to_stderr else None)

    # Detect shell integration
    shell_integration_active = os.environ.get("TERMINALAI_SHELL_INTEGRATION") == "1"

    if not commands:
        return

    n_commands = len(commands)

    # === Single Command Logic ===
    if n_commands == 1:
        command = commands[0]
        is_stateful = is_stateful_command(command)
        is_risky = is_risky_command(command)

        # A. Handle eval_mode pathway STRICTLY first.
        # Only enter this block if specifically running in eval_mode for shell function.
        if eval_mode:
            # A.1 Auto-confirm non-risky commands if -y is used IN eval_mode
            if auto_confirm and not is_risky:
                print(command) # Output command to stdout for shell function to eval
                sys.exit(0) # Exit successfully after printing command

            # A.2 Otherwise, prompt for confirmation (to stderr)
            if is_risky:
                confirm_msg, default_choice = "Execute? [y/N]: ", "n"
            else: # Not risky, but -y was not used
                confirm_msg, default_choice = "Execute? [Y/n]: ", "y"
            style = "yellow" if is_risky else "green"
            # Print prompt to stderr so it's visible but not captured by shell eval
            print(confirm_msg, end="", file=sys.stderr); sys.stderr.flush()
            choice = input().lower() or default_choice # Read choice from stdin

            if choice == "y":
                print(command) # Output command to stdout for shell function to eval
                sys.exit(0) # Exit successfully after printing command
            else:
                print("[Cancelled]", file=sys.stderr) # Notify user on stderr
                sys.exit(1) # Exit with error if cancelled IN eval_mode to signal failure

        # B. Handle NON-eval_mode pathway (covers interactive `ai` and `ai --chat`)
        # This block is only reached if eval_mode is False.
        elif is_stateful: # Check if the command is stateful
            # B.1 Prompt user to copy the stateful command
            prompt_text = (
                f"[STATEFUL COMMAND] '{command}' changes shell state. "
                "Copy to clipboard? [Y/n]: " # Standard clipboard prompt
            )
            console.print(Text(prompt_text, style="yellow bold"), end="")
            choice = input().lower()
            if choice != 'n': # Default to yes (copy)
                copy_to_clipboard(command)
                console.print("[green]Command copied to clipboard. Paste and run manually.[/green]")
            # We do NOT exit here in interactive mode; just return to the interactive loop
            # or let the main script exit if it was a single (non-chat) interaction.
            return

        else: # C. Handle NON-eval_mode and NON-stateful command
            # C.1 Auto-confirm non-risky if -y was used (only relevant if called non-interactively without eval)
            if auto_confirm and not is_risky:
                console.print(f"[green]Auto-executing: {command}[/green]")
                run_command(command)
                return

            # C.2 Regular confirmation prompt for direct execution
            if is_risky:
                confirm_msg, default_choice = "Execute? [y/N]: ", "n"
            else:
                confirm_msg, default_choice = "Execute? [Y/n]: ", "y"
            style = "yellow" if is_risky else "green"
            console.print(Text(confirm_msg, style=style), end="")
            choice = input().lower() or default_choice
            if choice == "y":
                run_command(command) # Execute using subprocess
            # We do NOT exit here in interactive mode; just return.
            return

    # === Multiple Command Logic ===
    else:
        cmd_list = []
        for i, cmd in enumerate(commands, 1):
            is_risky_cmd = is_risky_command(cmd)
            is_stateful_cmd = is_stateful_command(cmd)
            cmd_text = f"[cyan]{i}[/cyan]: [white]{cmd}[/white]"
            if is_risky_cmd:
                cmd_text += " [bold red][RISKY][/bold red]"
            if is_stateful_cmd:
                cmd_text += " [bold yellow][STATEFUL][/bold yellow]"
            cmd_list.append(cmd_text)
        console.print(Panel(
            "\n".join(cmd_list),
            title=f"Found {n_commands} commands",
            border_style="blue"
        ))
        console.print(Text("Enter command number, 'a' for all, or 'q' to quit: ", style="bold cyan"), end="")
        choice = input().lower()

        if choice == "q":
            return
        elif choice == "a":
            for cmd in commands:
                if is_stateful_command(cmd):
                    is_cmd_risky = is_risky_command(cmd)

                    if eval_mode or shell_integration_active:
                        # Always require extra confirmation for risky commands
                        if is_cmd_risky:
                            prompt_text = (
                                f"[RISKY][STATEFUL COMMAND] '{cmd}' is risky and changes "
                                "shell state. Execute? [y/N]: "
                            )
                            console.print(Text(prompt_text, style="red bold"), end="")
                            subchoice = input().lower()
                            if subchoice.lower() != "y":
                                console.print("[Cancelled]")
                                sys.exit(1)
                        else:
                            prompt_text = (
                                f"[STATEFUL COMMAND] '{cmd}' changes shell state. "
                                "Execute? [Y/n]: "
                            )
                            console.print(Text(prompt_text, style="yellow bold"), end="")
                            subchoice = input().lower()
                            if subchoice.lower() != "y":
                                console.print("[Cancelled]")
                                sys.exit(1)
                        print(cmd)
                        sys.exit(0)
                    else:
                        prompt_text = (
                            f"[STATEFUL COMMAND] '{cmd}' changes shell state. "
                            "Copy to clipboard? [Y/n]: "
                        )
                        console.print(Text(prompt_text, style="yellow bold"), end="")
                        subchoice = input().lower()
                        if subchoice.lower() != "n":
                            copy_to_clipboard(cmd)
                            console.print("[green]Command copied to clipboard. Paste and run manually.[/green]")
                else:
                    if is_risky_command(cmd):
                        console.print(Text(f"[RISKY] Execute risky command '{cmd}'? [y/N]: ", style="red bold"), end="")
                        subchoice = input().lower()
                        if subchoice != "y":
                            continue
                    run_command(cmd)
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(commands):
                cmd = commands[idx]
                if is_stateful_command(cmd):
                    is_cmd_risky = is_risky_command(cmd)

                    if eval_mode or shell_integration_active:
                        if is_cmd_risky:
                            prompt_text = (
                                f"[RISKY][STATEFUL COMMAND] '{cmd}' is risky and changes "
                                "shell state. Execute? [y/N]: "
                            )
                            console.print(Text(prompt_text, style="red bold"), end="")
                            subchoice = input().lower()
                            if subchoice.lower() != "y":
                                console.print("[Cancelled]")
                                sys.exit(1)
                        else:
                            prompt_text = (
                                f"[STATEFUL COMMAND] '{cmd}' changes shell state. "
                                "Execute? [Y/n]: "
                            )
                            console.print(Text(prompt_text, style="yellow bold"), end="")
                            subchoice = input().lower()
                            if subchoice.lower() != "y":
                                console.print("[Cancelled]")
                                sys.exit(1)
                        print(cmd)
                        sys.exit(0)
                    else:
                        prompt_text = (
                            f"[STATEFUL COMMAND] '{cmd}' changes shell state. "
                            "Copy to clipboard? [Y/n]: "
                        )
                        console.print(Text(prompt_text, style="yellow bold"), end="")
                        subchoice = input().lower()
                        if subchoice.lower() != "n":
                            copy_to_clipboard(cmd)
                            console.print("[green]Command copied to clipboard. Paste and run manually.[/green]")
                else:
                    run_command(cmd)
            else:
                console.print(f"[red]Invalid choice: {choice}[/red]")
            return

    # Single command logic
    command = commands[0]
    is_stateful = is_stateful_command(command)
    is_risky = is_risky_command(command)
    if eval_mode or shell_integration_active:
        if is_risky:
            confirm_msg = "Execute? [y/N]: "
            default_choice = "n"
        else:
            confirm_msg = "Execute? [Y/n]: "
            default_choice = "y"
        style = "yellow" if is_risky else "green"
        print(confirm_msg, end="", file=sys.stderr if rich_to_stderr else sys.stdout)
        (sys.stderr if rich_to_stderr else sys.stdout).flush()
        choice = input().lower()
        if not choice:
            choice = default_choice
        if choice == "y":
            print(command)
            sys.exit(0)
        else:
            print("[Cancelled]", file=sys.stderr if rich_to_stderr else sys.stdout)
            return  # Never sys.exit(1) on cancel
    if is_stateful:
        prompt_text = (
            f"[STATEFUL COMMAND] '{command}' changes shell state. "
            "To execute seamlessly, install the ai shell integration (see setup). "
            "Copy to clipboard instead? [Y/n]: "
        )
        console.print(Text(prompt_text, style="yellow bold"), end="")
        choice = input().lower()
        if choice != 'n':
            copy_to_clipboard(command)
            console.print("[green]Command copied to clipboard. Paste and run manually.[/green]")
        return
    confirm_msg = "Execute? [y/N]: " if is_risky else "Execute? [Y/n]: "
    default_choice = "n" if is_risky else "y"
    if auto_confirm and not is_risky:
        console.print(f"[green]Auto-executing: {command}[/green]")
        run_command(command)
        return
    style = "yellow" if is_risky else "green"
    console.print(Text(confirm_msg, style=style), end="")
    choice = input().lower()
    if not choice:
        choice = default_choice
    if choice == "y":
        run_command(command)
    else:
        console.print("[Cancelled]")
    return

def run_command(command):
    """Execute a shell command with error handling."""
    console = Console()

    if not command:
        return

    if not is_shell_command(command):
        console.print(f"[yellow]Warning: '{command}' doesn't look like a valid shell command.[/yellow]")
        console.print("[yellow]Execute anyway? [y/N]:[/yellow]", end=" ")
        choice = input().lower()
        if choice != "y":
            return

    console.print(Panel(f"[bold white]Executing: [/bold white][cyan]{command}[/cyan]",
                       border_style="green",
                       title="Command Execution",
                       title_align="left"))

    success = run_shell_command(command)
    if not success:
        console.print(f"[bold red]Command failed: {command}[/bold red]")

def interactive_mode(chat_mode=False):
    """Run TerminalAI in interactive mode. If chat_mode is True, stay in a loop."""
    console = Console()

    if chat_mode:
        console.print(Panel.fit(
            Text("TerminalAI AI Chat Mode: You are now chatting with the AI. Type 'exit' to quit.", style="bold magenta"),
            border_style="magenta"
        ))
        console.print("[dim]Type 'exit', 'quit', or 'q' to return to your shell.[/dim]")
    else:
        # Create the styled text for the panel
        panel_text = Text()
        panel_text.append("Terminal AI: ", style="bold cyan")
        panel_text.append("What is your question? ", style="white")
        panel_text.append("(Type ", style="yellow")
        panel_text.append("exit", style="bold red")
        panel_text.append(" or ", style="yellow")
        panel_text.append("q", style="bold red")
        panel_text.append(" to quit)", style="yellow")
        console.print(Panel.fit(
            panel_text,
            border_style="cyan" # Keep border cyan
        ))

    while True:
        # Add visual separation between interactions
        console.print("")
        provider_name = load_config().get("default_provider", "Unknown") # Get provider name
        prompt = Text()
        prompt.append("AI:", style="bold cyan")
        prompt.append("(", style="bold green")
        prompt.append(provider_name, style="bold green")
        prompt.append(")", style="bold green")
        prompt.append("> ", style="bold cyan")
        console.print(prompt, end="")
        query = input().strip()

        if query.lower() in ["exit", "quit", "q"]:
            console.print("[bold cyan]Goodbye![/bold cyan]")
            break

        if not query:
            continue

        system_context = get_system_context()

        provider = get_provider(load_config().get("default_provider", ""))
        if not provider:
            console.print("[bold red]No AI provider configured. Please run 'ai setup' first.[/bold red]")
            break

        try:
            # Show a thinking indicator
            console.print("[dim]Thinking...[/dim]")

            response = provider.generate_response(query, system_context, verbose=False)

            # Clear the thinking indicator with a visual separator
            console.print(Rule(style="dim"))

            print_ai_answer_with_rich(response)

            # Extract and handle commands from the response, limiting to max 3 commands
            # to avoid overwhelming the user in interactive mode
            commands = get_commands_interactive(response, max_commands=3)

            if commands:
                handle_commands(commands, auto_confirm=False)

        except SystemExit: # Allow SystemExit from handle_commands (eval mode) to pass through
            raise
        except (ValueError, TypeError, OSError, KeyboardInterrupt) as e:
            # Catch common user/AI errors
            console.print(f"[bold red]Error during processing: {str(e)}[/bold red]")
            import traceback
            traceback.print_exc()
        except Exception as e:
            # Catch-all for truly unexpected errors (should be rare)
            console.print(f"[bold red]Unexpected error: {str(e)}[/bold red]")
            import traceback
            traceback.print_exc()

        # If NOT in chat_mode, exit after the first interaction (successful or error)
        if not chat_mode:
            break # Break the while loop

    # If the loop was broken (only happens if not chat_mode), exit cleanly.
    sys.exit(0)

def setup_wizard():
    """Run the setup wizard to configure TerminalAI."""
    console = Console()

    logo = '''
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██║       █████╗ ██╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║      ██╔══██╗██║
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║      ███████║██║
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║      ██╔══██║██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗ ██║  ██║██║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═╝  ╚═╝╚═╝
'''
    while True:
        console.clear()
        console.print(logo, style="bold cyan")
        console.print("[bold magenta]TerminalAI Setup Menu:[/bold magenta]")
        menu_options = [
            "1. Set default provider",
            "2. See current system prompt",
            "3. Edit current system prompt",
            "4. Reset system prompt to default",
            "5. Setup API keys",
            "6. See current API keys",
            "7. Install ai shell integration",
            "8. Uninstall ai shell integration",
            "9. Check ai shell integration",
            "10. View quick setup guide",
            "11. About TerminalAI",
            "12. Exit"
        ]
        menu_info = {
            '1': ("Set which AI provider (OpenRouter, Gemini, Mistral, Ollama) "
                  "is used by default for all queries."),
            '2': "View the current system prompt that guides the AI's behavior.",
            '3': "Edit the system prompt to customize how the AI responds.",
            '4': "Reset the system prompt to the default recommended by TerminalAI.",
            '5': "Set/update API key/host for any provider.",
            '6': "List providers and their stored API key/host.",
            '7': ("Install the 'ai' shell function for seamless stateful command execution "
                  "(Only affects ai \"...\" mode)."),
            '8': "Uninstall the 'ai' shell function from your shell config.",
            '9': "Check if the 'ai' shell integration is installed in your shell config.",
            '10': "Display the quick setup guide to help you get started.",
            '11': "View information about TerminalAI, including version and links.",
            '12': "Exit the setup menu."
        }
        for opt in menu_options:
            num, desc = opt.split('.', 1)
            console.print(f"[bold yellow]{num}[/bold yellow].[white]{desc}[/white]")
        info_prompt = ("Type 'i' followed by a number (e.g., i1) "
                       "for more info about an option.")
        console.print(f"[dim]{info_prompt}[/dim]")
        choice = console.input("[bold green]Choose an action (1-12): [/bold green]").strip()
        config = load_config()
        if choice.startswith('i') and choice[1:].isdigit():
            info_num = choice[1:]
            if info_num in menu_info:
                info_text = menu_info[info_num]
                console.print(f"[bold cyan]Info for option {info_num}:[/bold cyan]")
                console.print(info_text)
            else:
                console.print("[red]No info available for that option.[/red]")
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '1':
            providers = list(config['providers'].keys())
            console.print("\n[bold]Available providers:[/bold]")
            for idx, p_item in enumerate(providers, 1):
                is_default = ""
                if p_item == config.get('default_provider'):
                    is_default = ' (default)'
                console.print(f"[bold yellow]{idx}[/bold yellow]. {p_item}{is_default}")
            sel_prompt = f"[bold green]Select provider (1-{len(providers)}): [/bold green]"
            sel = console.input(sel_prompt).strip()
            if sel.isdigit() and 1 <= int(sel) <= len(providers):
                selected_provider = providers[int(sel)-1]
                config['default_provider'] = selected_provider
                save_config(config)
                console.print(f"[bold green]Default provider set to "
                              f"{selected_provider}.[/bold green]")
            else:
                console.print("[red]Invalid selection.[/red]")
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '2':
            console.print("\n[bold]Current system prompt:[/bold]\n")
            console.print(get_system_prompt())
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '3':
            console.print("\n[bold]Current system prompt:[/bold]\n")
            console.print(config.get('system_prompt', ''))
            new_prompt_input = (
                "\n[bold green]Enter new system prompt "
                "(leave blank to cancel):\n[/bold green]"
            )
            new_prompt = console.input(new_prompt_input)
            if new_prompt.strip():
                config['system_prompt'] = new_prompt.strip()
                save_config(config)
                console.print(
                    "[bold green]System prompt updated.[/bold green]"
                )
            else:
                console.print("[yellow]No changes made.[/yellow]")
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '4':
            config['system_prompt'] = DEFAULT_SYSTEM_PROMPT
            save_config(config)
            console.print("[bold green]System prompt reset to default.[/bold green]")
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '5':
            providers = list(config['providers'].keys())
            console.print("\n[bold]Providers:[/bold]")
            for idx, p_item in enumerate(providers, 1):
                console.print(f"[bold yellow]{idx}[/bold yellow]. {p_item}")
            sel_prompt = (f"[bold green]Select provider to set API key/host "
                          f"(1-{len(providers)}): [/bold green]")
            sel = console.input(sel_prompt).strip()
            if sel.isdigit() and 1 <= int(sel) <= len(providers):
                pname = providers[int(sel)-1]
                if pname == 'ollama':
                    current = config['providers'][pname].get('host', '')
                    console.print(f"Current host: {current}")
                    ollama_host_prompt = (
                        "Enter new Ollama host (e.g., http://localhost:11434): "
                    )
                    new_host = console.input(ollama_host_prompt).strip()
                    if new_host:
                        config['providers'][pname]['host'] = new_host
                        save_config(config)
                        console.print(
                            "[bold green]Ollama host updated.[/bold green]"
                        )
                    else:
                        console.print("[yellow]No changes made.[/yellow]")
                else:
                    current = config['providers'][pname].get('api_key', '')
                    display_key = '(not set)' if not current else '[hidden]'
                    console.print(f"Current API key: {display_key}")
                    new_key_prompt = f"Enter new API key for {pname}: "
                    new_key = console.input(new_key_prompt).strip()
                    if new_key:
                        config['providers'][pname]['api_key'] = new_key
                        save_config(config)
                        console.print(
                            f"[bold green]API key for {pname} updated.[/bold green]"
                        )
                    else:
                        console.print("[yellow]No changes made.[/yellow]")
            else:
                console.print("[red]Invalid selection.[/red]")
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '6':
            providers = list(config['providers'].keys())
            console.print("\n[bold]Current API keys / hosts:[/bold]")
            for p_item in providers:
                if p_item == 'ollama':
                    val = config['providers'][p_item].get('host', '')
                    shown = val if val else '[not set]'
                else:
                    val = config['providers'][p_item].get('api_key', '')
                    shown = '[not set]' if not val else '[hidden]'
                console.print(f"[bold yellow]{p_item}:[/bold yellow] {shown}")
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '7':
            install_shell_integration()
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '8':
            uninstall_shell_integration()
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '9':
            check_shell_integration()
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '10':
            console.print("\n[bold cyan]Quick Setup Guide:[/bold cyan]\n")
            guide = """
[bold yellow]1. Installation[/bold yellow]

You have two options to install TerminalAI:

[bold green]Option A: Install from PyPI (Recommended)[/bold green]
    pip install coaxial-terminal-ai

[bold green]Option B: Install from source[/bold green]
    git clone https://github.com/coaxialdolor/terminalai.git
    cd terminalai
    pip install -e .

[bold yellow]2. Initial Configuration[/bold yellow]

In a terminal window, run:
    ai setup

• Enter [bold]5[/bold] to select "Setup API Keys"
• Select your preferred AI provider:
  - Mistral is recommended for its good performance and generous free tier limits
  - Ollama is ideal if you prefer locally hosted AI
  - You can also use OpenRouter or Gemini
• Enter the API key for your selected provider(s)
• Press Enter to return to the setup menu

[bold yellow]3. Set Default Provider[/bold yellow]

• At the setup menu, select [bold]1[/bold] to "Setup default provider"
• Choose a provider that you've saved an API key for
• Press Enter to return to the setup menu

[bold yellow]4. Understanding Stateful Command Execution[/bold yellow]

For commands like 'cd' or 'export' that change your shell's state, TerminalAI
will offer to copy the command to your clipboard. You can then paste and run it.

(Optional) Shell Integration:
• You can still install a shell integration via option [bold]7[/bold] in the setup menu.
  This is for advanced users who prefer a shell function for such commands.
  Note that the primary method is now copy-to-clipboard.

[bold yellow]5. Start Using TerminalAI[/bold yellow]
You're now ready to use TerminalAI! Here's how:

[bold green]Direct Query with Quotes[/bold green]
    ai "how do I find all text files in the current directory?"

[bold green]Interactive Mode[/bold green]
    ai
    AI: What is your question?
    : how do I find all text files in the current directory?

[bold green]Running Commands[/bold green]
• When TerminalAI suggests terminal commands, you'll be prompted:
  - For a single command: Enter Y to run or N to skip
  - For multiple commands: Enter the number of the command you want to run
  - For stateful (shell state-changing) commands, you'll be prompted to copy them
    to your clipboard to run manually.
"""
            console.print(guide)
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '11':
            console.print("\n[bold cyan]About TerminalAI:[/bold cyan]\n")
            console.print(f"[bold]Version:[/bold] {__version__}")
            console.print("[bold]GitHub:[/bold] https://github.com/coaxialdolor/terminalai")
            console.print("[bold]PyPI:[/bold] https://pypi.org/project/coaxial-terminal-ai/")
            console.print("\n[bold]Description:[/bold]")
            console.print(
                "TerminalAI is a command-line AI assistant designed to interpret user"
            )
            console.print(
                "requests, suggest relevant terminal commands, "
                "and execute them interactively."
            )
            console.print("\n[bold red]Disclaimer:[/bold red]")
            console.print(
                "This application is provided as-is without any warranties. "
                "Use at your own risk."
            )
            console.print(
                "The developers cannot be held responsible for any data loss, system damage,"
            )
            console.print(
                "or other issues that may occur from executing "
                "suggested commands."
            )
            console.input("[dim]Press Enter to continue...[/dim]")
        elif choice == '12':
            console.print(
                "[bold cyan]Exiting setup.[/bold cyan]"
            )
            break
        else:
            error_msg = (
                "Invalid choice. Please select a number from 1 to 12."
            )
            console.print(f"[red]{error_msg}[/red]")
            console.input("[dim]Press Enter to continue...[/dim]")
