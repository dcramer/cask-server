# from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from cask.views import EnhancedGraphQLView

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(EnhancedGraphQLView.as_view(graphiql=True)))
]
