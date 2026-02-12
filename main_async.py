"""
Verzija main.py s konkurentnim izvršavanjem background zadataka.

-autosave i realtime statistika
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.gui.async_window import MainWindowWithAsync


def main() -> None:
    app = MainWindowWithAsync()
    app.mainloop()


if __name__ == "__main__":
    main()
