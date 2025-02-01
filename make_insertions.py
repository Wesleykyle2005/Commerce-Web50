import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')
django.setup()

from auctions.models import User, Category, Listing, Bid, Comment

def create_users():
    users = []
    for i in range(1, 31):
        user = User.objects.create_user(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password='password123'
        )
        users.append(user)
        print(f'User created: {user.username}')
    return users

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        name='Admin1234'
        User.objects.create_superuser(
            username=name,
            email='admin@example.com',
            password=name
        )
        print(f'Superuser created: {name}')

def create_categories():
    categories = []
    for i in range(1, 31): 
        category = Category(name=f'Category {i}')
        categories.append(category)
    Category.objects.bulk_create(categories)
    return Category.objects.all().order_by('id')

def create_listings(users, categories):
    listings = []
    for i in range(30):
        listing = Listing(
            title=f'Laptop {i+1}',
            description=f'Description for laptop {i+1}',
            starting_bid=100.00 + (i * 50),
            current_price=100.00 + (i * 50),
            image_url=f'https://images.pexels.com/photos/1006293/pexels-photo-1006293.jpeg',
            owner=users[i % len(users)],
            category=categories[i % len(categories)],
            active=True
        )
        listings.append(listing)
    Listing.objects.bulk_create(listings)
    return Listing.objects.all().order_by('id')

def create_bids(users, listings):
    bids = []
    for i in range(30): 
        bid = Bid(
            amount=listings[i].current_price + (i * 10) + 50,
            bidder=users[(i + 5) % len(users)], 
            listing=listings[i]
        )
        bids.append(bid)
    Bid.objects.bulk_create(bids)

def create_comments(users, listings):
    comments = []
    for i in range(30):
        comment = Comment(
            content=f'This is the best laptop: {i+1}.',
            author=users[(i + 10) % len(users)], 
            listing=listings[i]
        )
        comments.append(comment)
    Comment.objects.bulk_create(comments)

def main():
    print("Creating users...")
    users = create_users()
    create_superuser()
    
    print("\nCreating categories...")
    categories = create_categories()
    
    print("\nCreating listings...")
    listings = create_listings(users, categories)
    
    print("\nCreating bid...")
    create_bids(users, listings)
    
    print("\nCreating comments...")
    create_comments(users, listings)
    
    print("\n¡All data has been inserted successfully!")

if __name__ == '__main__':
    main()