from colorama import init, Fore, Back, Style
from datetime import datetime

init(autoreset=True)


class Logger:
    def __init__(self, filename="log.txt"):
        self.filename = filename

    def _log(self, message, level, fore_color, back_color):
        tag = f" {level.upper():<7} "
        colored_tag = f"{fore_color}{back_color}{tag}{Style.RESET_ALL}"

        # Print to console with colors
        print(f"{colored_tag} {message}")

        # Write plain to file with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} {tag} {message}\n"

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(log_line)

    def info(self, message):
        self._log(message, "INFO", Fore.WHITE, Back.BLUE)

    def warning(self, message):
        self._log(message, "WARN", Fore.BLACK, Back.YELLOW)

    def error(self, message):
        self._log(message, "ERROR", Fore.WHITE, Back.RED)

    def success(self, message):
        self._log(message, "SUCCESS", Fore.BLACK, Back.GREEN)

    def clear(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("")  # Overwrite with empty content


# Example usage
if __name__ == "__main__":
    log = Logger("my_log.txt")

    log.clear()

    log.info("Server started successfully.")
    log.success("Backup completed successfully.")
    log.warning("Disk space is getting low.")
    log.error("Failed to connect to database.")
