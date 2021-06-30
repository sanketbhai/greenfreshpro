from django.db import models


# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50,default='null')

class Adress(models.Model):
    street = models.CharField(max_length=50)
    room_no = models.CharField(max_length=50)
    pincode=models.IntegerField()
    cusid=models.ForeignKey(Customer,on_delete=models.CASCADE)
    @property
    def adress(self):
        return self.street+','+str(self.room_no)+','+str(self.pincode)

class Product(models.Model):
    name= models.CharField(max_length=50,unique=True)
    cate = models.CharField(max_length=50)
    prise=models.IntegerField()
    img=models.ImageField(upload_to="media/app/img")

    
class Cart(models.Model):
    prod= models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    cusid=models.ForeignKey(Customer,on_delete=models.CASCADE)
    qty=models.IntegerField()
    @property
    def total(self):
    	return self.qty * self.prod.prise


class Order(models.Model):
    id=models.CharField(primary_key=True,max_length=1000)
    adress=models.ForeignKey(Adress,on_delete=models.CASCADE)
    


class Prod_orderd(models.Model):
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    prod= models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    
    qty=models.IntegerField()
    @property
    def total(self):
    	return self.qty * self.prod.prise



