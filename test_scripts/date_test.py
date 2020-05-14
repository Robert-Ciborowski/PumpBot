from datetime import datetime

now = datetime.now() # current date and time

year = now.strftime("%Y")
print("year:", year)

month = now.strftime("%m")
print("month:", month)

day = now.strftime("%d")
print("day:", day)

time = now.strftime("%H:%M:%S")
print("time:", time)

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",date_time)

date_time = now.strftime("%Y-%m-%d")
print("date and time:",date_time)

# import pandas as pd
#
# cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
#         'Price': [22000,25000,27000,35000]
#         }
#
# df = pd.DataFrame(cars, columns= ['Brand', 'Price'])
#
# df.to_csv ('export_dataframe.csv', index = False, header=True)
# df2 = pd.read_csv('export_dataframe.csv')
#
# print (df2)
