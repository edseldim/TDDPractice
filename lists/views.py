from django.shortcuts import HttpResponse,render,redirect
from lists.models import Item

# Create your views here.
def home_page(request):
    return render(request,"home.html")

def view_list(request):
    return render(request,"list.html",{"item_list":Item.objects.all()})

def new_list(request):
    Item.objects.create(text=request.POST["item_text"])
    return redirect("/lists/the-only-list-in-the-world/")