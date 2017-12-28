from django.shortcuts import render

# Create your views here.
class GeneralViews():
    def dashboard(request):
        return render(request,"dashboard.html")