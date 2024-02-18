import os
import datetime
from dotenv import load_dotenv
from integrations.google.sheets import GoogleSheetsAPI
from integrations.ship24.api import Ship24API
from catalogs import ShippingStatus, Ship24MilestoneStatus, SHIP24_AND_OWN_STATUS_DICT

load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

today = datetime.date.today()
month = today.strftime('%B').lower()
month = month[:3].upper()

RANGE = f'{month}!AG:AO'

def main():
    google_sheets = GoogleSheetsAPI('credentials.json', SPREADSHEET_ID, RANGE)
    shippings = google_sheets.get_values()
    headers = shippings[0]
    shippings = shippings[1:]

    ship24 = Ship24API()

    for shipping in shippings:

        if len(headers) != len(shipping):
            # add empty values to match the length of the headers
            shipping.extend([''] * (len(headers) - len(shipping)))

        # If the shipping is already delivered, we don't need to update it
        if shipping[headers.index('Estatus')] == ShippingStatus.DELIVERED.value:
            continue
        
        # If the shipping doesn't have a guide, we can't track it
        shipping_guide = shipping[headers.index('Guia')]

        if not shipping_guide:
            continue

        # If the shipping doesn't have a Ship24 ID, we need to create a tracker
        if not shipping[headers.index('Ship24 ID')]:
            tracker = ship24.create_tracker_and_get_tracking_info(shipping_guide)

            if not tracker:
                continue
            
            tracking_id = ship24.get_tracking_id(tracker)            
            shipping[headers.index('Ship24 ID')] = tracking_id

            status_milestone = ship24.get_status_milestone(tracker)
            status = SHIP24_AND_OWN_STATUS_DICT.get(status_milestone, "")
            shipping[headers.index('Estatus')] = status

            # If the shipping is delivered, we need to update the delivery date
            if status_milestone == Ship24MilestoneStatus.DELIVERED.value:
                delivery_date = ship24.get_delivery_date(tracker)
                shipping[headers.index('Fecha de entrega')] = delivery_date

            continue

        # If the shipping has a Ship24 ID, we need to update the tracker
        tracking_id = shipping[headers.index('Ship24 ID')]
        tracker = ship24.get_tracking_results_by_tracking_id(tracking_id)

        if not tracker:
            continue

        status_milestone = ship24.get_status_milestone(tracker)
        status = SHIP24_AND_OWN_STATUS_DICT.get(status_milestone, "")
        shipping[headers.index('Estatus')] = status

        # If the shipping is delivered, we need to update the delivery date
        if status_milestone == Ship24MilestoneStatus.DELIVERED.value:
            delivery_date = ship24.get_delivery_date(tracker)
            shipping[headers.index('Fecha de Entrega')] = delivery_date

    google_sheets.update_values([headers] + shippings)

main()
