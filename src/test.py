import data
from data import Models

print(list(Models.select()))

for m in Models.select():
    print(m.name)