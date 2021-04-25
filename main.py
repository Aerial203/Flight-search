# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()
sheet_data = data_manager.get_destination_data()

ORIGIN_CITY_IATA = "LON"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_data()

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=180)

for destination in sheet_data:
    flight = flight_search.search_flight(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        tomorrow,
        six_months_from_today)
    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:
        user_data = data_manager.get_email()
        emails = [row["email"] for row in user_data]
        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}" \
               f".{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

        message = f"Low price alert! Only £{flight.price} to fly from "\
                  f"{flight.origin_city}-{flight.origin_airport} to "\
                  f"{flight.destination_city}-{flight.destination_airport}, "\
                  f"from {flight.out_date} to {flight.return_date}."

        if flight.stop_over > 0:
            message += f"Flight has {flight.stop_over} stop over, via {flight.via_city}"

        notification_manager.send_sms(message)
        notification_manager.send_email(message=message, receiver_email=emails, link=link)

