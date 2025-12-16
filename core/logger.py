# core/logger.py
from datetime import datetime
import os
import sys

def get_base_dir():
    # Quando for .exe
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    # Quando for script normal
    return os.path.dirname(os.path.abspath(sys.argv[0]))

BASE_DIR = get_base_dir()
log_path = os.path.join(BASE_DIR, "log.txt")

# colorama opcional
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except Exception:
    class Fore:
        BLUE = ""
        GREEN = ""
        YELLOW = ""
        RED = ""
        WHITE = ""
        RESET = ""
    class Style:
        BRIGHT = ""
        NORMAL = ""

def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_header():
    print(Fore.BLUE + "\n" + "=" * 60)
    print(Fore.BLUE + f"{'SYNC ALOEE'.center(60)}")
    print(Fore.BLUE + f"{_timestamp().center(60)}")
    print(Fore.BLUE + "=" * 60 + Fore.RESET + "\n")

def log_info(message, status="info"):
    ts = _timestamp()
    line = f"{ts} - {message}"
    color = Fore.WHITE
    prefix = ""
    if status == "warning":
        prefix = "⚠ "
        color = Fore.YELLOW
    elif status == "error":
        prefix = "✖ "
        color = Fore.RED
    elif status == "info":
        color = Fore.GREEN

    try:
        print(color + prefix + line + Fore.RESET)
    except Exception:
        print(line)

    # grava em arquivo
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def write_summary(metrics: dict):
    """
    metrics example:
    {
      "Produtos": {"total": 100, "inseridos": 30, "atualizados": 70, "inativados": 2},
      ...
    }
    """
    separator = Fore.GREEN + "=" * 60 + Fore.RESET
    print("\n" + separator)
    print(Fore.BLUE + "RESUMO DA EXECUÇÃO".center(60) + Fore.RESET)
    print(Fore.GREEN + "-" * 60 + Fore.RESET)

    for nome, dados in metrics.items():
        total = dados.get("total", 0)
        ins = dados.get("inseridos", 0)
        upd = dados.get("atualizados", 0)
        ina = dados.get("inativados", 0)
        print(
            f"{Fore.GREEN}{nome}:{Fore.RESET} Total={Fore.WHITE}{total}{Fore.RESET}, "
            f"Inseridos={Fore.WHITE}{ins}{Fore.RESET}, Atualizados={Fore.WHITE}{upd}{Fore.RESET}, "
            f"Inativados={Fore.WHITE}{ina}{Fore.RESET}"
        )

    print(separator + "\n")

    # grava texto simples
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"DATA/HORA DA EXECUÇÃO: {_timestamp()}\n")
            for nome, dados in metrics.items():
                f.write(
                    f"{nome}: Total={dados.get('total',0)}, "
                    f"Inseridos={dados.get('inseridos',0)}, "
                    f"Atualizados={dados.get('atualizados',0)}, "
                    f"Inativados={dados.get('inativados',0)}\n"
                )
            f.write("=" * 50 + "\n\n")
    except Exception:
        pass
