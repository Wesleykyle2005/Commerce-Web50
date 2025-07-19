# 🛒 Commerce Web50 — CS50W Project Solution


🗪 README.md en español: [README_ES.md](README_ES.md)

**Commerce Web50**, a full-featured implementation of the online auction project inspired by eBay, developed as part of **CS50’s Web Programming with Python and JavaScript**. This solution is built using **Django** and fulfills all the specifications outlined in the original assignment.

---

## 📸 Screenshots

* **Active Listings**
  ![Active Listings](auctions/static/auctions/images/Active_listings.png)

* **Create New Listing**
  ![Create Listing](auctions/static/auctions/images/Create_new_listing.png)

* **View Listing**
  ![View Listing](auctions/static/auctions/images/view_listing.png)

* **Watchlist**
  ![Watchlist](auctions/static/auctions/images/Watchlist.png)

---

## 🧾 Overview

This platform allows users to:

* Create auctions with title, description, starting price, optional image, and optional category.
* Place bids in real time, with validation to ensure bids are higher than the current maximum.
* Post public comments on listings.
* Add or remove listings from a personal watchlist.
* Close their own auctions, automatically notifying the winner if any.
* Receive in-app notifications relevant to their activity.
* Filter and browse active auctions by category.

---

## ⚙️ Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/Wesleykyle2005/Commerce-Web50.git
cd Commerce-Web50
```

### 2. Install dependencies

```bash
pip install django
```

### 3. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Insert demo data

```bash
python make_insertions.py
```

This script generates:

* 30 user accounts
* 30 categories
* 30 listings with predefined bids and comments
* Superuser credentials:

  * **Username:** `Admin1234`
  * **Password:** `Admin1234`

### 5. Run the development server

```bash
python manage.py runserver
```

Access via: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📐 Implementation Details

* **Custom models:**

  * `User` (extends `AbstractUser`), `Auction`, `Bid`, `Comment`, `Category`

* **Auction creation form:**

  * Supports title, description, starting bid, optional image upload, and category selection.

* **Active listings:**

  * Home page shows all currently open auctions.

* **Auction detail view:**

  * Enables bidding, commenting, managing watchlist, and auction closure (by owner only).

* **Watchlist:**

  * Per-user view to track listings of interest.

* **Category navigation:**

  * Allows filtering of open listings by category.

* **Admin panel:**

  * Full Django admin support at `/admin`, accessible via the provided superuser.

---

## 🛠️ Technical Considerations

* Sensitive routes are protected using the `@login_required` decorator.
* Notifications are implemented via Django’s user messaging framework.
* Pagination is included to ensure performance at scale.
* Class-based views and model inheritance are employed to keep the project modular and extensible.

---

## 🔗 Quick Access

* **Admin interface:**
  [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
  Use the superuser credentials provided above.

* **Key features summary:**

  * Registered users can create auctions, place bids, and close their own listings.
  * Bids are only accepted if they exceed the current highest offer.
  * Real-time notifications are shown in the navigation bar.
  * Listings can be added to or removed from a personal watchlist.
  * Only the listing creator is allowed to close the auction manually.
