from django.db import models
from django.contrib.auth import get_user_model

#from django.contrib.messages  import constants as messages


User = get_user_model()
# Create your models here.
#for items
class Product(models.Model):
    #item id by default
    slug= models.SlugField()
    item_shortname=models.CharField(max_length=50);
    item_id= models.IntegerField()
    heading= models.CharField(max_length=100)#item_name
    sellers=models.IntegerField()
    sellers_id=models.TextField()
    img= models.ImageField()
    description = models.TextField()
    price= models.IntegerField()
    offer= models.BooleanField(default=False)
    category=models.CharField(max_length=100,default='electronics')


class Persondetails(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    email= models.CharField(max_length=100)
    address = models.TextField()
    city=models.CharField(max_length=100)
    zipcode= models.IntegerField()
    state= models.CharField(max_length=50)
    country = models.CharField(max_length=50)



class Cart(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created= models.DateTimeField(auto_now_add=True)
    purchased= models.BooleanField(default=False)


    def __str__(self):
        return f'{self.quantity} of {self.item.heading}'

    # getting total price of a item
    def get_total(self):
        return self.item.price * self.quantity


    def get_quantity(self):
        return self.quantity





class Order(models.Model):
    orderitems= models.ManyToManyField(Cart)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add=True)
    



    def _str_(self):
       return self.user.first_name

    #total price of all items
    def get_totals(self):
        total=0
        for order_item in self.orderitems.all():
            total+= order_item.get_total()

        return total

    def get_items(self):
        items=0
        for item in self.orderitems.all():
            items+= item.get_quantity()

        return items

    def get_date(self):
        return self.created

class Ordered(models.Model):
    orderitems= models.ManyToManyField(Cart)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add=True)
