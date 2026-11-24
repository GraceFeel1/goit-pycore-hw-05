import sys
from collections import Counter


def parse_log_line(line: str) -> dict:
    parts = line.strip().split(" ", 3)

    if len(parts) < 4:
        raise ValueError("Неправильний формат рядка логу.")

    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2].upper(),
        "message": parts[3],
    }


def load_logs(file_path: str) -> list:
    logs = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    try:
                        logs.append(parse_log_line(line))
                    except ValueError as error:
                        print(f"Помилка формату: {error}")

    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
    except PermissionError:
        print(f"Немає доступу до файлу: {file_path}")
    except OSError as error:
        print(f"Помилка читання файлу: {error}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    level = level.upper()

    return list(
        filter(
            lambda log: log["level"] == level,
            logs
        )
    )


def count_logs_by_level(logs: list) -> dict:
    return dict(Counter(log["level"] for log in logs))


def display_log_counts(counts: dict):
    print("\nРівень логування | Кількість")
    print("-----------------|----------")

    for level, count in counts.items():
        print(f"{level:<16} | {count}")


def main():
    if len(sys.argv) < 2:
        print("Використання: python task_3.py <шлях_до_логу> [рівень]")
        return

    file_path = sys.argv[1]
    logs = load_logs(file_path)

    if not logs:
        print("Логи не знайдені.")
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) >= 3:
        level = sys.argv[2].upper()
        filtered_logs = filter_logs_by_level(logs, level)

        print(f"\nДеталі логів для рівня '{level}':")

        if not filtered_logs:
            print("Записів такого рівня не знайдено.")
            return

        for log in filtered_logs:
            print(
                f"{log['date']} {log['time']} - "
                f"{log['message']}"
            )


if __name__ == "__main__":
    main()