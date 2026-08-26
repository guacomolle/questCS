"""
Точка входа для запуска квеста.

Запускает Streamlit-приложение app.py и открывает его в браузере.
Достаточно выполнить:
    python main.py
(предварительно один раз установив зависимость: pip install streamlit)
"""

import subprocess
import sys
from pathlib import Path

if __name__ == '__main__':
    app_path = Path(__file__).resolve().parent / "app.py"
    # Запускаем streamlit тем же интерпретатором, из которого вызван main.py,
    # чтобы использовалось окружение (например, .venv) текущего проекта.
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])
