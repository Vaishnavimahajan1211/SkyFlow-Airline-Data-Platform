import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD_FOLDER = PROJECT_ROOT / "data" / "gold"


# ============================================================
# EXPECTED GOLD TABLES
# ============================================================

EXPECTED_TABLES = {
    "dim_passenger": 1000,
    "dim_airport": 50,
    "dim_aircraft": 50,
    "dim_route": 100,
    "fact_booking": 5000,
    "fact_flight": 200,
    "fact_payment": 5000,
}


# ============================================================
# GLOBAL RESULT TRACKING
# ============================================================

total_checks = 0
passed_checks = 0
failed_checks = 0


def check(condition, message):
    """Print PASS/FAIL and update counters."""

    global total_checks, passed_checks, failed_checks

    total_checks += 1

    if condition:
        passed_checks += 1
        print(f"PASS  | {message}")
    else:
        failed_checks += 1
        print(f"FAIL  | {message}")


# ============================================================
# LOAD GOLD DATA
# ============================================================

def load_gold_table(table_name):
    """Load the first CSV file from a Gold table folder."""

    table_folder = GOLD_FOLDER / table_name

    if not table_folder.exists():
        check(False, f"{table_name} folder exists")
        return None

    csv_files = list(table_folder.glob("part-*.csv"))

    if not csv_files:
        check(False, f"{table_name} contains CSV data")
        return None

    try:
        df = pd.read_csv(csv_files[0])

        check(
            True,
            f"{table_name} loaded successfully ({len(df)} records)"
        )

        return df

    except Exception as e:
        check(False, f"{table_name} could not be loaded: {e}")
        return None


# ============================================================
# ROW COUNT CHECKS
# ============================================================

def check_row_counts(tables):

    print("\n" + "=" * 70)
    print("ROW COUNT CHECKS")
    print("=" * 70)

    for table_name, expected_count in EXPECTED_TABLES.items():

        df = tables.get(table_name)

        if df is None:
            continue

        actual_count = len(df)

        check(
            actual_count == expected_count,
            f"{table_name}: expected {expected_count}, found {actual_count}"
        )


# ============================================================
# PRIMARY KEY CHECKS
# ============================================================

def check_primary_keys(tables):

    print("\n" + "=" * 70)
    print("PRIMARY KEY CHECKS")
    print("=" * 70)

    primary_keys = {
        "dim_passenger": "passenger_id",
        "dim_airport": "airport_code",
        "dim_aircraft": "aircraft_id",
        "dim_route": "route_id",
        "fact_booking": "booking_id",
        "fact_flight": "flight_id",
        "fact_payment": "payment_id",
    }

    for table_name, primary_key in primary_keys.items():

        df = tables.get(table_name)

        if df is None:
            continue

        # Column exists
        check(
            primary_key in df.columns,
            f"{table_name}: {primary_key} column exists"
        )

        if primary_key not in df.columns:
            continue

        # Null check
        null_count = df[primary_key].isna().sum()

        check(
            null_count == 0,
            f"{table_name}: {primary_key} has no NULL values"
        )

        # Duplicate check
        duplicate_count = df[primary_key].duplicated().sum()

        check(
            duplicate_count == 0,
            f"{table_name}: {primary_key} has no duplicate values"
        )


# ============================================================
# FOREIGN KEY CHECKS
# ============================================================

def check_foreign_keys(tables):

    print("\n" + "=" * 70)
    print("FOREIGN KEY CHECKS")
    print("=" * 70)

    # --------------------------------------------------------
    # Booking -> Passenger
    # --------------------------------------------------------

    booking = tables.get("fact_booking")
    passenger = tables.get("dim_passenger")

    if booking is not None and passenger is not None:

        if "passenger_id" in booking.columns and \
           "passenger_id" in passenger.columns:

            valid_ids = set(
                passenger["passenger_id"].dropna()
            )

            invalid_ids = booking[
                ~booking["passenger_id"].isin(valid_ids)
            ]

            check(
                len(invalid_ids) == 0,
                f"fact_booking -> dim_passenger: "
                f"{len(invalid_ids)} invalid passenger IDs"
            )

    # --------------------------------------------------------
    # Booking -> Flight
    # --------------------------------------------------------

    flight = tables.get("fact_flight")

    if booking is not None and flight is not None:

        if "flight_id" in booking.columns and \
           "flight_id" in flight.columns:

            valid_ids = set(
                flight["flight_id"].dropna()
            )

            invalid_ids = booking[
                ~booking["flight_id"].isin(valid_ids)
            ]

            check(
                len(invalid_ids) == 0,
                f"fact_booking -> fact_flight: "
                f"{len(invalid_ids)} invalid flight IDs"
            )

    # --------------------------------------------------------
    # Payment -> Booking
    # --------------------------------------------------------

    payment = tables.get("fact_payment")

    if payment is not None and booking is not None:

        if "booking_id" in payment.columns and \
           "booking_id" in booking.columns:

            valid_ids = set(
                booking["booking_id"].dropna()
            )

            invalid_ids = payment[
                ~payment["booking_id"].isin(valid_ids)
            ]

            check(
                len(invalid_ids) == 0,
                f"fact_payment -> fact_booking: "
                f"{len(invalid_ids)} invalid booking IDs"
            )


# ============================================================
# BUSINESS RULE CHECKS
# ============================================================

def check_business_rules(tables):

    print("\n" + "=" * 70)
    print("BUSINESS RULE CHECKS")
    print("=" * 70)

    # --------------------------------------------------------
    # Booking Amount Checks
    # --------------------------------------------------------

    booking = tables.get("fact_booking")

    if booking is not None:

        for column in [
            "ticket_price",
            "tax",
            "discount",
            "final_amount"
        ]:

            if column in booking.columns:

                negative_count = (
                    booking[column] < 0
                ).sum()

                check(
                    negative_count == 0,
                    f"fact_booking: {column} has no negative values"
                )

        # ----------------------------------------------------
        # Final Amount Consistency
        # ----------------------------------------------------

        required_columns = {
            "ticket_price",
            "tax",
            "discount",
            "final_amount"
        }

        if required_columns.issubset(booking.columns):

            calculated_amount = (
                booking["ticket_price"]
                + booking["tax"]
                - booking["discount"]
            )

            difference = (
                calculated_amount
                - booking["final_amount"]
            ).abs()

            inconsistent_count = (
                difference > 0.01
            ).sum()

            check(
                inconsistent_count == 0,
                f"fact_booking: final_amount calculation "
                f"has {inconsistent_count} inconsistencies"
            )

    # --------------------------------------------------------
    # Flight Checks
    # --------------------------------------------------------

    flight = tables.get("fact_flight")

    if flight is not None:

        if "delay_minutes" in flight.columns:

            negative_delays = (
                flight["delay_minutes"] < 0
            ).sum()

            check(
                negative_delays == 0,
                f"fact_flight: delay_minutes has "
                f"{negative_delays} negative values"
            )

    # --------------------------------------------------------
    # Payment Checks
    # --------------------------------------------------------

    payment = tables.get("fact_payment")

    if payment is not None:

        if "amount" in payment.columns:

            negative_amounts = (
                payment["amount"] < 0
            ).sum()

            check(
                negative_amounts == 0,
                f"fact_payment: amount has "
                f"{negative_amounts} negative values"
            )


# ============================================================
# REQUIRED COLUMN CHECKS
# ============================================================

def check_required_columns(tables):

    print("\n" + "=" * 70)
    print("REQUIRED COLUMN CHECKS")
    print("=" * 70)

    required_columns = {

        "dim_passenger": [
            "passenger_id",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "email",
            "phone",
            "passport_number",
            "nationality",
        ],

        "dim_airport": [
            "airport_code",
            "airport_name",
            "city",
            "country",
            "timezone",
        ],

        "dim_aircraft": [
            "aircraft_id",
            "aircraft_code",
            "manufacturer",
            "model",
            "capacity",
            "manufacturing_year",
            "status",
        ],

        "dim_route": [
            "route_id",
            "source_airport",
            "destination_airport",
            "route_type",
            "distance_km",
            "duration_minutes",
            "fuel_estimate_liters",
        ],

        "fact_booking": [
            "booking_id",
            "passenger_id",
            "flight_id",
            "booking_date",
            "seat_class",
            "booking_status",
            "ticket_price",
            "tax",
            "discount",
            "final_amount",
            "payment_status",
        ],

        "fact_flight": [
            "flight_id",
            "flight_number",
            "route_id",
            "aircraft_id",
            "departure_datetime",
            "arrival_datetime",
            "flight_status",
            "terminal",
            "gate_number",
            "delay_minutes",
        ],

        "fact_payment": [
            "payment_id",
            "booking_id",
            "payment_date",
            "payment_method",
            "payment_status",
            "amount",
        ],
    }

    for table_name, columns in required_columns.items():

        df = tables.get(table_name)

        if df is None:
            continue

        missing_columns = [
            column
            for column in columns
            if column not in df.columns
        ]

        check(
            len(missing_columns) == 0,
            f"{table_name}: all required columns exist"
            + (
                f" | Missing: {missing_columns}"
                if missing_columns
                else ""
            )
        )


# ============================================================
# FINAL SUMMARY
# ============================================================

def print_summary():

    print("\n" + "=" * 70)
    print("DATA QUALITY SUMMARY")
    print("=" * 70)

    print(f"Total Checks : {total_checks}")
    print(f"Passed       : {passed_checks}")
    print(f"Failed       : {failed_checks}")

    if failed_checks == 0:

        print("\nSTATUS: DATA QUALITY PASSED")
        print("All Gold layer quality checks are successful.")

    else:

        print("\nSTATUS: DATA QUALITY FAILED")
        print("Please fix the failed checks before moving forward.")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("SKYFLOW - DATA QUALITY CHECK")
    print("=" * 70)

    print(f"\nGold Folder: {GOLD_FOLDER}")

    # --------------------------------------------------------
    # Load all Gold tables
    # --------------------------------------------------------

    tables = {}

    print("\n" + "=" * 70)
    print("LOADING GOLD TABLES")
    print("=" * 70)

    for table_name in EXPECTED_TABLES:

        tables[table_name] = load_gold_table(table_name)

    # --------------------------------------------------------
    # Run checks
    # --------------------------------------------------------

    check_required_columns(tables)

    check_row_counts(tables)

    check_primary_keys(tables)

    check_foreign_keys(tables)

    check_business_rules(tables)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print_summary()

    # Exit with error code if quality checks failed
    if failed_checks > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()