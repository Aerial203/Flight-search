import requests

# https://docs.google.com/spreadsheets/d/1NH437wOPQrpaj8veuKE0Ydbfsb6bqJ3Euo68LHEipoc/edit#gid=0

SHEET_ENDPOINT = "https://api.sheety.co/1eaaedb0bcf30cbb6613c5468d7b83ce/flightDeals/prices"


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEET_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_data(self):
        for city in self.destination_data:
            body = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            response = requests.put(url=f"{SHEET_ENDPOINT}/{city['id']}", json=body)
            print(response.text)

    def get_email(self):
        customer_endpoint = "https://api.sheety.co/1eaaedb0bcf30cbb6613c5468d7b83ce/flightDeals/users"
        response = requests.get(url=customer_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data