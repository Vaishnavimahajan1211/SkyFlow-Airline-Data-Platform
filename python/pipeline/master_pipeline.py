import subprocess
import sys
from pathlib import Path


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PYTHON = sys.executable


# ============================================================
# PIPELINE STEPS
# ============================================================

PIPELINE_STEPS = [
    (
        "Passenger Dimension",
        "python/spark/passenger_gold.py"
    ),
    (
        "Airport Dimension",
        "python/spark/airport_gold.py"
    ),
    (
        "Aircraft Dimension",
        "python/spark/aircraft_gold.py"
    ),
    (
        "Route Dimension",
        "python/spark/route_gold.py"
    ),
    (
        "Booking Fact",
        "python/spark/booking_fact.py"
    ),
    (
        "Flight Fact",
        "python/spark/flight_fact.py"
    ),
    (
        "Payment Fact",
        "python/spark/payment_fact.py"
    ),
    (
        "Data Quality Checks",
        "python/quality/data_quality_checks.py"
    ),
]


# ============================================================
# RUN PIPELINE STEP
# ============================================================

def run_step(step_number, step_name, script_path):

    print("\n")
    print("=" * 75)
    print(f"STEP {step_number}: {step_name}")
    print("=" * 75)

    full_script_path = PROJECT_ROOT / script_path

    if not full_script_path.exists():
        print(f"ERROR: Script not found:")
        print(full_script_path)
        return False

    try:

        result = subprocess.run(
    [PYTHON, "-m", script_path.replace("/", ".").replace(".py", "")],
    cwd=PROJECT_ROOT,
    check=False
)

        if result.returncode == 0:

            print("\n" + "-" * 75)
            print(f"SUCCESS: {step_name}")
            print("-" * 75)

            return True

        else:

            print("\n" + "-" * 75)
            print(f"FAILED: {step_name}")
            print(f"Exit Code: {result.returncode}")
            print("-" * 75)

            return False

    except Exception as error:

        print("\n" + "-" * 75)
        print(f"ERROR while running {step_name}")
        print(error)
        print("-" * 75)

        return False


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    print("\n")
    print("=" * 75)
    print("SKYFLOW - ENTERPRISE DATA PLATFORM")
    print("MASTER PYSPARK PIPELINE")
    print("=" * 75)

    print(f"\nProject Root:")
    print(PROJECT_ROOT)

    print(f"\nTotal Pipeline Steps: {len(PIPELINE_STEPS)}")

    successful_steps = 0

    # --------------------------------------------------------
    # Execute pipeline
    # --------------------------------------------------------

    for step_number, (step_name, script_path) in enumerate(
        PIPELINE_STEPS,
        start=1
    ):

        success = run_step(
            step_number,
            step_name,
            script_path
        )

        if not success:

            print("\n")
            print("=" * 75)
            print("PIPELINE FAILED")
            print("=" * 75)

            print(
                f"\nPipeline stopped at STEP {step_number}: "
                f"{step_name}"
            )

            print("\nPlease fix the above error before continuing.")

            sys.exit(1)

        successful_steps += 1

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("\n")
    print("=" * 75)
    print("SKYFLOW PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 75)

    print(
        f"\nSuccessful Steps: "
        f"{successful_steps}/{len(PIPELINE_STEPS)}"
    )

    print("\nPipeline Flow:")
    print("Raw Data")
    print("    ↓")
    print("Silver Layer")
    print("    ↓")
    print("Gold Dimensions")
    print("    ↓")
    print("Gold Facts")
    print("    ↓")
    print("Data Quality Checks")
    print("    ↓")
    print("PIPELINE SUCCESS")

    print("\nSkyFlow Master Pipeline is READY.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()