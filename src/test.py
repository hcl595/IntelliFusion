import data
from data import Models
a = Models.get(Models.id == 1)
print(a.url)
