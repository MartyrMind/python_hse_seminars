"""Создать воспроизводимые CSV с продажами маленькой кофейни."""

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Название, цена в рублях и обычный спрос за день.
MENU = (
    ("espresso", 180, 25),
    ("americano", 220, 45),
    ("cappuccino", 300, 60),
    ("latte", 320, 50),
)


def generate_data(output_dir: Path, *, seed: int, days: int, start_date: date) -> None:
    """Записать продажи и цены; при повторном запуске заменить эти два CSV."""
    if days <= 0:
        raise ValueError("days must be positive")
    # Проверяем диапазон дат до создания файлов.
    last_date = start_date + timedelta(days=days - 1)
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "sales.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["date", *(name for name, _, _ in MENU)])
        for offset in range(days):
            day = start_date + timedelta(days=offset)
            weekend_factor = 1.3 if day.weekday() >= 5 else 1.0
            daily_factor = rng.uniform(0.65, 1.35)
            quantities = [
                0
                if rng.random() < 0.04
                else max(0, round(rng.gauss(demand, demand * 0.15) * daily_factor * weekend_factor))
                for _, _, demand in MENU
            ]
            writer.writerow([day.isoformat(), *quantities])

    with (output_dir / "prices.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["drink", "price"])
        writer.writerows((name, price) for name, price, _ in MENU)

    print(f"Созданы sales.csv и prices.csv: {output_dir.resolve()}")
    print(f"Дней: {days}; период: {start_date} — {last_date}; seed: {seed}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42, help="seed случайных чисел (42)")
    parser.add_argument("--days", type=int, default=28, help="число дней продаж (28)")
    parser.add_argument(
        "--start-date",
        type=date.fromisoformat,
        default=date(2026, 10, 5),
        help="первый день в формате YYYY-MM-DD (2026-10-05)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "data",
        help="каталог CSV (по умолчанию data рядом со скриптом)",
    )
    args = parser.parse_args()
    if args.days <= 0:
        parser.error("--days must be positive")
    try:
        args.start_date + timedelta(days=args.days - 1)
    except OverflowError:
        parser.error("date range is too large")
    generate_data(args.output_dir, seed=args.seed, days=args.days, start_date=args.start_date)


if __name__ == "__main__":
    main()
