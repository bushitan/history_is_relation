# -*- coding: utf-8 -*-
from django import template
from django import forms
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.template import Context, loader
from django.views.generic import View, TemplateView, ListView, DetailView
from django.db.models import Q
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
# from blog.models import Article, Category, Carousel, Column, Nav, News
from blog.models import *
from vmaig_comments.models import Comment
from vmaig_auth.models import VmaigUser
from vmaig_auth.forms import VmaigUserCreationForm, VmaigPasswordRestForm
from vmaig_blog.settings import PAGE_NUM
import datetime
import time
import json
import logging

# 缓存
try:
    cache = caches['memcache']
except ImportError as e:
    cache = caches['default']

# logger
logger = logging.getLogger(__name__)


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 热门文章
            context['hot_article_list'] = \
                Article.objects.order_by("-view_times")[0:10]
            # 导航条
            context['nav_list'] = Nav.objects.filter(status=0)
            # 最新评论
            context['latest_comment_list'] = \
                Comment.objects.order_by("-create_time")[0:10]
        except Exception as e:
            logger.error(u'[BaseMixin]加载基本信息出错')

        return context


class IndexView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM  # 分页--每页的数目

    def get_context_data(self, **kwargs):
        pass
        # 轮播
        kwargs['carousel_page_list'] = Carousel.objects.all()
        return super(IndexView, self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0)
        return article_list

class TimeLineIndexView(BaseMixin, ListView):
    template_name = 'time/index.html'
    context_object_name = 'story_list'
    # paginate_by = PAGE_NUM  # 分页--每页的数目

    def get_context_data(self, **kwargs):  #把参数传入模板中，并且可以增加新的参数
        # pass
        # story_list = Story.objects.filter()
        # print story_list ,"OK "
        # return story_list
        # 轮播
        # kwargs['story_l'] = Carousel.objects.all()
        return super(TimeLineIndexView, self).get_context_data(**kwargs)

    def get_queryset(self):  #只做参数的查询
        story_list = Story.objects.all()
        print story_list
        return story_list

class HeroView(BaseMixin, ListView):
    template_name = 'time/hero.html'
    context_object_name = 'time'
    def get_context_data(self, **kwargs):
        pass
    def get_queryset(self):
        pass

class StoryView(BaseMixin, ListView):
    template_name = 'time/story.html'
    context_object_name = 'story'

    def get_context_data(self, **kwargs):

        _id = self.kwargs.get('id', '')
        _story = Story.objects.filter(id=_id)
        note_list = []
        temp_note_list = RelStoryNote.objects.filter(story=_id)
        for n in temp_note_list:
            note_list.append(n.note)
        kwargs['note_list'] = note_list
        kwargs['story_id'] = _id

        # print _id
        return super(StoryView, self).get_context_data(**kwargs)

    def get_queryset(self):
        _id = self.kwargs.get('id', '')
        story = Story.objects.get(id=_id)
        print story.title
        return story
        # article_list = Article.objects.filter(status=0)
        # return article_list



class AddStoryView(BaseMixin, ListView):
    template_name = 'time/add_story.html'
    def post(self, request, *args, **kwargs):
        _title = self.request.POST.get("title", "")
        _occur_date = self.request.POST.get("occur_date", "")
        _death_date = self.request.POST.get("death_date", "")
        _mirror = self.request.POST.get("mirror", "")

        #创建的story存在，跳转至页面
        if Story.objects.filter(title=_title).exists():
            _id = Story.objects.get(title=_title).id
            mydict = {"url": '/story/'+ str(_id) }

        #创建新story
        else:
            _newStory = Story(
                title = _title,
                # occur_date = _occur_date,
                # death_date = _death_date,
                mirror = _mirror
            )
            _newStory.save()
            _id = _newStory.id
            mydict = {"url": '/story/'+ str(_id) }
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )
        # return super(AddStoryView, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        return super(AddStoryView, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass


class AddNoteView(BaseMixin, ListView):
    template_name = 'time/add_note.html'
    context_object_name = 'note'

    def post(self, request, *args, **kwargs):
        print "OK"
        _story_id  = self.kwargs.get('story_id', '')
        # _story_id = self.request.POST.get("story_id", "")
        _occur_date = self.request.POST.get("occur_date", "")
        _mark = self.request.POST.get("mark", "")
        _description = self.request.POST.get("description", "")
        _style = int(self.request.POST.get("style", ""))
        # print "style" , _style
        #创建note（可以重复）
        _newNote = Note(
            occur_date = _occur_date,
            mark = _mark,
            description = _description,
            style = _style
        )
        _newNote.save()
        _note_id = _newNote.id

        # print "style1" , _style
        #story与note关系保存
        _story = Story.objects.get(id=_story_id)
        if RelStoryNote.objects.filter(story = _story, note = _newNote).exists() is False:
            _rel = RelStoryNote(
                story = _story,
                note = _newNote
            )
            _rel.save()

        #把获取的数据又传到前台
        mydict = {"url": '/story/'+ _story_id }
        print _story_id ,2
        # mydict = {
        #     "occur_date": _occur_date,
        #     "mark": _mark,
        #     "description": _description,
        #     "style": _style
        # }
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def get_context_data(self, **kwargs):
        kwargs['story_id']  = self.kwargs.get('story_id', '')
        return super(AddNoteView, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    # context_object_name = 'story'

#修改note
class EditorNoteView(BaseMixin, ListView):
    template_name = 'time/editor_note.html'
    context_object_name = 'note'

    #修改后的note
    def post(self, request, *args, **kwargs):
        _note_id = self.kwargs.get('note_id', '')
        _story_id  = self.kwargs.get('story_id', '')
        _occur_date = self.request.POST.get("occur_date", "")
        _mark = self.request.POST.get("mark", "")
        _description = self.request.POST.get("description", "")
        _style = int(self.request.POST.get("style", ""))

        #修改note
        _updateNote = Note.objects.get(id = _note_id )
        _updateNote.occur_date = _occur_date
        _updateNote.mark = _mark
        _updateNote.description = _description
        # print _mark,_description
        print _updateNote.style,_updateNote.description
        _updateNote.style = _style
        _updateNote.save()

        mydict = {"url": '/story/'+ _story_id }
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def get_context_data(self, **kwargs):
        kwargs['story_id']  = self.kwargs.get('story_id', '') #传入story的id
        return super(EditorNoteView, self).get_context_data(**kwargs)
    def get_queryset(self):
        _note_id = self.kwargs.get('note_id', '')
        note = Note.objects.get(id=_note_id)
        # print _note.mark
        return note
    # context_object_name = 'story'

#删除标签
class DeleteNoteView(BaseMixin, ListView):
    # template_name = 'time/editor_note.html'
    # context_object_name = 'note'

    def post(self, request, *args, **kwargs):
        _note_id = self.kwargs.get('note_id', '')
        _story_id  = self.kwargs.get('story_id', '')

        print Note.objects.filter(id=_note_id).exists()
        if  Note.objects.filter(id=_note_id).exists():
            _note = Note.objects.get(id=_note_id)
            _story = Story.objects.get(id=_story_id)
            _rel = RelStoryNote.objects.filter(story = _story, note = _note)
            _rel.delete()
            _note.delete()

        mydict = {"url": '/story/'+ _story_id }
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )



class ArticleView(BaseMixin, DetailView):
    queryset = Article.objects.filter(status=0)
    template_name = 'blog/article.html'
    context_object_name = 'article'
    slug_field = 'en_title'

    def get(self, request, *args, **kwargs):
        # 统计文章的访问访问次数
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        self.cur_user_ip = ip

        en_title = self.kwargs.get('slug')
        # 获取15*60s时间内访问过这篇文章的所有ip
        visited_ips = cache.get(en_title, [])

        # 如果ip不存在就把文章的浏览次数+1
        if ip not in visited_ips:
            try:
                article = self.queryset.get(en_title=en_title)
            except Article.DoesNotExist:
                logger.error(u'[ArticleView]访问不存在的文章:[%s]' % en_title)
                raise Http404
            else:
                article.view_times += 1
                article.save()
                visited_ips.append(ip)

            # 更新缓存
            cache.set(en_title, visited_ips, 15*60)

        return super(ArticleView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # 评论
        en_title = self.kwargs.get('slug', '')
        kwargs['comment_list'] = \
            self.queryset.get(en_title=en_title).comment_set.all()
        return super(ArticleView, self).get_context_data(**kwargs)


class AllView(BaseMixin, ListView):
    template_name = 'blog/all.html'
    context_object_name = 'article_list'

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all()
        kwargs['PAGE_NUM'] = PAGE_NUM
        return super(AllView, self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0)[0:PAGE_NUM]
        return article_list

    def post(self, request, *args, **kwargs):
        val = self.request.POST.get("val", "")
        sort = self.request.POST.get("sort", "time")
        start = self.request.POST.get("start", 0)
        end = self.request.POST.get("end", PAGE_NUM)

        start = int(start)
        end = int(end)

        if sort == "time":
            sort = "-pub_time"
        elif sort == "recommend":
            sort = "-view_times"
        else:
            sort = "-pub_time"

        if val == "all":
            article_list = \
                Article.objects.filter(status=0).order_by(sort)[start:end+1]
        else:
            try:
                article_list = Category.objects.get(
                                   name=val
                               ).article_set.filter(
                                   status=0
                               ).order_by(sort)[start:end+1]
            except Category.DoesNotExist:
                logger.error(u'[AllView]此分类不存在:[%s]' % val)
                raise PermissionDenied

        isend = len(article_list) != (end-start+1)

        article_list = article_list[0:end-start]

        html = ""
        for article in article_list:
            html += template.loader.get_template(
                        'blog/include/all_post.html'
                    ).render(template.Context({'post': article}))

        mydict = {"html": html, "isend": isend}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )


class SearchView(BaseMixin, ListView):
    template_name = 'blog/search.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM

    def get_context_data(self, **kwargs):
        kwargs['s'] = self.request.GET.get('s', '')
        return super(SearchView, self).get_context_data(**kwargs)

    def get_queryset(self):
        # 获取搜索的关键字
        s = self.request.GET.get('s', '')
        # 在文章的标题,summary和tags中搜索关键字
        article_list = Article.objects.only(
            'title', 'summary', 'tags'
        ).filter(
            Q(title__icontains=s) |
            Q(summary__icontains=s) |
            Q(tags__icontains=s),
            status=0
        )
        return article_list


class TagView(BaseMixin, ListView):
    template_name = 'blog/tag.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM

    def get_queryset(self):
        tag = self.kwargs.get('tag', '')
        article_list = \
            Article.objects.only('tags').filter(tags__icontains=tag, status=0)

        return article_list


class CategoryView(BaseMixin, ListView):
    template_name = 'blog/category.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM

    def get_queryset(self):
        category = self.kwargs.get('category', '')
        try:
            article_list = \
                Category.objects.get(name=category).article_set.all()
        except Category.DoesNotExist:
            logger.error(u'[CategoryView]此分类不存在:[%s]' % category)
            raise Http404

        return article_list


class UserView(BaseMixin, TemplateView):
    template_name = 'blog/user.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            logger.error(u'[UserView]用户未登陆')
            return render(request, 'blog/login.html')

        slug = self.kwargs.get('slug')

        if slug == 'changetx':
            self.template_name = 'blog/user_changetx.html'
            return super(UserView, self).get(request, *args, **kwargs)
        elif slug == 'changepassword':
            self.template_name = 'blog/user_changepassword.html'
            return super(UserView, self).get(request, *args, **kwargs)
        elif slug == 'changeinfo':
            self.template_name = 'blog/user_changeinfo.html'
            return super(UserView, self).get(request, *args, **kwargs)
        elif slug == 'message':
            self.template_name = 'blog/user_message.html'
            return super(UserView, self).get(request, *args, **kwargs)

        logger.error(u'[UserView]不存在此接口')
        raise Http404


class ColumnView(BaseMixin, ListView):
    queryset = Column.objects.all()
    template_name = 'blog/column.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM

    def get_context_data(self, **kwargs):
        column = self.kwargs.get('column', '')
        try:
            kwargs['column'] = Column.objects.get(name=column)
        except Column.DoesNotExist:
            logger.error(u'[ColumnView]访问专栏不存在: [%s]' % column)
            raise Http404

        return super(ColumnView, self).get_context_data(**kwargs)

    def get_queryset(self):
        column = self.kwargs.get('column', '')
        try:
            article_list = Column.objects.get(name=column).article.all()
        except Column.DoesNotExist:
            logger.error(u'[ColumnView]访问专栏不存在: [%s]' % column)
            raise Http404

        return article_list


class NewsView(BaseMixin, TemplateView):
    template_name = 'blog/news.html'

    def get_context_data(self, **kwargs):
        timeblocks = []

        # 获取开始和终止的日期
        start_day = self.request.GET.get("start", "0")
        end_day = self.request.GET.get("end", "6")
        start_day = int(start_day)
        end_day = int(end_day)

        start_date = datetime.datetime.now()

        # 获取url中时间断的资讯
        for x in range(start_day, end_day+1):
            date = start_date - datetime.timedelta(x)
            news_list = News.objects.filter(
                pub_time__year=date.year,
                pub_time__month=date.month,
                pub_time__day=date.day
            )

            if news_list:
                timeblocks.append(news_list)

        kwargs['timeblocks'] = timeblocks
        kwargs['active'] = start_day/7  # li中那个显示active

        return super(NewsView, self).get_context_data(**kwargs)
