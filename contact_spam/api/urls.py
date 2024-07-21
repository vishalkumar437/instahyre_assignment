from django.urls import path
from contact_spam.api.views import ContactSearchByName, ReportSpamByPhone, SearchByPhone

urlpatterns = [
    path("searchByName", ContactSearchByName.as_view(), name="ContactSearchByName"),
    path("reportSpam", ReportSpamByPhone.as_view(), name="ReportSpam"),
    path('searchByPhone/<str:query_param>', SearchByPhone.as_view(), name='SearchByPhone'),
]