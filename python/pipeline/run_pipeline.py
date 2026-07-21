"""
SkyFlow Complete ETL Pipeline
"""

# =====================================================
# GENERATORS
# =====================================================

from python.generators.airport_generator import generate_airport_data
from python.generators.aircraft_generator import generate_aircraft
from python.generators.route_generator import generate_routes
from python.generators.passenger_generator import generate_passengers
from python.generators.flight_generator import generate_flights
from python.generators.booking_generator import generate_bookings
from python.generators.payment_generator import generate_payments

# =====================================================
# VALIDATORS
# =====================================================

from python.validators.airport_validator import validate_airports
from python.validators.aircraft_validator import validate_aircraft
from python.validators.route_validator import validate_routes
from python.validators.passenger_validator import validate_passengers
from python.validators.flight_validator import validate_flights
from python.validators.booking_validator import validate_bookings
from python.validators.payment_validator import validate_payments

# =====================================================
# LOADERS
# =====================================================

from python.loaders.load_airport import load_airport
from python.loaders.load_aircraft import load_aircraft
from python.loaders.load_route import load_route
from python.loaders.load_passenger import load_passenger
from python.loaders.load_flight import load_flight
from python.loaders.load_booking import load_booking
from python.loaders.load_payment import load_payment


def run_pipeline():

    print("\n" + "=" * 70)
    print("         SKYFLOW ENTERPRISE AIRLINE DATA PLATFORM")
    print("                COMPLETE ETL PIPELINE")
    print("=" * 70)

    # =====================================================
    # STEP 1 : GENERATE DATA
    # =====================================================

    print("\nGenerating Airport Data...")
    generate_airport_data()

    print("Generating Aircraft Data...")
    generate_aircraft()

    print("Generating Route Data...")
    generate_routes()

    print("Generating Passenger Data...")
    generate_passengers()

    print("Generating Flight Data...")
    generate_flights()

    print("Generating Booking Data...")
    generate_bookings()

    print("Generating Payment Data...")
    generate_payments()

    # =====================================================
    # STEP 2 : VALIDATE DATA
    # =====================================================

    print("\nValidating Airport Data...")
    validate_airports()

    print("Validating Aircraft Data...")
    validate_aircraft()

    print("Validating Route Data...")
    validate_routes()

    print("Validating Passenger Data...")
    validate_passengers()

    print("Validating Flight Data...")
    validate_flights()

    print("Validating Booking Data...")
    validate_bookings()

    print("Validating Payment Data...")
    validate_payments()

    # =====================================================
    # STEP 3 : LOAD INTO MYSQL
    # =====================================================

    print("\nLoading Airport...")
    load_airport()

    print("Loading Aircraft...")
    load_aircraft()

    print("Loading Route...")
    load_route()

    print("Loading Passenger...")
    load_passenger()

    print("Loading Flight...")
    load_flight()

    print("Loading Booking...")
    load_booking()

    print("Loading Payment...")
    load_payment()

    print("\n" + "=" * 70)
    print("     SKYFLOW ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()