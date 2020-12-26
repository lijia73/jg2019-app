from django.urls import path

import polls.views as views

urlpatterns = [
    path('', views.index, name='index'),
    #登录
    path('login/', views.login),
    #事件分析
    path('event/', views.event),
    #input event.id
    path('eventdetail/', views.eventdetail),
    #目标分析
    path('target/', views.target),
    #input target.id
    path('targetdetail/', views.targetdetail),
    #媒体监控
    path('media/', views.media),
    #input media.id
    path('mediadetail/', views.mediadetail),    
    #文本分析
    path('article/', views.article),
    #input article.id
    path('articledetail/', views.articledetail),
    #input files
    path('files/', views.files),
    #搜索方案
    path('plan/', views.plan),
    #input plan.id
    path('plandetail/', views.plandetail),
    #input plan
    path('uploadplan/', views.uploadplan),
    #图片管理
    #input source_name
    path('imagemanager/', views.imagemanager),
    path('imagebar/', views.imagebar),
    #知识图谱搜索
    #input txt file
    path('knowledgegraph/', views.knowledgegraph),
    #视频管理
    path('videomanager/', views.videomanager),
    path('videobar/', views.videobar),
    #返回图谱
    path('knowledgeoftarget/', views.knowledgeoftarget),

    #目标分析：关联事件图谱
    path('relatedeventimage/', views.relatedeventimage),
    
]

