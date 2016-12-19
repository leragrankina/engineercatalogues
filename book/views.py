from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse

import stripe
# Create your views here.


class BookView(TemplateView):
    template_name = 'book/index.html'


def charge(request):
    stripe.api_key = "sk_test_vqYqDBQbgvF1X0OoOHyhXZGR"
    token = request.POST['stripeToken']
    try:
        charge = stripe.Charge.create(
            amount=10000,
            currency="usd",
            source=token,
            description="Example charge"
        )
        if charge and charge.paid:
            return render(request, 'book/success.html')

    except stripe.error.CardError as e:
        body = e.json_body
        err = body['error']
        return render(request, 'book/index.html', context={'error':err})

