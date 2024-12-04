from django.contrib import admin
from django.urls import path, include

urlpatterns = [   
    path('admin/', admin.site.urls),
    path('garden/', include('gardening.urls')),  
    path('users/', include('users.urls'))
]
