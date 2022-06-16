from django.contrib import admin
from django.urls import path, include
from sholah_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', views.GuestViewSet)
router.register('movies', views.MovieViewSet)
router.register('reservations', views.ReservationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('guest/list', views.no_rest_no_model),
    path('guests/', views.no_rest_from_model),
    path('guest/create', views.FBV_list),
    path('guest/actions/<int:pk>', views.FBV_pk),
    path('guest/all', views.CbvList.as_view()),
    path('guest/all/<int:pk>', views.CbvDetail.as_view()),
    path('guest/mixins', views.mixins_list.as_view()),
    path('guest/mixins/<int:pk>', views.mixins_pk.as_view()),
    path('guest/generics', views.grnrrics_list.as_view()),
    path('guest/generics/<int:pk>', views.generaics_pk.as_view()),
    path('viewsets/', include(router.urls)),
    path('get-movie/', views.get_movie),
    path('post-reservation/', views.new_reservation),

]
