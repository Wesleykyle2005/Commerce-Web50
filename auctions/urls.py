"""
URL configuration for the auctions app.

This module defines the URL patterns for the auctions app, 
mapping URLs to their corresponding views.

Available URL patterns:
- "" : Home page, handled by `views.index`
- "login" : Login page, handled by `views.login_view`
- "logout" : Logout page, handled by `views.logout_view`
- "register" : Registration page, handled by `views.register`
- "add/listing" : Page to add a new listing, handled by `views.add_listing`
- "listing/<listing_id>(/<override>)?" : View a specific listing, 
optionally with an override, handled by `views.view_listing`
- "add/comment/<listing_id>" : Add a comment to a listing, handled by `views.add_comment`
- "add/bid/<listing_id>" : Add a bid to a listing, handled by `views.add_bid`
- "close/auction/<listing_id>" : Close an auction for a listing, handled by `views.close_auction`
- "notifications/show" : Show notifications, handled by `views.notifications_show`
- "display/watchlist" : Display the user's watchlist, 
handled by `views.display_watchlist`
- "add/watchlist/<listing_id>" : Add a listing to the user's watchlist, 
handled by `views.add_watchlist`
- "display/category" : Display listings by category, handled by `views.display_category`
"""

from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add/listing", views.add_listing, name="add_listing"),
    re_path(r'^listing/(?P<listing_id>\d+)(?:/(?P<override>\w+))?$',
     views.view_listing, name='view_listing'),
    path("add/comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("add/bid/<int:listing_id>", views.add_bid, name="add_bid"),
    path("close/auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("notifications/show", views.notifications_show, name="notifications_show"),
    path("display/watchlist", views.display_watchlist, name="display_watchlist"),
    path("add/watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("display/category", views.display_category, name="display_category"),
    path("mark/read/<int:notification_id>", views.mark_read, name="mark_read"),
]
