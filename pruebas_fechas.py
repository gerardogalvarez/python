import datetime

timestamp = datetime.datetime(year=2016, month=12, day=2, hour=13, minute=26, second=49)
d = datetime.datetime.now()
# d = datetime.timedelta(seconds=1136)
# d = datetime.now()
print(d)
d += datetime.timedelta(seconds=12)

print(d)