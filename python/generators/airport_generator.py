"""
Airport Generator
SkyFlow Enterprise Airline Data Platform
"""

import pandas as pd
from pathlib import Path

from python.config.config import RAW_FOLDER

AIRPORTS = [

    {
        "airport_code": "DEL",
        "airport_name": "Indira Gandhi International Airport",
        "city": "Delhi",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

    {
        "airport_code": "BOM",
        "airport_name": "Chhatrapati Shivaji Maharaj International Airport",
        "city": "Mumbai",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

    {
        "airport_code": "BLR",
        "airport_name": "Kempegowda International Airport",
        "city": "Bengaluru",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

    {
        "airport_code": "MAA",
        "airport_name": "Chennai International Airport",
        "city": "Chennai",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

    {
        "airport_code": "CCU",
        "airport_name": "Netaji Subhas Chandra Bose International Airport",
        "city": "Kolkata",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

    {
        "airport_code": "HYD",
        "airport_name": "Rajiv Gandhi International Airport",
        "city": "Hyderabad",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

    {
        "airport_code": "AMD",
        "airport_name": "Sardar Vallabhbhai Patel International Airport",
        "city": "Ahmedabad",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

    {
        "airport_code": "COK",
        "airport_name": "Cochin International Airport",
        "city": "Kochi",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

    {
        "airport_code": "GOI",
        "airport_name": "Goa International Airport",
        "city": "Goa",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

    {
        "airport_code": "PNQ",
        "airport_name": "Pune International Airport",
        "city": "Pune",
        "country": "India",
        "timezone": "Asia/Kolkata"
    },

        {
        "airport_code": "JFK",
        "airport_name": "John F. Kennedy International Airport",
        "city": "New York",
        "country": "USA",
        "timezone": "America/New_York"
    },

    {
        "airport_code": "LAX",
        "airport_name": "Los Angeles International Airport",
        "city": "Los Angeles",
        "country": "USA",
        "timezone": "America/Los_Angeles"
    },

    {
        "airport_code": "ORD",
        "airport_name": "O'Hare International Airport",
        "city": "Chicago",
        "country": "USA",
        "timezone": "America/Chicago"
    },

    {
        "airport_code": "ATL",
        "airport_name": "Hartsfield-Jackson Atlanta International Airport",
        "city": "Atlanta",
        "country": "USA",
        "timezone": "America/New_York"
    },

    {
        "airport_code": "DFW",
        "airport_name": "Dallas/Fort Worth International Airport",
        "city": "Dallas",
        "country": "USA",
        "timezone": "America/Chicago"
    },

    {
        "airport_code": "SFO",
        "airport_name": "San Francisco International Airport",
        "city": "San Francisco",
        "country": "USA",
        "timezone": "America/Los_Angeles"
    },

    {
        "airport_code": "SEA",
        "airport_name": "Seattle-Tacoma International Airport",
        "city": "Seattle",
        "country": "USA",
        "timezone": "America/Los_Angeles"
    },

    {
        "airport_code": "MIA",
        "airport_name": "Miami International Airport",
        "city": "Miami",
        "country": "USA",
        "timezone": "America/New_York"
    },

    {
        "airport_code": "LAS",
        "airport_name": "Harry Reid International Airport",
        "city": "Las Vegas",
        "country": "USA",
        "timezone": "America/Los_Angeles"
    },

    {
        "airport_code": "BOS",
        "airport_name": "Logan International Airport",
        "city": "Boston",
        "country": "USA",
        "timezone": "America/New_York"
    },

        {
        "airport_code": "LHR",
        "airport_name": "Heathrow Airport",
        "city": "London",
        "country": "United Kingdom",
        "timezone": "Europe/London"
    },

    {
        "airport_code": "LGW",
        "airport_name": "Gatwick Airport",
        "city": "London",
        "country": "United Kingdom",
        "timezone": "Europe/London"
    },

    {
        "airport_code": "MAN",
        "airport_name": "Manchester Airport",
        "city": "Manchester",
        "country": "United Kingdom",
        "timezone": "Europe/London"
    },

    {
        "airport_code": "EDI",
        "airport_name": "Edinburgh Airport",
        "city": "Edinburgh",
        "country": "United Kingdom",
        "timezone": "Europe/London"
    },

    {
        "airport_code": "BHX",
        "airport_name": "Birmingham Airport",
        "city": "Birmingham",
        "country": "United Kingdom",
        "timezone": "Europe/London"
    },

        {
        "airport_code": "DXB",
        "airport_name": "Dubai International Airport",
        "city": "Dubai",
        "country": "UAE",
        "timezone": "Asia/Dubai"
    },

    {
        "airport_code": "DWC",
        "airport_name": "Al Maktoum International Airport",
        "city": "Dubai",
        "country": "UAE",
        "timezone": "Asia/Dubai"
    },

    {
        "airport_code": "AUH",
        "airport_name": "Zayed International Airport",
        "city": "Abu Dhabi",
        "country": "UAE",
        "timezone": "Asia/Dubai"
    },

    {
        "airport_code": "SHJ",
        "airport_name": "Sharjah International Airport",
        "city": "Sharjah",
        "country": "UAE",
        "timezone": "Asia/Dubai"
    },

    {
        "airport_code": "RKT",
        "airport_name": "Ras Al Khaimah International Airport",
        "city": "Ras Al Khaimah",
        "country": "UAE",
        "timezone": "Asia/Dubai"
    },

        {
        "airport_code": "FRA",
        "airport_name": "Frankfurt Airport",
        "city": "Frankfurt",
        "country": "Germany",
        "timezone": "Europe/Berlin"
    },

    {
        "airport_code": "MUC",
        "airport_name": "Munich Airport",
        "city": "Munich",
        "country": "Germany",
        "timezone": "Europe/Berlin"
    },

    {
        "airport_code": "BER",
        "airport_name": "Berlin Brandenburg Airport",
        "city": "Berlin",
        "country": "Germany",
        "timezone": "Europe/Berlin"
    },

    {
        "airport_code": "HAM",
        "airport_name": "Hamburg Airport",
        "city": "Hamburg",
        "country": "Germany",
        "timezone": "Europe/Berlin"
    },

        {
        "airport_code": "CDG",
        "airport_name": "Charles de Gaulle Airport",
        "city": "Paris",
        "country": "France",
        "timezone": "Europe/Paris"
    },

    {
        "airport_code": "ORY",
        "airport_name": "Paris Orly Airport",
        "city": "Paris",
        "country": "France",
        "timezone": "Europe/Paris"
    },

    {
        "airport_code": "NCE",
        "airport_name": "Nice Côte d'Azur Airport",
        "city": "Nice",
        "country": "France",
        "timezone": "Europe/Paris"
    },

    {
        "airport_code": "LYS",
        "airport_name": "Lyon-Saint Exupéry Airport",
        "city": "Lyon",
        "country": "France",
        "timezone": "Europe/Paris"
    },

        {
        "airport_code": "HND",
        "airport_name": "Haneda Airport",
        "city": "Tokyo",
        "country": "Japan",
        "timezone": "Asia/Tokyo"
    },

    {
        "airport_code": "NRT",
        "airport_name": "Narita International Airport",
        "city": "Tokyo",
        "country": "Japan",
        "timezone": "Asia/Tokyo"
    },

    {
        "airport_code": "KIX",
        "airport_name": "Kansai International Airport",
        "city": "Osaka",
        "country": "Japan",
        "timezone": "Asia/Tokyo"
    },

    {
        "airport_code": "CTS",
        "airport_name": "New Chitose Airport",
        "city": "Sapporo",
        "country": "Japan",
        "timezone": "Asia/Tokyo"
    },

        {
        "airport_code": "SIN",
        "airport_name": "Singapore Changi Airport",
        "city": "Singapore",
        "country": "Singapore",
        "timezone": "Asia/Singapore"
    },

    {
        "airport_code": "XSP",
        "airport_name": "Seletar Airport",
        "city": "Singapore",
        "country": "Singapore",
        "timezone": "Asia/Singapore"
    },

        {
        "airport_code": "SYD",
        "airport_name": "Sydney Kingsford Smith Airport",
        "city": "Sydney",
        "country": "Australia",
        "timezone": "Australia/Sydney"
    },

    {
        "airport_code": "MEL",
        "airport_name": "Melbourne Airport",
        "city": "Melbourne",
        "country": "Australia",
        "timezone": "Australia/Melbourne"
    },

    {
        "airport_code": "BNE",
        "airport_name": "Brisbane Airport",
        "city": "Brisbane",
        "country": "Australia",
        "timezone": "Australia/Brisbane"
    },

        {
        "airport_code": "YYZ",
        "airport_name": "Toronto Pearson International Airport",
        "city": "Toronto",
        "country": "Canada",
        "timezone": "America/Toronto"
    },

    {
        "airport_code": "YVR",
        "airport_name": "Vancouver International Airport",
        "city": "Vancouver",
        "country": "Canada",
        "timezone": "America/Vancouver"
    },

    {
        "airport_code": "YUL",
        "airport_name": "Montréal–Trudeau International Airport",
        "city": "Montreal",
        "country": "Canada",
        "timezone": "America/Toronto"
    }



]

def generate_airport_data():

    df = pd.DataFrame(AIRPORTS)

    output_file = RAW_FOLDER / "airport.csv"

    df.to_csv(output_file, index=False)

    print(f"Airport data generated successfully: {output_file}")


if __name__ == "__main__":

    generate_airport_data()