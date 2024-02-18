from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class GoogleSheetsAPI:
    def __init__(self, credentials_file, spreadsheet_id, range_name):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self.credentials = self.get_credentials()
        self.service = self.get_service()
        self.sheet = self.service.spreadsheets()
        self.values = self.get_values()


    def get_credentials(self):
        return Credentials.from_service_account_file(self.credentials_file)
    
    def get_service(self):
        return build('sheets', 'v4', credentials=self.credentials)
    
    def get_values(self):
        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id, range=self.range_name).execute()
        return result.get('values', [])
    
    def update_values(self, data):
        body = {
            'values': data
        }
        result = self.sheet.values().update(spreadsheetId=self.spreadsheet_id, range=self.range_name, valueInputOption='RAW', body=body).execute()
        return result.get('updatedCells')
    
    def get_columns(self, columns):
        headers = self.values[0]
        data = self.values[1:]
        return [[row[headers.index(column)] for column in columns] for row in data]
    
    def update_column(self, column, data):
        headers = self.values[0]
        data = self.values[1:]
        column_index = headers.index(column)
        for i, row in enumerate(data):
            row[column_index] = data[i]
        self.update_values(data)
    
    def update_row(self, row, data):
        headers = self.values[0]
        data = self.values[1:]
        for i, header in enumerate(headers):
            data[row][i] = data[i]
        self.update_values(data)
