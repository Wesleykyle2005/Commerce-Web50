from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    active_listings = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(
        request,
        "auctions/index.html",
        {"listings": active_listings, "categories": categories},
    )


def close_auction(request, id):
    listing = get_object_or_404(Listing, pk=id)
    listing.active = False
    listing.save()
    context = {
        "listing": listing,
        "is_watchlist": request.user in listing.watchlist.all(),
        "comments": Comment.objects.filter(listing=listing),
        "is_owner": request.user == listing.owner,
        "update": True,
        "message": "Auction closed",
    }
    return render(request, "auctions/listing.html", context)


def listing_detail(request, id):
    listing = get_object_or_404(Listing, pk=id)
    context = {
        "listing": listing,
        "is_watchlist": request.user in listing.watchlist.all(),
        "comments": Comment.objects.filter(listing=listing),
        "is_owner": request.user == listing.owner,
    }
    return render(request, "auctions/listing.html", context)


def display_category(request):
    if request.method == "POST":
        category_name = request.POST.get("category")
        category = get_object_or_404(Category, name=category_name)
        active_listings = Listing.objects.filter(active=True, category=category)
        categories = Category.objects.all()
        return render(
            request,
            "auctions/index.html",
            {"listings": active_listings, "categories": categories},
        )


def display_watchlist(request):
    user = request.user
    listings = user.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {"listings": listings})


def add_comment(request, id):
    if request.method == "POST":
        user = request.user
        listing = get_object_or_404(Listing, pk=id)
        message = request.POST.get("new_comment")
        comment = Comment(author=user, listing=listing, message=message)
        comment.save()
        return HttpResponseRedirect(reverse("listing_detail", args=(id,)))


def remove_watchlist(request, id):
    listing = get_object_or_404(Listing, pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing_detail", args=(id,)))


def add_watchlist(request, id):
    listing = get_object_or_404(Listing, pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing_detail", args=(id,)))


def add_bid(request, id):
    if request.method == "POST":
        new_bid_amount = float(request.POST.get("new_bid"))
        listing = get_object_or_404(Listing, pk=id)
        if new_bid_amount > listing.starting_bid.amount:
            new_bid = Bid(user=request.user, amount=new_bid_amount)
            new_bid.save()
            listing.starting_bid = new_bid
            listing.save()
            context = {
                "listing": listing,
                "update": True,
                "message": "Bid updated successfully",
                "is_watchlist": request.user in listing.watchlist.all(),
                "comments": Comment.objects.filter(listing=listing),
                "is_owner": request.user == listing.owner,
            }
            return render(request, "auctions/listing.html", context)
        else:
            context = {
                "listing": listing,
                "update": False,
                "message": "Bid not high enough",
                "is_watchlist": request.user in listing.watchlist.all(),
                "comments": Comment.objects.filter(listing=listing),
                "is_owner": request.user == listing.owner,
            }
            return render(request, "auctions/listing.html", context)
    return HttpResponseRedirect(reverse("listing_detail", args=(id,)))


def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {"categories": categories})
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        image_url = request.POST.get("image_url")
        starting_bid_amount = float(request.POST.get("starting_bid"))
        category_name = request.POST.get("category")

        user = request.user
        category = get_object_or_404(Category, name=category_name)

        starting_bid = Bid(amount=starting_bid_amount, user=user)
        starting_bid.save()

        new_listing = Listing(
            title=title,
            description=description,
            image_url=image_url,
            starting_bid=starting_bid,
            category=category,
            owner=user,
        )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html")
