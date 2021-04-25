import requests
from flight_data import FlightData
from pprint import pprint

TEQUILA_API_KEY = "7siWVmOj8x1hvSKwO9KUR40KKk6DsL-V"
TEQUILA_END_POINT = "https://tequila-api.kiwi.com"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.headers = {
            "apikey": TEQUILA_API_KEY,
        }

    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_END_POINT}/locations/query"
        query = {
            "term": city_name,
            "location_types": "airport"
        }
        response = requests.get(url=location_endpoint, params=query, headers=self.headers)
        result = response.json()["locations"]
        code = result[0]["city"]["code"]
        return code

    def search_flight(self, from_city_code, to_city_code, from_data, to_date):
        search_endpoint = f"{TEQUILA_END_POINT}/v2/search"
        parameter = {
            "fly_from": from_city_code,
            "fly_to": to_city_code,
            "date_from": from_data.strftime("%d/%m/%Y"),
            "date_to": to_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "cur": "GBP",
        }
        response = requests.get(url=search_endpoint, headers=self.headers, params=parameter)
        try:
            data = response.json()["data"][0]
        except IndexError:
            parameter["max_stopovers"] = 1
            response = requests.get(
                url=search_endpoint,
                headers=self.headers,
                params=parameter
            )
            try:
                data = response.json()["data"][0]
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data['route'][0]['cityFrom'],
                    origin_airport=data['route'][0]['flyFrom'],
                    destination_city=data['route'][1]['cityTo'],
                    destination_airport=data['route'][1]['flyTo'],
                    out_date=data['route'][0]['local_departure'].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_over=1,
                    via_city=data['route'][1]['cityFrom']
                )
                return flight_data
            except IndexError:
                print(f"No flight from the {from_city_code}-{to_city_code}")
                return None
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            # print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data