import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.gui.main_window import MainWindow


def main() -> None:
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
