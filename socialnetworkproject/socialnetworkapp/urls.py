import debug_toolbar
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from django.contrib import admin

from . import views
# from .admin import admin_site

from rest_framework.routers import DefaultRouter

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('tags', views.TagViewSet, basename='tag')
router.register('actions', views.ActionViewSet, basename='action')
router.register('comments', views.CommentViewSet, basename='comment')
router.register('posts', views.PostViewSet, basename='post')
router.register('posts', views.PostListCreateViewSet, basename='post')
router.register('reports', views.ReportViewSet, basename='report')
router.register('auction_items', views.AuctionItemViewSet, basename='auction_item')
router.register('transactions', views.TransactionViewSet, basename='transaction')

# defind view for swagger tool
schema_view = get_schema_view(
    openapi.Info(
        title="Course API",
        default_version='v1.0',
        description="APIs for Charity Social Network Project",
        contact=openapi.Contact(email="trung.pv194@gmail.com"),
        license=openapi.License(name="Phan Văn Trung @2021"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

    # swagger url
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # oauth2
    re_path(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # defind end_point to get client_id and client_secret
    path('oauth2-info/', views.AuthInfo.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
