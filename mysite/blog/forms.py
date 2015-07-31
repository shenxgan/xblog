#!/usr/bin/env python
# coding=utf-8
import datetime
import re
import markdown

from django import forms

from models import Article
#from models import Article, Comment
#from message.models import Notification
#from utils.emoji import emoji


class ArticlePublishForm(forms.Form):
    title = forms.CharField(
        label=u'文章标题',
        max_length=50,
        widget=forms.TextInput(attrs={'class': '', 'placeholder': u'文章标题，记得在标题末尾添加".html"'}),
        )

    content = forms.CharField(
        label=u'内容',
        min_length=10,
        widget=forms.Textarea(),
        #widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': u'事情是这样子的……'}),
        )

    #ARTICLETYPE= (
    #    ('django', 'Django'),
    #    ('python', 'Python'),
    #    ('other', 'Other'),
    #)
    #type = forms.ChoiceField(
    #    label=u'文章类型',
    #    choices=ARTICLETYPE,
    #    widget=forms.RadioSelect(),
    #    )

    tags = forms.CharField(
        label=u'标签',
        max_length=30,
        widget=forms.TextInput(attrs={'class': '', 'placeholder': u'文章标签，以空格进行分割'}),
        )

    def save(self, username, article=None):
        cd = self.cleaned_data
        title = cd['title']
        title_zh = title
        now = datetime.datetime.now()
        content_md = cd['content']
        #content_html = markdown.markdown(cd['content'])
        content_html = markdown.markdown(cd['content'], extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
        re_title = '<h\d>(.+)</h\d>'
        data = content_html.split('\n')
        for line in data:
            title_info = re.findall(re_title, line)
            if title_info:
                title_zh = title_info[0]
                break
        url = '/article/%s' % (title)
        tags = cd['tags']
        #article = Article(
        #    url=url,
        #    title=title,
        #    title_zh=title_zh,
        #    author=username,
        #    content_md=content_md,
        #    content_html=content_html,
        #    label=label,
        #    views=0,
        #    created=now,
        #    updated=now)
        if article:
            article.url = url
            article.title = title
            article.title_zh = article
            article.content_md = content_md
            article.content_html = content_html
            #article.type = type
            article.tags = tags
            article.updated = now
        else:
            article = Article(
                url=url,
                title=title,
                title_zh=title_zh,
                author=username,
                content_md=content_md,
                content_html=content_html,
                #type=type,
                tags=tags,
                views=0,
                created=now,
                updated=now)
        article.save()


#class BlogCommentForm(forms.Form):
#    comment = forms.CharField(
#        label=u'',
#        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': u'你想说什么？'}),
#        )
#
#    def clean_comment(self):
#        comment = self.cleaned_data['comment']
#        # to do ... escape safe
#        comment = comment.replace('&', '&amp;')
#        comment = comment.replace('<', '&lt;')
#        comment = comment.replace('>', '&gt;')
#        comment = comment.replace('\'', '&#39;')
#        comment = comment.replace('"', '&quot;')
#        comment = comment.replace('::', ': :')
#        re_url = 'https?://\S+'
#        url_list = re.findall(re_url, comment)
#        for url in url_list:
#            if url.endswith('.PNG') or \
#               url.endswith('.JPG') or \
#               url.endswith('.JPEG') or \
#               url.endswith('.BMP') or \
#               url.endswith('.GIF') or \
#               url.endswith('.png') or \
#               url.endswith('.jpg') or \
#               url.endswith('.jpeg') or \
#               url.endswith('.bmp') or \
#               url.endswith('.gif'):
#                replace = '<img src="%s" alt="%s">' % (url, url)
#            else:
#                replace = '<a href="%s" target="_block">%s</a>' % (url, url)
#            comment = comment.replace(url, replace)
#        re_name = '(\:\S+\:)'
#        emoji_list = re.findall(re_name, comment)
#        for name in emoji_list:
#            position = emoji.get(name)
#            if position:
#                replace = '<span class="emoji" style="background-position: -%spx 0;"></span>' % (str((position-1)*32+5))
#                comment = comment.replace(name, replace)
#        comment = comment.replace(': :', '::')
#        return comment
#
#    def save(self, request):
#        cd = self.cleaned_data
#        now = datetime.datetime.now()
#        username = request.user.username
#        article_title = request.POST.get('article_title')
#        comment = Comment(username=username, article_title=article_title, comment=cd['comment'], created=now)
#        comment.save()
#        ## notify
#        url = request.path
#        receiver = request.POST.get('article_author')
#        if receiver != username:
#            description = cd['comment'][:20]
#            if len(cd['comment']) >= 20:
#                description += ' ...'
#            notification = Notification(url=url, receiver=receiver, sender=username, description=description, type=u'博客评论', read=False, created=now)
#            notification.save()
