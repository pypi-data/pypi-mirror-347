import argparse
from pathlib import Path
from report_monaco.racing import RaceData


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Monaco 2018 Q1 lap‐time report"
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        required=True,
        help="the way to file (start.log, end.log, abbreviations.txt)"
    )
    parser.add_argument(
        "--driver", "-d",
        type=str,
        help="if True  print by driver"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--asc", action="store_true", help="sorting asc")
    group.add_argument("--desc", action="store_true", help="sorting desc")

    args = parser.parse_args()

    folder_path = Path(args.file)

    if not folder_path.exists():
        folder_path = Path(__file__).parent.parent / folder_path

    sort_order = "desc" if args.desc else "asc"

    try:
        RaceData().print_report(
            folder=folder_path,
            driver=args.driver,
            sort_order=sort_order
        )
    except FileNotFoundError as e:
        raise FileNotFoundError(f"[ERROR] {e}")
    except ValueError as e:
       raise ValueError(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
