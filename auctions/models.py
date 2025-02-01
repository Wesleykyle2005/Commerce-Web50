"""
This module defines the database models for the auctions app.

Models:
- User: Extends the default Django AbstractUser model.
- Category: Represents a category for listings.
- Listing: Represents an auction listing.
- Bid: Represents a bid placed on a listing.
- Comment: Represents a comment made on a listing.
- Notification: Represents a notification for a user.

Each model includes fields and methods relevant to its purpose.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extends the default Django AbstractUser model."""

class Category(models.Model):
    """Represents a category for listings."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)

class Listing(models.Model):
    """Represents an auction listing."""
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    image_url = models.URLField()
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="listings"
    )
    winner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name="won_listings"
    )
    watchers = models.ManyToManyField(User, related_name="watchlist", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="listings"
    )

    def __str__(self):
        return str(self.title)

class Bid(models.Model):
    """Represents a bid placed on a listing."""
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(
        User,
        related_name="bids",
        on_delete=models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids"
    )

    def __str__(self):
        return f"{self.amount} by {self.bidder.username} on {self.listing.title}"

class Comment(models.Model):
    """Represents a comment made on a listing."""
    content = models.TextField()
    author = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.listing.title}"

class Notification(models.Model):
    """Represents a notification for a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.message)
    