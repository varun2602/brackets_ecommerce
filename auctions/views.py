from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import models

li = []
test1 = []
def index(request):
    if request.method == "GET":
        listings_all = models.Listing.objects.all()
        categories = models.Category.objects.all()
        context = {"listings_all": listings_all, "categories": categories}
        return render(request, "auctions/index.html", context)

def listing_page(request, l_id):
    if request.method == "GET":
        listing_specific = models.Listing.objects.get(pk = l_id)
        comments = models.Comment.objects.filter(listing = listing_specific)
        context = {"listing_specific": listing_specific, "comments": comments}
        return render(request, "auctions/listing_page.html", context)
    if request.method == "POST":
        current_user = request.user
        specific_listing = models.Listing.objects.get(pk = l_id)
        # test = models.watchlist.objects.get(listing = specific_listing, owner = current_user)
        # if test == "n":
        #     context = {"message": "Listing already in watchlist", "listing_specific": specific_listing}
        #     return render(request, "auctions/listing_page.html", context)
        watchlist_add = models.watchlist(listing = specific_listing, owner = current_user)
        watchlist_add.save()
        return HttpResponseRedirect(reverse('listing_page', args = (l_id,)))

def create_listing(request):
    if request.method == "GET":
        categories = models.Category.objects.all()
        context = {"categories": categories}
        return render(request, "auctions/create_listing.html", context)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image_url = request.POST.get("iurl")
        starting_price = request.POST.get("bid")
        owner = request.user
        category_id = request.POST.get("categories")
        category = models.Category.objects.get(pk = category_id)
        listing_to_create = models.Listing(title = title, description = description, starting_bid = starting_price, image_url = image_url, owner = owner, category = category )
        listing_to_create.save()
        categories = models.Category.objects.all()
        context = {"message": "Listing Created", "categories":categories}
        return render(request, "auctions/create_listing.html", context)
        # return HttpResponse(f"{category}")

def watchlist(request):
    if request.method == "GET":
        current_user = request.user
        listings_user = models.watchlist.objects.filter(owner = current_user)
        context = {"listings_user": listings_user}
        return render(request, "auctions/watchlist.html", context)

def bid(request, l_id):
    if request.method == "GET":
        # Get current user name 
        bidding_user = request.user
        # Get the associated listing 
        listing_specific = models.Listing.objects.get(pk = l_id)
        # Get the satrting price entered by the user 
        listing_starting_price = int(listing_specific.starting_bid)
        # Get the bid price entered by the current user 
        bid_price = int(request.GET.get("lbid"))
        # Get all the bids made so far 
        all_bids = models.Bid.objects.filter(bidding_listing = listing_specific)
        max = 0
        for a in all_bids:
            if a.bid_price > max:
                max = a.bid_price
        print(max)
        if bid_price <= listing_starting_price or  bid_price <= max:
            context = {"message": "Bid price should be atleast greater than starting price and other bid prices "}
            return render(request, "auctions/error.html", context)
        else:
            bid_object = models.Bid(bid_price = bid_price, bidding_user = bidding_user, bidding_listing = listing_specific)
            bid_object.save()
            return HttpResponseRedirect(reverse('listing_page', args = (l_id,)))
            

            
            return HttpResponse("Test Successful")
            # return HttpResponseRedirect(reverse('listing_page', args = (l_id,)))   
def close_listing(request, l_id):
    # Getting the listing 
    listing_specific = models.Listing.objects.get(pk = l_id)
    # Rendering the listing inactive
    listing_specific.is_active = False
    listing_specific.save()
    # Declaring the winner
    bids_for_listing = models.Bid.objects.filter(bidding_listing = listing_specific)
    for b in bids_for_listing:
        print(b)
    # return HttpResponse('Successful')
    max = 0
    for b in bids_for_listing:
        if b.bid_price > max:
            max = b.bid_price
    bid_winner_listing = models.Bid.objects.filter(bidding_listing = listing_specific, bid_price = max)
    # return HttpResponse(f'{bid_winner_listing[0]}')
    bid_winner = bid_winner_listing[0].bidding_user
    listing_title = listing_specific.title
    context = {"bid_winner":bid_winner, "listing_title": listing_title}
    return render(request, "auctions/bid_winner.html", context)
    # return HttpResponse(f"{bid_winner}")

def closed_listings_page(request):
    listings_closed = models.Listing.objects.filter(is_active = False)
    context = {"listings_closed": listings_closed}
    return render(request, "auctions/closed_listings.html", context)

def comments(request, l_id):
    comment = request.GET.get("comment")
    comment_owner = request.user
    listing_specific = models.Listing.objects.get(pk = l_id)
    comment_object = models.Comment(comment = comment, comment_owner = comment_owner, listing = listing_specific)
    comment_object.save()
    return HttpResponseRedirect(reverse('listing_page', args = (l_id,)))

def filter_category(request):
    category_id = request.GET.get("categories")
    category = models.Category.objects.get(pk = category_id)
    listings_category = models.Listing.objects.filter(category = category)
    context = {"category":category, "listings_category": listings_category}
    return render(request, "auctions/filter.html", context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def remove_watchlist(request, l_id):
    listing_specific = models.Listing.objects.get(pk = l_id)
    watchlist_obj = models.watchlist.objects.get(listing = listing_specific)
    watchlist_obj.delete()
    return HttpResponseRedirect(reverse('watchlist'))
