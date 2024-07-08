from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Bid(models.Model):
    amount = models.FloatField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid"
    )

    def __float__(self):
        return self.amount


class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    image_url = models.URLField(max_length=200)
    starting_bid = models.ForeignKey(
        Bid, blank=True, null=True, on_delete=models.CASCADE, related_name="bidPrice"
    )
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="category",
    )
    watchlist = models.ManyToManyField(
        User, blank=True, related_name="listingWatchlist"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="comments"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="comments",
    )
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"
