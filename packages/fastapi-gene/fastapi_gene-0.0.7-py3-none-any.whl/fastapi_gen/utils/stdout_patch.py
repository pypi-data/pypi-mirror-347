import sys

from rich.console import Console

original_stdout = sys.stdout
rich_console = Console(file=original_stdout)


class RichStdout:
    def write(self, text: str):
        if text.strip():
            rich_console.print(text, end="")
        return len(text)

    def flush(self):
        original_stdout.flush()
