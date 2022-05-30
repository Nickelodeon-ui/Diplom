# pylint: skip-file

from django.urls import path

from .views import (
    PropertiesListView,
    PropertyDetailView,
    AboutUsView,
    SearchForReservationView,
    BookPropertyView
)


urlpatterns = [
    path('', PropertiesListView.as_view(), name="properties_list"),
    path('search_for_reservation', SearchForReservationView.as_view(), name='search_for_reservation'),
    # path("more-bg/<int:lower_border>", MoreBoardGamesView.as_view(), name="more_bg"),
    # path("more-searched-bg/<int:lower_border>", MoreSearchedBoardGamesView.as_view(), name="more_searched_bg"),
    path("<int:pk>", PropertyDetailView.as_view(), name="property_detail"),
    path("<int:pk>", BookPropertyView.as_view(), name="book_property"),
    # path("download-csv/", DownloadCSVView.as_view(), name="download_csv"),
    # path("download-pdf/", DownloadPDFView.as_view(), name="download_pdf"),
    path("about-us/", AboutUsView.as_view(), name="about_us"),
]   