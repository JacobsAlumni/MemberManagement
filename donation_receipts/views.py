import base64

from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth import decorators
from django.contrib.auth import mixins
from django.http import FileResponse
from django.views import generic
from django.conf import settings

from .models import DonationReceipt


@decorators.login_required
def download_receipt(request, receipt_id):
    receipt: DonationReceipt = get_object_or_404(
        DonationReceipt, external_id=receipt_id, received_from=request.user
    )

    response = FileResponse(receipt.receipt_pdf)
    response[
        "Content-Disposition"
    ] = f"filename=Zuwendungsbestätigung vom {receipt.received_on}.pdf"

    return response


class ReceiptList(mixins.LoginRequiredMixin, generic.ListView):
    model = DonationReceipt
    template_name = "donation_receipts/list.html"
    ordering = "-received_on"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(received_from=self.request.user, finalized=True)
        )


class ReceiptView(
    generic.DetailView, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin
):
    model = DonationReceipt
    template_name = "donation_receipts/receipt_pdf.html"
    slug_field = "external_id"
    context_object_name = "receipt"
    slug_url_kwarg = "receipt_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with open(settings.SIGNATURE_IMAGE, "rb") as sig_image:
            encoded = base64.b64encode(sig_image.read())
            context["sig_image_b64"] = "data:image/png;base64," + encoded.decode(
                "ascii"
            )

        return context

    def test_func(self):
        obj = self.get_object()

        return obj.finalized and obj.received_from == self.request.user
