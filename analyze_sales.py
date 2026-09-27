from pathlib import Path

import pandas as pd


def main() -> None:
    sales = pd.read_csv(Path(__file__).with_name("sales.csv"))
    sales["revenue"] = sales["units"] * sales["price"]
    print(sales)
    print(f"\nTotal revenue: ${sales['revenue'].sum():.2f}")


if __name__ == "__main__":
    main()
