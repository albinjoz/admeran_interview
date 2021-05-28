"""admaren URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from application import overview, views
from django.contrib import admin
from django.urls import path, include

from application.serializer import MultiFieldJWTSerializer,CustomRefreshSerializer

from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views


router = routers.DefaultRouter()
router.register(r'^snippet', views.SnippetViewset),
router.register(r'^tag', views.TagViewset),

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('overview', overview.overview_snippet),
    path('reg', views.register),
    path('login', jwt_views.TokenObtainPairView.as_view(serializer_class=MultiFieldJWTSerializer), name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(serializer_class=CustomRefreshSerializer), name='token_refresh'),
]
