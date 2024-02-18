import os
from dotenv import load_dotenv
import datetime
import requests

load_dotenv()
BASE_URL = os.getenv("SHIP24_BASE_URL")
BAREAR_TOKEN = os.getenv("SHIP24_BAREAR_TOKEN")

class Ship24API:
    def __init__(self):
        self.api_key = BAREAR_TOKEN
        self.headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        self.base_url = BASE_URL

    def create_tracker(self, tracking_number):
        url = f"{self.base_url}/trackers/"

        payload = {
            "trackingNumber": tracking_number
        }

        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code != 200:
            return {}

        return response.json()

    def list_existing_trackers(self, page=1, limit=40):
        url = f"{self.base_url}/trackers/"
        query_params = {
            "page": page,
            "limit": limit
        }

        response = requests.get(url, params=query_params, headers=self.headers)

        if response.status_code != 200:
            return {}

        return response.json()

    def create_tracker_and_get_tracking_info(self, tracking_number):
        url = f"{self.base_url}/trackers/track/"
        payload = {
            "trackingNumber": tracking_number
        }
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code != 201:
            return {}

        return response.json()

    def get_existing_tracker(self, tracker_id):
        url = f"{self.base_url}/trackers/{tracker_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return {}

        return response.json()

    def update_existing_tracker(self, tracker_id, is_subscribed, courier_code):
        url = f"{self.base_url}/trackers/{tracker_id}/"
        payload = {
            "isSubscribed": is_subscribed,
            "courierCode": courier_code
        }
        response = requests.patch(url, json=payload, headers=self.headers)

        if response.status_code != 200:
            return {}

        return response.json()

    def get_tracking_results_by_tracking_number(self, tracking_number):
        url = f"{self.base_url}/trackers/search/{tracking_number}/results/"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return {}

        return response.json()
    
    def get_tracking_results_by_tracking_id(self, tracking_id):
        url = f"{self.base_url}/trackers/{tracking_id}/results/"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return {}

        return response.json()

    def get_status_milestone(self, tracker):
        return tracker['data']['trackings'][0]['shipment']['statusMilestone']
    
    def get_tracking_id(self, tracker):
        return tracker['data']['trackings'][0]['tracker']['trackerId']

    def get_delivery_date(self, tracker):
        # Search in the first event of the tracker
        events = tracker['data']['trackings'][0]['events']
        last_event = events[0]

        # Get the date from the datetime in format "YYYY-MM-DDTHH:MM:SS.000Z"
        delivery_date = last_event['datetime'] # "2024-02-16T12:09:00.000Z"
        
        # Return the delivery date in format "MM/DD/YYYY"
        delivery_date = datetime.datetime.strptime(delivery_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%m/%d/%Y")
        return delivery_date
