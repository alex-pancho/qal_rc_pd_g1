from datetime import (
    datetime,
    timedelta,
    timezone
)
# datetime.datetime

its_day = datetime.today()
print(its_day)

mydatetime = datetime.fromtimestamp(1706551390)
print(mydatetime, type(mydatetime))

mydatetime = datetime.fromtimestamp(0)
print(mydatetime, type(mydatetime))

ordinal_day = 365 # Порядковий номер дня
dt = datetime.fromordinal(ordinal_day)
print(dt)

day_number = datetime.today().toordinal()
print(f'Порядковий номер сьогоднішнього дня: {day_number}')

ordinal_day = 737777 # Порядковий номер дня
dt = datetime.fromordinal(ordinal_day)
print(dt)

tz = timezone.utc
current_datetime = datetime.now(tz)
print("Поточна дата і час:", current_datetime)
current_datetime = datetime.now()
print("Поточна дата і час:", current_datetime)
its_day = datetime.today()
print("today дата і час:", its_day)

incoming_date = "Aug 24, 1991"
pattern = "%b %d, %Y"
dt_incoming_date = datetime.strptime(incoming_date, pattern)
print(dt_incoming_date)

some_day_1 = "Sep 20, 2022"
some_day_1_1 = "Dec 21, 2022"
some_day_2 = "Dec 21 2022"
some_day_3 = "May 5, 2025"

for day in [some_day_1, some_day_1_1, some_day_2, some_day_3]:
    try:
        print(datetime.strptime(day, pattern))
    except ValueError:
        print(f"wrong time format: {day}, expect {pattern}")

pattern_output = "Now year %Y %m month and day is %d time is: %H:%M"
good_time_output = datetime.strftime(dt_incoming_date, pattern_output)
print(good_time_output)

dt_01 = "19:45:23"  # Germany
dt_02 = "20:00:22"
dt_03 = "20:00:27"
dt_04 = "20:45:23"  # Kyiv

def to_hour(time_in_hour:str):
    return datetime.strptime(time_in_hour, "%H:%M:%S")

new_dt = map(to_hour, [dt_01, dt_02, dt_03, dt_04])
dt_01_alex, dt_02_nata, dt_03_jena, dt_04_rost = new_dt
print(dt_01_alex, dt_02_nata, dt_03_jena, dt_04_rost)


diff_time = dt_02_nata - dt_01_alex
print("Diff", diff_time, type(diff_time))
if dt_02_nata - dt_01_alex > timedelta(minutes=15):
    print("FAIL")
else:
    print("pass")

some_delta = timedelta(days=999999)
print(current_datetime + some_delta)

minus_td = dt_01_alex - dt_02_nata
print(minus_td, type(minus_td), timedelta(minutes=-15))


print("*"*88)
d = datetime.today()
print(d)
print(d.isocalendar())
print(d.isoformat())
print(d.isoweekday())
print(d.timetuple())
print(d.weekday())

dd = d.replace(year=2021, day=12)
print(dd)


td = timedelta(days=5, hours=3, minutes=30)
print(td)


big_td = timedelta(seconds=1_000_000)
print(big_td)


big_td = timedelta(seconds=1_000_000_000)
print(big_td)
print(11574/365)
