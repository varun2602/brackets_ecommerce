from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length = 30, default = '')

    def __str__(self):
        return f"{self.category}"



class Listing(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500, default = '')
    starting_bid = models.IntegerField()
    image_url = models.URLField(max_length = 1000, blank = True, null = True, default = '')
    owner = models.ForeignKey(User, on_delete = models.CASCADE, default = '',  related_name = "listing_owner")
    is_active = models.BooleanField(default = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True, null = True, related_name = "category_related")
    

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    comment = models.CharField(max_length = 400, null = True, default = '')
    comment_owner = models.CharField(max_length = 50, null = True, default = '')
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, null= True, blank = True, related_name = "listing_related")
    
    def __str__(self):
        return f"{self.comment}"

class Bid(models.Model):
    bid_price = models.IntegerField(max_length = 5, default = 0)
    bidding_user = models.ForeignKey(User, on_delete = models.CASCADE, default = '', related_name = "bidding_user_related")
    bidding_listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bidding_listing_related")

    def __str__(self):
        return f"{self.bidding_user}:{self.bid_price}"





class watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, null = True,  related_name = "listing_watchlist")
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null = True ,  related_name = "listing_owner_watchlist")

    def __str__(self):
        return f"{self.listing}"
        

