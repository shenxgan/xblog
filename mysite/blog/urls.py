from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from views import ArticlePublishView, ArticleDetailView, ArticleEditView, BlogSitemap

urlpatterns = [
    url(r'^$', 'blog.views.blog_index', name='blog_index'),
    url(r'^article/publish$', ArticlePublishView.as_view(), name='article_publish'),
    url(r'^article/(?P<title>\w+\.?\w+)$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^article/(?P<title>\w+\.?\w+)/edit$', ArticleEditView.as_view(), name='article_edit'),

    #sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'blog': BlogSitemap}},name='django.contrib.sitemaps.views.sitemap')
]
