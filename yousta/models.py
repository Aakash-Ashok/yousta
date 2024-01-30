from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):

    phone=models.CharField(max_length=100,unique=True)
    address=models.CharField(max_length=200)


class Category(models.Model):

    name=models.CharField(max_length=200,unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Cloths(models.Model):
    name=models.CharField(max_length=200)
    options=(
        ("linen","linen"),
        ("cotton","cotton"),
        ("satin","satin"),
        ("nylon","nylon"),
        ("polyster","polyster"),
        ("silk","silk")
    )
    material=models.CharField(max_length=200,choices=options,default="cotton")
    image=models.ImageField(upload_to="images")
    brand=models.CharField(max_length=200)
    category=models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)

    @property
    def varients(self):
        qs=self.clothvarients_set.all()
        return qs
    
    def __str__(self):
        return self.name
    
    @property
    def reviews(self):
        qs=self.reviews_set.all()
        return qs
    
    @property
    def avg_rating(self):
        rating=self.reviews_set.all().values_list("rating",flat=True)
        return sum(rating)/len(rating) if rating else 0
       

class ClothVarients(models.Model):
    price=models.PositiveIntegerField()
    color=models.CharField(max_length=100)
    options=(
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL"),
        ("XXl","XXL")
    )

    size=models.CharField(max_length=200,choices=options,default="M")
    cloth=models.ForeignKey(Cloths,on_delete=models.CASCADE)

    def __str__(self):
        return self.cloth.name
    
    @property
    def offers(self):
       today=date.today()
       qs=self.offers_set.all()
       qs=qs.filter(due_date__gt=today)
       return qs



class Offers(models.Model):
    clothvarient=models.ForeignKey(ClothVarients,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    start_date=models.DateTimeField()
    due_date=models.DateTimeField()


class Carts(models.Model):
    clothvarient=models.ForeignKey(ClothVarients,on_delete=models.DO_NOTHING)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("in-cart","in-cart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )

    status=models.CharField(max_length=200,choices=options,default="in-cart")
    date=models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    clothvarient=models.ForeignKey(ClothVarients,on_delete=models.CASCADE)
    options=(
      
        ("order-placed","order-placed"),
        ("cancelled","cancelled"),
        ("dispatced","dispatched"),
        ("in-transit","in-transit"),
        ("delivered","delivered")
    )
    status=models.CharField(max_length=200,choices=options,default="order-placed")
    orderd_date=models.DateTimeField(auto_now_add=True)
    expected_date=models.DateField(null=True)
    address=models.CharField(max_length=200)

from django.core.validators import MinValueValidator,MaxValueValidator

class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cloth=models.ForeignKey(Cloths,null=True,on_delete=models.SET_NULL)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=300)



    


    





