from webapp.models import Product, Sale, SaleLine
from datetime import date, timedelta, datetime
import random
    
def random_date(start_date=datetime(2023,1,1), end_date=datetime(2023,7,30)):
    num_days = (end_date - start_date).days  
    rand_days = random.randint(1, num_days)
    rand_date = start_date + timedelta(days=rand_days, hours=random.randint(1,20), seconds=random.randint(1,60), minutes=random.randint(1,60))     
    return rand_date

def random_product():   
    product = Product.objects.get(id=random.randint(1,100))
    return product


def random_quantity(model):
    random_quantity = int(model.stock * random.uniform(0.02, 0.2))
    return random_quantity

print(Sale.reporting.get_name())
# get_daily_stats(date(2023,1,29))