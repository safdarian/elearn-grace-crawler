import re
import jdatetime

am_pm_map = {"صبح": "AM", "عصر": "PM"}
persian_months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", 
                          "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
persian_weekdays = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]

def parse_persian_date(persian_date):
    if not persian_date:
        return persian_date
    if persian_date == "-":
        return None
    persian_date = persian_date.replace("،", "")
    persian_date = re.sub(rf"{"|".join(persian_weekdays)}", "", persian_date)
    persian_date = re.sub(rf"({"|".join(persian_months)})", lambda x: str(persian_months.index(x.group(1)) + 1), persian_date)    
    persian_date = persian_date.replace("عصر", "PM").replace("صبح", "AM")
    day = persian_date.split()[0].strip()
    month = persian_date.split()[1].strip()
    year = persian_date.split()[2].strip()
    time = persian_date.split()[3].strip()
    am_pm = persian_date.split()[4].strip()
    if am_pm == "PM":
        if int(time.split(":")[0]) < 12:
            time = time.split(":")
            time = f"{int(time[0]) + 12}:{time[1]}"
    elif am_pm == "AM":
        if int(time.split(":")[0]) == 12:
            time = time.split(":")
            time = f"{int(time[0]) - 12}:{time[1]}"
    jdatetime_object = jdatetime.datetime.strptime(f"{year}-{month}-{day} {time}", "%Y-%m-%d %H:%M")    
    return jdatetime_object