from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'โปรไฟล์'
        verbose_name_plural = 'โปรไฟล์'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{ self.user } { self.user.first_name } { self.user.last_name }  {self.phone_number}'

class New(models.Model):
    headline = models.CharField(max_length=300)
    desc = models.TextField()
    display = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ข่าวสาร'
        verbose_name_plural = 'ข่าวสาร'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.id}  {self.headline}'
    
class Pet(models.Model):
    name = models.CharField(max_length=300)
    age = models.IntegerField()
    profile = models.ImageField(upload_to='pets/',null=True,blank=True)
    sex = models.CharField(max_length=300)
    breed = models.CharField(max_length=300)
    desc = models.TextField()
    date_time = models.DateTimeField()

    class Meta:
        verbose_name = 'สัตว์เลี้ยง'
        verbose_name_plural = 'รายการสัตว์เลี้ยง'
        ordering = ['id']


    def __str__(self) -> str:
        return f'{self.id}  {self.name}'
    
class Food(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    img = models.ImageField(upload_to='foods/',null=True,blank=True)
    stock = models.BooleanField(default=True)
    suggested = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'อาหาร'
        verbose_name_plural = 'รายการอาหาร'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.id}  {self.name} {self.price}'
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foods = models.ManyToManyField(Food, through='CartItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = 'ตะกร้า'
        verbose_name_plural = 'ตะกร้า'
        ordering = ['id']

    def calculate_total_price(self):
        # คำนวณราคารวมจาก CartItem ที่อยู่ในตะกร้า
        total_price = sum(cart_item.total_price for cart_item in self.cartitem_set.all())
        self.total_price = total_price
        self.save()

    def __str__(self) -> str:
        return f'{self.id}  {self.user} { self.user.first_name } { self.user.last_name }'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,)

    def calculate_total_price(self):
        self.total_price = self.food.price * self.quantity
        self.save()

    def save(self, *args, **kwargs):
        self.total_price = self.food.price * self.quantity

        super().save(*args, **kwargs)

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.save()
            self.calculate_total_price()

    def increase_quantity(self):
        self.quantity += 1
        self.save()
        self.calculate_total_price()

    def remove_from_cart(self):
        self.delete()


    class Meta:
        verbose_name = 'รายการ'
        verbose_name_plural = 'รายการในตะกร้า'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.id}-{self.cart.user} {self.food.name} จำนวน-{self.quantity} ราคา-{self.total_price}'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_cancelled = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    items = models.TextField()

    class Meta:
        verbose_name = 'คำสั่งซื้อ'
        verbose_name_plural = 'รายการคำสั่งซื้อ'
        ordering = ['-id']
            
    def __str__(self):
        return f'{self.id} - {self.user.username} - Total: {self.total_price} - Cancelled: {self.is_cancelled} - Paid: {self.is_paid}'


