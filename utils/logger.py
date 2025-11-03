from datetime import datetime
import os

# Diretório do log
BASE_DIR = os.getcwd()
log_path = os.path.join(BASE_DIR, "log.txt")

# Tenta usar colorama, se não estiver, ignora cores
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        BLUE = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        WHITE = ''
        RESET = ''
    class Style:
        BRIGHT = ''
        NORMAL = ''

def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_header():
    """Cabeçalho insano do sistema"""
    print(Fore.BLUE + "\n" + "="*60)
    print(Fore.BLUE + f"{'SYNC ALOEE'.center(60)}")
    print(Fore.BLUE + f"{_timestamp().center(60)}")
    print(Fore.BLUE + "="*60 + Fore.RESET + "\n")

def log_info(message, status=None):
    """Imprime no console e grava no log"""
    timestamp = _timestamp()
    line = f"{timestamp} - {message}"

    # Prefixo e cor
    prefix = ""
    color = Fore.WHITE
    if status == "warning":
        prefix = "⚠ "
        color = Fore.YELLOW
    elif status == "error":
        prefix = "✖ "
        color = Fore.RED
    elif status == "info":
        color = Fore.GREEN

    print(color + prefix + line + Fore.RESET)

    # Grava no TXT
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def write_summary(produtos_total, produtos_inseridos, produtos_atualizados,
                  modelos_total, modelos_inseridos, modelos_atualizados):
    """Resumo final do dia com cores ajustadas"""
    separator = Fore.GREEN + "="*60 + Fore.RESET
    print("\n" + separator)
    print(Fore.BLUE + "RESUMO DA EXECUÇÃO".center(60) + Fore.RESET)
    print(Fore.GREEN + "-"*60 + Fore.RESET)

    # Linhas com título verde e valores em branco
    lines = [
        f"{Fore.GREEN}Produtos:{Fore.RESET} Total={Fore.WHITE}{produtos_total}{Fore.RESET}, Inseridos={Fore.WHITE}{produtos_inseridos}{Fore.RESET}, Atualizados={Fore.WHITE}{produtos_atualizados}{Fore.RESET}",
        f"{Fore.GREEN}Modelos :{Fore.RESET} Total={Fore.WHITE}{modelos_total}{Fore.RESET}, Inseridos={Fore.WHITE}{modelos_inseridos}{Fore.RESET}, Atualizados={Fore.WHITE}{modelos_atualizados}{Fore.RESET}"
    ]

    for line in lines:
        print(line)

    print(separator + "\n")

    # Grava no TXT sem cores
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n" + "="*50 + "\n")
        f.write(f"DATA/HORA DA EXECUÇÃO: {_timestamp()}\n")
        f.write(f"Produtos: Total={produtos_total}, Inseridos={produtos_inseridos}, Atualizados={produtos_atualizados}\n")
        f.write(f"Modelos : Total={modelos_total}, Inseridos={modelos_inseridos}, Atualizados={modelos_atualizados}\n")
        f.write("="*50 + "\n\n")
