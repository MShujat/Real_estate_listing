from background_task import background
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint as pp
from .models import RealEstateItem


@background(schedule=2)
def realestate_gs_marker(realstate_object):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "/home/muhammadshujathussain/personal/user_realestate/user_listing_proj/real_estate_listing/shujat_updated_gsheets.json", scope)
    client = gspread.authorize(creds)
    realstate_object = RealEstateItem.objects.get(id=realstate_object['id'])
    sheet = client.open("RealEstateData").sheet1
    insert_row = [realstate_object.created_by.email, realstate_object.description,
                  str(realstate_object.price), realstate_object.address]
    sheet.insert_row(insert_row)
    data = sheet.get_all_records()
    pp(data)
