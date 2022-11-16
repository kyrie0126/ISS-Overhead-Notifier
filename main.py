import requests
from datetime import datetime
import smtplib
import time

# ---------------------------- Constants ----------------------------
MY_LAT = 40.712776  # for NY City, use 'latlong.net' to find any city's coordinates
MY_LONG = -74.005974
MY_GMAIL = ""  # your email - you'll need to change smtp_ssl param if not a gmail acct
MY_PASS = ""  # app-specific password since gmail doesn't allow less secure apps anymore

# ---------------------------- API Calls ----------------------------
# ISS location
iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
data = iss_response.json()
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# today's sunrise/sunset
sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
sun_response.raise_for_status()
data = sun_response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
hour_now = time_now.hour

# ---------------------------- Functions ----------------------------


# ISS proximity with 5 degree margin of error
def is_close():
    if iss_latitude-5 <= MY_LAT <= iss_latitude+5 and iss_latitude-5 <= MY_LONG <= iss_longitude+5:
        return True
    else:
        return False


# check that it's dark outside
def is_dark():
    if hour_now < sunrise or sunset < hour_now:
        return True
    else:
        return False


# ---------------------------- Run Program ----------------------------
# if ISS is close, and it's dark, email myself a notification
while True:
    time.sleep(60)  # refresh every 60 sec
    if is_close() and is_dark():
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(MY_GMAIL, MY_PASS)
            connection.sendmail(
                from_addr=MY_GMAIL,
                to_addrs=MY_GMAIL,
                msg="Subject:ISS Is Above You\n\nLook up now!"
            )
