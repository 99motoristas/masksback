import csv
from mask.models import Driver
import hashlib

Driver.objects.all().delete()
i = 0
with open('./upload.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        i=i+1
        if(i%1000 == 0):
            print(i)
        _, created = Driver.objects.get_or_create(
                hashed_phone=row[1],
                hashed_cpf=row[0],
                date=row[3],
                city=row[2]
                )


print("fuck")
