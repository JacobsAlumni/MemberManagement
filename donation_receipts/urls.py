from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.ReceiptList.as_view(), name='list'),
    path('<uuid:receipt_id>/download', views.download_receipt, name='download'),
]

if settings.DEBUG:
    urlpatterns.append(path('<uuid:receipt_id>/view', views.ReceiptView.as_view(extra_context={'giant_floating_text': 'MUSTER'}), name='view'))
