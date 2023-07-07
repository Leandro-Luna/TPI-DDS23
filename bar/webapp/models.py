from django.db import models
from datetime import datetime
# Create your models here.

from django.db import models

class ReportingManager(models.Manager):
    def get_name(self):
        return self.model._meta.model_name
    def order_set(self, income):
        incomplete = {row['categoria']: row['total'] for row in income}
        categorias = self.get_categories()
        
        final = []
        for cat in categorias:
            if cat in list(incomplete.keys()):
                final.append(float(incomplete[cat]))
            else:
                final.append(0)
        return final
    def _get_income_by_category(self, qs):
        income = qs.annotate(categoria=models.F(f'{self.get_name()}line__product__category'),
                             total_linea=models.F(f'{self.get_name()}line__quantity')*models.F(f'{self.get_name()}line__unit_price'))\
                    .values('categoria')\
                    .annotate(total=models.Sum('total_linea'))
        return self.order_set(income)
    
    def get_categories(self):
        return list(map(lambda x:x['categoria'],(Product.objects.annotate(categoria=models.F('category'))\
            .values('categoria').order_by('categoria').distinct())))
    
    def get_daily_stats(self, date):
        filters = {f"{self.get_name()}_date__year":date.year,
                   f"{self.get_name()}_date__month":date.month,
                   f"{self.get_name()}_date__day":date.day}
        sales = self.filter(**filters)
        return self._get_income_by_category(sales)
    
    def get_weekly_stats(self, date):
        filters = {f"{self.get_name()}_date__year":date.year,
                   f"{self.get_name()}_date__week":date.isocalendar()[1] }
        sales = self.filter(**filters)
        return self._get_income_by_category(sales)

    def get_monthly_stats(self, date):
        filters = {f"{self.get_name()}_date__year":date.year,
                   f"{self.get_name()}_date__month":date.month}
        sales = self.filter(**filters)
        return self._get_income_by_category(sales)

    def get_anual_stats(self, year):
        filter = {f"{self.get_name()}_date__year":year}
        sales = self.filter(**filter)
        return self._get_income_by_category(sales)
        
class Product(models.Model):
    # Django automaticamente agrega id si no es especificado
    name = models.CharField(max_length=20)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True, null=False)

class Purchase(models.Model):
    purchase_date = models.DateTimeField()
    provider = models.CharField(max_length=50, null=True)

    objects = models.Manager()
    reporting = ReportingManager()

class PurchaseLine(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

class Sale(models.Model):
    sale_date = models.DateTimeField(default=datetime.now)
    client = models.CharField(max_length=50, null=True)
    
    objects = models.Manager()
    reporting = ReportingManager()

class SaleLine(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

income = Sale.reporting
expenses = Purchase.reporting