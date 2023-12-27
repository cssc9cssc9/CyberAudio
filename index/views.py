from django.shortcuts import render
from index.models import PresentIndex
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def index_view(request):
    PresentIndexModel=  PresentIndex.objects.all()
    return render(request, 'index.html')
