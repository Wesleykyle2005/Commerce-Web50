from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("display_category", views.display_category, name="display_category"),
    path("listing/<int:id>", views.listing_detail, name="listing_detail"),
    path("remove_watchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("display_watchlist", views.display_watchlist, name="display_watchlist"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("add_bid/<int:id>", views.add_bid, name="add_bid"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
]
