from emapp.station.models import StationModel
import pandas as pd
import numpy as np
import requests
import json

def writedatatotable(row, df, index):
        name = row['Name_of_Station']
        stationManager = row['Receiving_Station_Manager']
        stationCode = row['Name_of_Station']
        contact = row['Station_Manager_Mobile_Number_and_Emergency_number']
        latitude = row['Latitude']
        longitude = row['Longitude']
        email = row['Station_manager_E_mail_ID']

        q = StationModel(name = name,
                        stationManager = stationManager,
                        stationCode = stationCode,
                        contact = contact,
                        latitude  = latitude,
                        longitude = longitude,
                        email = email)
        q.save()

def main():
        filename = 'STD-IandFeeder-details-Contact-Details-5.xlsx' # Replace with filename
        df = pd.read_excel(filename)
        index_limit = 9179
        for index, row in df.iterrows():
                if index > index_limit:
                        break
                try:
                        writedatatotable(row, df, index)
                except Exception as e:
                        print(e)

main()
