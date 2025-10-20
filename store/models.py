from django.db import models
from django.contrib.auth.models import User


class Slide(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField('rasm')

    def __str__(self):
        return self.title
    
class Products(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=20000)
    slug = models.CharField(max_length=255)
    image = models.ImageField()
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.description[:30] + '...  read more'
    
    def shortem(self):
        return self.title[:10] + '...'
    

class Comment(models.Model):
    news = models.ForeignKey(Products, on_delete=models.CASCADE,null=True, related_name='comments')
    comment_text = models.TextField('comment', max_length=1000)
    
    def __str__(self):
        return 'USER' + self.comment_text
    
    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'



class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title
    
    def total_price(self):
        return self.product.price * self.quantity