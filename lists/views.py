from django.shortcuts import HttpResponse,render,redirect
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == "POST":
        new_item_text = request.POST.get("item_text","")
        Item.objects.create(text=new_item_text)
        return redirect("/")
    return render(request,"home.html",{"item_list":Item.objects.all()})
    # return render(request, "home.html")