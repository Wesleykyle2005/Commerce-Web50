from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import User, Category, Listing, Bid, Comment, Notification
from django.core.paginator import Paginator


class ListingForm(forms.Form):
    """
    Form for creating a new listing.

    Fields:
    - title: The title of the listing.
    - description: A description of the listing.
    - starting_bid: The starting bid for the listing.
    - image_url: The URL of the image for the listing.
    - category: The category of the listing.
    """
    title = forms.CharField(
        label="Titulo",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Name of the listing'
            }
        )
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-control'
            }
        )
    )
    starting_bid = forms.DecimalField(
        label='Starting bid',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'min': 0.01,
                'step': 0.01,
                'class': 'form-control',
                'placeholder': '0.00'
            }
        )
    )
    image_url = forms.URLField(
        label='Image URL',
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'link to the image'
            }
        )
    )
    category = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        """Initialize the form with category choices."""
        super().__init__(*args, **kwargs)
        categories = Category.objects.all().values_list('id', 'name')
        self.fields['category'].choices = [("", "Select a category")] + list(categories)


class CommentForm(forms.Form):
    """
    Form for adding a comment to a listing.

    Fields:
    - comment: The content of the comment.
    """
    comment = forms.CharField(
        label='Content',
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-control'
            }
        )
    )


def index(request):
    """Render the index page with active listings."""
    listings = Listing.objects.filter(active=True)
    paginator = Paginator(listings, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "auctions/index.html", {
        "page_obj": page_obj
    })


def login_view(request):
    """Handle user login."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """Handle user registration."""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def add_listing(request):
    """Handle adding a new listing."""
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "form": ListingForm()
        })
    else:
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                starting_bid=form.cleaned_data['starting_bid'],
                image_url=form.cleaned_data['image_url'],
                owner=request.user,
                current_price=form.cleaned_data['starting_bid'],
                category=Category.objects.get(id=form.cleaned_data['category'])
            )
            listing.save()
            return redirect('index')


@login_required
def view_listing(request, listing_id, override=None):
    """View a specific listing."""
    if request.method == "GET":
        listing = get_object_or_404(Listing, id=listing_id)

        if not listing.active and not override:
            return redirect('index')

        isowner = listing.owner == request.user
        min_bid = listing.current_price + 1
        comments = Comment.objects.filter(listing_id=listing.id)

        return render(request, "auctions/view_listing.html", {
            "listing": listing,
            "isowner": isowner,
            "comments": comments,
            "comment_form": CommentForm(),
            "min_bid": min_bid,
            "override": override is not None,
            "watching": request.user in listing.watchers.all()
        })


@login_required
def add_comment(request, listing_id):
    """Add a comment to a listing."""
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                content=form.cleaned_data['comment'],
                author=request.user,
                listing=get_object_or_404(Listing, id=listing_id),
            )
            comment.save()
            return redirect('view_listing', listing_id=listing_id)
    else:
        form = CommentForm()
    return render(request, 'auctions/view_listing.html', {
        'form': form,
        'listing': get_object_or_404(Listing, id=listing_id),
        'comments': Comment.objects.filter(listing_id=listing_id)
    })


@login_required
def add_bid(request, listing_id):
    """Add a bid to a listing."""
    if request.method == "POST":
        listing = get_object_or_404(Listing, id=listing_id)
        bid = float(request.POST['bid'])
        if bid > listing.current_price:
            listing.current_price = bid
            listing.save()
            new_bid = Bid(
                amount=bid,
                bidder=request.user,
                listing=listing
            )
            new_bid.save()
            Notification.objects.create(
                user=listing.owner,
                message=f"A new offer has been made in: {listing.title}",
                listing=listing
            )
            return redirect('view_listing', listing_id=listing_id)


@login_required
def close_auction(request, listing_id):
    """Close an auction for a listing."""
    listing_this = get_object_or_404(Listing, id=listing_id)
    listing_this.active = False
    highest_bid = Bid.objects.filter(listing=listing_this).order_by('-amount').first()
    if highest_bid:
        bid_winner = highest_bid.bidder
        listing_this.winner = bid_winner
        Notification.objects.create(
            user=bid_winner,
            message=f"Congratulations, you have won the auction for: {listing_this.title}",
            listing=listing_this
        )
    else:
        listing_this.winner = None
    listing_this.save()
    return redirect('index')


@login_required
def notifications_show(request):
    """Show notifications for the logged-in user."""
    notifications_for_this_user = Notification.objects.filter(user=request.user)
    return render(request, 'auctions/notifications.html', {
        'notifications': notifications_for_this_user
    })


@login_required
def display_watchlist(request):
    """Display the watchlist for the logged-in user."""
    user_watchlist = Listing.objects.filter(watchers=request.user)
    return render(request, 'auctions/watchlist.html', {
        "listings": user_watchlist
    })


@login_required
def add_watchlist(request, listing_id):
    """Add or remove a listing from the watchlist."""
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user in listing.watchers.all():
        listing.watchers.remove(request.user)
        return redirect('display_watchlist')
    else:
        listing.watchers.add(request.user)
    return redirect('display_watchlist')


@login_required
def display_category(request):
    """Display listings by category."""
    categories = Category.objects.all()

    if request.method == "POST":
        category_id = request.POST['category']
        category = get_object_or_404(Category, id=category_id)
        listings = Listing.objects.filter(category=category)
        return render(request, 'auctions/categories.html', {
            'listings': listings,
            'category': category,
            'categories': categories,
            'find_listing': True
        })

    return render(request, 'auctions/categories.html', {
        'categories': categories,
        'find_listing': False
    })


@login_required
def mark_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    return redirect('notifications_show')	