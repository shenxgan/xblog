from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap
from django.http import Http404
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

from models import Article
from forms import ArticlePublishForm


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.url


def blog_index(request):
    context = {
        'test': 'just for test.',
        'welcome': 'hello world.'
    }
    return render(request, 'blog_index.html', context)


class ArticlePublishView(FormView):
    template_name = 'article_publish.html'
    form_class = ArticlePublishForm
    success_url = '/blog/'

    def form_valid(self, form):
        form.save(self.request.user.username)
        return super(ArticlePublishView, self).form_valid(form)

    #def get_success_url(self):
    #    title = self.request.POST.get('title')
    #    success_url = '/article/%s' % (title)
    #    return success_url


class ArticleDetailView(DetailView):
    template_name = 'article_detail.html'

    def get_object(self, **kwargs):
        title = self.kwargs.get('title')
        try:
            #now = datetime.datetime.now()
            #Article.objects.bulk_create([
            #    Article(url='test001.html',title='test',title_zh='hehe',author='sh',content_md='hh', content_html='hh',tags='hh',views=0,created=now,updated=now),
            #    Article(url='test001.html',title='test',title_zh='hehe',author='sh',content_md='hh', content_html='hh',tags='hh',views=0,created=now,updated=now),
            #    Article(url='test001.html',title='test',title_zh='hehe',author='sh',content_md='hh', content_html='hh',tags='hh',views=0,created=now,updated=now)
            #])
            article = Article.objects.get(title=title)
            article.views += 1
            article.save()
            article.tags = article.tags.split()
        except Article.DoesNotExist:
            raise Http404("Article does not exist")
        return article


class ArticleEditView(FormView):
    template_name = 'article_publish.html'
    form_class = ArticlePublishForm
    article = None

    def get_initial(self, **kwargs):
        title = self.kwargs.get('title')
        try:
            self.article = Article.objects.get(title=title)
            initial = {
                'title': title,
                'content': self.article.content_md,
                'tags': self.article.tags,
            }
            return initial
        except Article.DoesNotExist:
            raise Http404("Article does not exist")

    def form_valid(self, form):
        form.save(self.request, self.article)
        return super(ArticleEditView, self).form_valid(form)

    def get_success_url(self):
        title = self.request.POST.get('title')
        #success_url = '/blog/article/%s' % (title)
        success_url = reverse('article_detail', args=(title,))
        return success_url
