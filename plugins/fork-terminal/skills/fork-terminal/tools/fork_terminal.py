#!/usr/bin/env -S uv run
"""Fork a new terminal window with a command."""

import os
import platform
import re
import subprocess


def fork_terminal(command: str) -> str:
    """Open a new Terminal window and run the specified command."""
    system = platform.system()
    cwd = os.getcwd()

    if system == "Darwin":  # macOS
        # Escape double quotes in cwd for the shell
        escaped_cwd = cwd.replace('"', '\\"')
        # Build shell command using double quotes for cd
        shell_command = f'cd "{escaped_cwd}" && {command}'

        # Strategy: Convert single-quoted strings to use $'...' ANSI-C quoting
        # This allows newlines to be represented as \n escape sequences
        # which bash will interpret correctly without breaking the command
        #
        # We need to:
        # 1. Replace newlines with literal \n (for $'...' quoting to interpret)
        # 2. Escape single quotes within $'...' as \'
        # 3. Use $'...' instead of '...' for strings containing newlines

        def convert_single_quoted_string(match):
            """Convert '...' to $'...' with proper escaping."""
            content = match.group(1)
            # Escape backslashes first, then single quotes, then convert newlines
            escaped = (
                content
                .replace("\\", "\\\\")
                .replace("'", "\\'")
                .replace("\n", "\\n")
            )
            return f"$'{escaped}'"

        # Replace single-quoted strings that contain newlines
        converted_command = re.sub(
            r"'((?:[^'\\]|\\.)*?)'",
            lambda m: convert_single_quoted_string(m) if '\n' in m.group(1) else m.group(0),
            shell_command
        )

        # Escape for AppleScript: backslashes and double quotes
        escaped_shell_command = converted_command.replace("\\", "\\\\").replace('"', '\\"')

        try:
            result = subprocess.run(
                ["osascript", "-e", f'tell application "Terminal" to do script "{escaped_shell_command}"'],
                capture_output=True,
                text=True,
            )
            output = f"stdout: {result.stdout.strip()}\nstderr: {result.stderr.strip()}\nreturn_code: {result.returncode}"
            return output
        except Exception as e:
            return f"Error: {str(e)}"

    elif system == "Windows":
        # Use /d flag to change drives if necessary
        full_command = f'cd /d "{cwd}" && {command}'
        subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", full_command], shell=True)
        return "Windows terminal launched"

    else:  # Linux and others
        raise NotImplementedError(f"Platform {system} not supported")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        output = fork_terminal(" ".join(sys.argv[1:]))
        print(output)