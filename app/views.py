from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def faq(request):
    return render(request, 'faq.html')


def contacts(request):
    return render(request, 'contacts.html')


def services(request):
    return render(request, 'services.html')


def support(request):
    return render(request, 'support.html')

