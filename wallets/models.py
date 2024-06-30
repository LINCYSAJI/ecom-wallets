from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save

class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.name


class Color(models.Model):

    name = models.CharField(max_length=100, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.name



class Brand(models.Model):

    name = models.CharField(max_length=100, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.name
    
class Tag(models.Model):

    name=models.CharField(max_length=200)

    def __str__(self):

        return self.name

class Product(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField(null=True, blank=True)#blank true for accept null value for form , null true for accept null value in db 

    color_object = models.ManyToManyField(Color)

    category_object = models.ForeignKey(Category, on_delete=models.CASCADE)

    brand_object = models.ForeignKey(Brand, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='product_images', null=True, blank=True, default='product_images/default.jpg')

    price = models.PositiveIntegerField()

    tag_object=models.ManyToManyField(Tag)
    
    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.title
    


class Basket(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE,related_name="cart")

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.owner.username
    
    @property
    def cart_item_count(self):
        
        return self.cartitems.filter(is_order_placed=False).count()
    
    @property
    def cart_total(self):
        
        basket_items=self.cartitems.filter(is_order_placed=False)
        
        total_amount=0
        
        if basket_items:
        
            for bi in basket_items:
                
                total_amount+=bi.total_amount # basketitem total amount
            
        return total_amount
            
            
    

class BasketItem(models.Model):

    basket_object = models.ForeignKey(Basket, on_delete=models.CASCADE,related_name="cartitems")

    product_object = models.ForeignKey(Product, on_delete=models.CASCADE)

    color_object = models.ForeignKey(Color, on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(default=1)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    is_order_placed=models.BooleanField(default=False)
    
    @property
    def total_amount(self):
        
        return self.product_object.price*self.quantity


class Order(models.Model):

    user_object = models.ForeignKey(
                                        User,
                                        on_delete=models.CASCADE, 
                                        related_name='myorders'
                                    )

    basket_item_objects = models.ManyToManyField(BasketItem)

    delivery_address = models.CharField(max_length=250)

    phone = models.CharField(max_length=12)

    pin=models.CharField(max_length=10,null=True)

    email = models.CharField(max_length=100)

    pay_options = (
        ('online', 'online'),
        ('cod', 'cod')
    )

    payment_mode = models.CharField(
                                        max_length=100, 
                                        choices=pay_options, 
                                        default='cod'
                                    )

    order_id = models.CharField(max_length=200, null=True)

    is_paid = models.BooleanField(default=False)

    order_status = (
        ('order_confirmed', 'Order confirmed'),
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),

    )

    status = models.CharField(
                                max_length=200, 
                                choices=order_status, 
                                default='order_confirmed'
                            )

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    
    @property
    def sub_total(self):
        
        basket_items=self.basket_item_objects.all()
        
        total=0
        
        if basket_items:
            
            for bi in basket_items:
                
                total+=bi.total_amount
                
        return total
    
# automatically created basket object when user object is

    
def create_basket(sender,instance,created,**kwargs):
    
    if created:
        
        Basket.objects.create(owner=instance) # create basket,owner doesn't accept default value. instance contain user_object
        
post_save.connect(sender=User,receiver=create_basket)

#to create admin level user

# ====> python manage.py createsuperuser

