from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing', views.create_listing, name = "create_listing"),
    path("<int:l_id>/listing_page", views.listing_page, name = "listing_page"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("<int:l_id>/bid", views.bid, name = "bid"),
    path("<int:l_id>/close_listing", views.close_listing, name = "close_listing"),
    path("closed_listings_page", views.closed_listings_page, name = "closed_listings_page"),
    path("<int:l_id>/comments", views.comments, name = "comments"),
    path("filter_category", views.filter_category, name = "filter_category"),
    path('remove_watchlist/<int:l_id>', views.remove_watchlist, name = 'remove_watchlist')
]
