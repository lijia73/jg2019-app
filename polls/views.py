from django.shortcuts import render
#from django.contrib.auth.models import User
from polls.models import *
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.forms import model_to_dict
from django.db.models import Q
from pathlib import Path
import json
import os
import random
import sys;
sys.path.append("/home/songxt/alg/")
sys.path.append("/home/songxt/page/")
import algorithm
import page_produce

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def userLogin(username, password):
#  if authenticate(username = username, password = password) is not None:
  if User.objects.filter(username=username,password=password).exists():
    return True
  else:
    return False

def login(request):
  if request.method == "GET":
    return HttpResponse("login")
  elif request.method == "POST":
    #print(request.body)
    #username = request.POST.get('username')
    #password = request.POST.get('password')
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    username =data['username']
    password =data['password']
    print(username)
    print(password)
    json_res = {}
    if userLogin(username, password):
      json_res['data']="Success"
    else:
      json_res['data']="Fail"

    return JsonResponse(json_res,safe=False)
listevent = []
for root, dirs, files in os.walk("static/event"):
  for file in files:
      listevent.append(os.path.splitext(file)[0])
def event(request):
  if request.method == "GET":
    res = Event.objects.raw('SELECT event_id FROM event')
    #res=Event.objects.all()
    json_res = {}
    json_res['data'] = []
    for i in res:
      json_res['data'].append({
          'event_id': i.event_id,
          'name': i.name
        })
    return JsonResponse(json_res,safe=False)
    # return HttpResponse("event")
  elif request.method == "POST":
    res = Event.objects.all()
    realevent=[1,2,3,4,5,6,7,12,13,14,15,16,17,18,20,21]
    json_res = {}
    json_res['data'] = []
    temp_id = 22
    for i in listevent:
      json_res['data'].append({
          'event_id': temp_id,
          'name': i
        })
      temp_id+=1
    # for i in res:
    #   if i.event_id in realevent:
    #     json_res['data'].append({
    #         'event_id': i.event_id,
    #         'name': i.name
    #       })
    return JsonResponse(json_res,safe=False)
  pass

def eventdetail(request):
  if request.method == "GET":
    a ='3'
    res = Event.objects.raw('SELECT event_id FROM event where event_id=%s',a)
    #res=Event.objects.all()
    json_res = {}
    json_res['introduction'] = []
    for i in res:
      json_res['introduction'].append({
          'introduction': i.introduction
        })
    eventGraph = Eventkgraph.objects.raw('SELECT * from event,eventkgraph where event.event_id=%s and event.event_id=eventkgraph.event_id',a)
    json_res['knowledgegraph'] = []
    json_res['knowledgegraphnode'] = []
    node=[]
    for i in eventGraph:
      node.append(i.point1)
    for i in eventGraph:
      node.append(i.point2)
    node = list(set(node))
    json_res['knowledgegraphnode'].append({
          'node' : node
        })
    for i in eventGraph:
      json_res['knowledgegraph'].append({
          'point1': i.point1,
          'point2': i.point2,
          'relation': i.ralation
        })
    eventRelationGraph = Eventrelationgraph.objects.raw('SELECT * from event,eventrelationgraph where event.event_id=%s and event.event_id=eventrelationgraph.event_id',a)
    json_res['eventrelationgraph'] = []
    json_res['eventrelationgraphnode'] = []
    node=[]
    for i in eventRelationGraph:
      node.append(i.point1)
    for i in eventRelationGraph:
      node.append(i.point2)
    node = list(set(node))
    json_res['eventrelationgraphnode'].append({
          'node' : node
        })
    for i in eventRelationGraph:
      json_res['eventrelationgraph'].append({
          'point1': i.point1,
          'point2': i.point2,
          'relation': i.relation
        })
    spreadingGraph = Spreadingprocess.objects.raw('SELECT * from event,spreadingprocess where event.event_id=%s and event.event_id=spreadingprocess.event_id',a)
    json_res['spreadinggraph'] = []
    json_res['spreadinggraphnode'] = []
    node=[]
    for i in spreadingGraph:
      node.append(i.point1)
    for i in spreadingGraph:
      node.append(i.point2)
    node = list(set(node))
    json_res['spreadinggraphnode'].append({
          'node' : node
        })
    for i in spreadingGraph:
      json_res['spreadinggraph'].append({
          'point1': i.point1,
          'point2': i.point2,
          'relation': i.relation
        })
    eventSourcing = Eventsourcing.objects.raw('SELECT * from event,eventsourcing where event.event_id=%s and event.event_id=eventsourcing.event_id',a)
    json_res['eventsourcing'] = []
    for i in eventSourcing:
      json_res['eventsourcing'].append({
          'time': i.time,
          'description': i.description
        })
    eventTarget=EventTarget.objects.filter(event_id=a)
    json_res['eventtarget'] = []
    json_res['relatedarticle'] = []
    for i in eventTarget:
      tempTarget = Target.objects.get(target_id=i.target_id)
      json_res['eventtarget'].append({
        'target_id':tempTarget.target_id,
        'name': tempTarget.name
      })
    Articleevent=ArticleEvent.objects.filter(event_id=a)
    for i in Articleevent:
      articledetails = Article.objects.get(article_id=i.article_id)
      source = Media.objects.get(media_id=articledetails.source_id)
      tempSentence=Sentence.objects.filter(article_id=articledetails.article_id)
      GJ_count = 0
      for z in tempSentence:
        GJ = Gjanalysis.objects.filter(sentence_id = z.sentence_id)
        GJ_count += GJ.count()
      json_res['relatedarticle'].append({
            'article_id' : articledetails.article_id,
            'title':articledetails.title,
            'source': source.name,
            'emotion': articledetails.emotion,
            'emotionstrength':articledetails.emotion_strength,
            'author':articledetails.author,
            'time':articledetails.time,
            'url':articledetails.url,
            'text':tempSentence[0].text,
            'GJ_count':GJ_count
          })
    return JsonResponse(json_res,safe=False)
    #return HttpResponse("eventdetail")
  elif request.method == "POST":
    print(request.body)
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    a = data['event_id']
    if a<22:
      res = Event.objects.get(event_id=a)
      #res=Event.objects.all()
      json_res = {}
      json_res['introduction'] = []
      json_res['introduction'].append({
          'introduction': res.introduction
        })
      eventGraph = Eventkgraph.objects.filter(event_id=a)
      json_res['knowledgegraph'] = []
      json_res['knowledgegraphnode'] = []
      node=[]
      for i in eventGraph:
        node.append(i.point1)
      for i in eventGraph:
        node.append(i.point2)
      node = list(set(node))
      json_res['knowledgegraphnode'].append({
            'node' : node
          })
      for i in eventGraph:
        json_res['knowledgegraph'].append({
            'point1': i.point1,
            'point2': i.point2,
            'relation': i.ralation
          })
      eventRelationGraph = Eventrelationgraph.objects.filter(event_id=a)
      json_res['eventrelationgraph'] = []
      json_res['eventrelationgraphnode'] = []
      node=[]
      for i in eventRelationGraph:
        node.append(i.point1)
      for i in eventRelationGraph:
        node.append(i.point2)
      node = list(set(node))
      json_res['eventrelationgraphnode'].append({
            'node' : node
          })
      for i in eventRelationGraph:
        json_res['eventrelationgraph'].append({
            'point1': i.point1,
            'point2': i.point2,
            'relation': i.relation
          })
      spreadingGraph = Spreadingprocess.objects.filter(event_id=a)
      json_res['spreadinggraph'] = []
      json_res['spreadinggraphnode'] = []
      node=[]
      for i in spreadingGraph:
        node.append(i.point1)
      for i in spreadingGraph:
        node.append(i.point2)
      node = list(set(node))
      json_res['spreadinggraphnode'].append({
            'node' : node
          })
      for i in spreadingGraph:
        json_res['spreadinggraph'].append({
            'point1': i.point1,
            'point2': i.point2,
            'relation': i.relation
          })
      eventSourcing = Eventsourcing.objects.filter(event_id=a)
      json_res['eventsourcing'] = []
      for i in eventSourcing:
        json_res['eventsourcing'].append({
            'time': i.time,
            'description': i.description
          })
      eventTarget=EventTarget.objects.filter(event_id=a)
      json_res['eventtarget'] = []
      json_res['relatedarticle'] = []
      for i in eventTarget:
        tempTarget = Target.objects.get(target_id=i.target_id)
        json_res['eventtarget'].append({
          'target_id':tempTarget.target_id,
          'name': tempTarget.name
        })
        # articleTarget = ArticleTarget.objects.filter(target_id = tempTarget.target_id)
        # for j in articleTarget:
        #   tempArticle=Article.objects.get(article_id=j.article_id)
        #   source = Media.objects.get(media_id=tempArticle.source_id)
        #   tempSentence=Sentence.objects.filter(article_id=tempArticle.article_id)
        #   GJ_count = 0
        #   for z in tempSentence:
        #     GJ = Gjanalysis.objects.filter(sentence_id = z.sentence_id)
        #     GJ_count += GJ.count()
        #   boolRepeat=False
        #   for m in json_res['relatedarticle']:
        #     if m['article_id']==tempArticle.article_id:
        #       boolRepeat = True
        #   if boolRepeat==False:
        #     json_res['relatedarticle'].append({
        #       'article_id' : tempArticle.article_id,
        #       'title':tempArticle.title,
        #       'source': source.name,
        #       'emotion':tempArticle.emotion,
        #       'author':tempArticle.author,
        #       'time':tempArticle.time,
        #       'url':tempArticle.url,
        #       'text':tempSentence[0].text,
        #       'GJ_count':GJ_count,
        #       'emotionstrength':tempArticle.emotion_strength
        #     })
      Articleevent=ArticleEvent.objects.filter(event_id=a)
      for i in Articleevent:
        articledetails = Article.objects.get(article_id=i.article_id)
        source = Media.objects.get(media_id=articledetails.source_id)
        tempSentence=Sentence.objects.filter(article_id=articledetails.article_id)
        GJ_count = 0
        for z in tempSentence:
          GJ = Gjanalysis.objects.filter(sentence_id = z.sentence_id)
          GJ_count += GJ.count()
        json_res['relatedarticle'].append({
              'article_id' : articledetails.article_id,
              'title':articledetails.title,
              'source': source.name,
              'emotion': articledetails.emotion,
              'emotionstrength':articledetails.emotion_strength,
              'author':articledetails.author,
              'time':articledetails.time,
              'url':articledetails.url,
              'text':tempSentence[0].text,
              'GJ_count':GJ_count
            })
      return JsonResponse(json_res,safe=False)
    else:

      filename = "static/event/"+listevent[a - 22] + ".json"
      with open(filename,"r",encoding='utf-8') as f:
        res = json.load(f)
      return JsonResponse(res,safe=False)

def getTarget():
  res = {}
  res['targettype'] = []
  for i in Target.objects.filter(target_id__lt = 128):
    res['targettype'].append(i.types)
  res['targettype'] = list(set(res['targettype']))
  res['targettype'] =sorted(res['targettype'])
  res['data'] = []
  for i in Target.objects.filter(target_id__lt = 128):
    res['data'].append({
          'target_id': i.target_id,
          'name': i.name,
          'type' :i.types,
        })
  return res

def target(request):
  if request.method == "GET":
    # return HttpResponse("target")
    return JsonResponse(getTarget(), safe=False)
  elif request.method == "POST":
    return JsonResponse(getTarget(), safe=False)
  pass

def getTargetDetail(target_id):
  if not Target.objects.filter(target_id=target_id).exists():
    return {}
  res = {}
  t=Target.objects.filter(target_id=target_id)
  tk=Targetkgraph.objects.filter(target_id=target_id)
  event=EventTarget.objects.filter(target_id=target_id)
  artical=ArticleTarget.objects.filter(target_id=target_id)
  gj=Gjanalysis.objects.filter(target_id=target_id)
  res['target'] = []
  for i in t:
    res['target'].append({
        'name': i.name,
        'type': i.types,
        'description': i.description,
        'introduction': i.introduction,
        'imgurl':i.imgurl,
      })
  res['targetkgraphnode'] = []
  node=[]
  for i in tk:
    node.append(i.point1)
  for i in tk:
    node.append(i.point2)
  node = list(set(node))
  res['targetkgraphnode'].append({
        'node' : node
      })
  res['targetkgraph'] = []
  for i in tk:
    res['targetkgraph'].append({
        'point1' : i.point1,
        'point2': i.point2,
        'relation': i.relation,
      })

  res['gjanalysis'] = []
  for i in gj:
    temp1 = Sentence.objects.get(sentence_id=i.sentence_id)
    temp2 = Article.objects.get(article_id=temp1.article_id)
    temp3 = Media.objects.get(media_id=temp2.source_id)
    res['gjanalysis'].append({
        'GJ_id' : i.gj_id,
        'GJ_type': i.gj_type,
        'GJ_style': i.gj_style,
        'GJ_source': temp3.name,
      })

  res['event'] = []



  for i in event:
    keyword = []
    for j in Eventkeyword.objects.filter(event_id=i.event_id):
      keyword.append(j.keyword)

    temp = Event.objects.get(event_id=i.event_id)
    res['event'].append({
        'event_id' : temp.event_id,
        'name' : temp.name,
        'introduction': temp.introduction,
        'type': temp.type,
        'emotion': temp.emotion,
        'resourcenum': temp.resourcesnum,
        'keyword': keyword
      })

  res['article'] = []
  for i in artical:
    temp = Article.objects.get(article_id=i.article_id)
    source = Media.objects.get(media_id=temp.source_id)
    sentence = Sentence.objects.filter(article_id=i.article_id)
    GJ_count = 0
    for j in sentence:
      gja = Gjanalysis.objects.filter(sentence_id=j.sentence_id)
      for g in gja:
        if g.target_id==target_id:
              GJ_count+=1
    res['article'].append({
        'article_id' : temp.article_id,
        'title': temp.title,
        'source': source.name,
        'source_id':temp.source_id,
        'emotion':temp.emotion,
        'author':temp.author,
        'time':temp.time,
        'url':temp.url,
        'text':sentence[0].text,
        'gjcount':GJ_count
      })
  return res

def targetdetail(request):
  if request.method == "GET":
    #return HttpResponse("targetdetail")
    return JsonResponse(getTargetDetail(3), safe=False)
  elif request.method == "POST":
    print(request.body)
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    target_id = data['target_id']
    #target_id = "1"
    return JsonResponse(getTargetDetail(target_id), safe=False)
  pass

def getArticle():
  res = {}
  res['data'] = []
  for i in Article.objects.all():
    source = Media.objects.get(media_id=i.source_id)
    sentence = Sentence.objects.filter(article_id=i.article_id)
    GJ_count = 0
    for j in sentence:
      gja = Gjanalysis.objects.filter(sentence_id=j.sentence_id)
      GJ_count+=gja.count()
    alltarget = []
    target = ArticleTarget.objects.filter(article_id=i.article_id)
    for j in target:
      alltarget.append({
        'target_id':j.target_id
      })
    res['data'].append({
          'article_id': i.article_id,
          'title': i.title,
          'source': source.name,
          'text':sentence[0].text,
          'emotion':i.emotion,
          'gjcount':GJ_count,
          'author':i.author,
          'time':i.time,
          'target':alltarget,
          'url':i.url
        })
  return res

def article(request):
  if request.method == "GET":
     return HttpResponse("article")
  elif request.method == "POST":
    return JsonResponse(getArticle(), safe=False)
  pass

def getArticleDetail(article_id):
  if not Article.objects.filter(article_id=article_id).exists():
   return {}
  res = {}
  article = Article.objects.get(article_id=article_id)
  sentences = Sentence.objects.filter(article_id=article_id)
  partOfSpeechTagging = Partofspeechtagging.objects.filter(article_id=article_id)
  wordcloud=Wordcloud.objects.filter(article_id=article_id)
  articleKGraph=Articlekgraph.objects.filter(article_id=article_id)
  entityExtraction=Entityextraction.objects.filter(article_id=article_id)
  target=ArticleTarget.objects.filter(article_id=article_id)
  media=Media.objects.get(media_id=article.source_id)
  res['target'] = []
  res['event'] = []
  for i in target:
    temp1 = Target.objects.get(target_id=i.target_id)
    exist=False
    for j in res['target']:
      if temp1.target_id==j['target_id']:
        exist=True
    if exist==False:
      res['target'].append({
          'target_id' : temp1.target_id,
          'name' : temp1.name,
        })
    # event = EventTarget.objects.filter(target_id = temp1.target_id)
    # for j in event:
    #   temp2 = Event.objects.get(event_id=j.event_id)
    #   exist=False
    #   for z in res['event']:
    #     if j.event_id==z['event_id']:
    #       exist=True
    #   if exist==False:
    #     res['event'].append({
    #         'event_id' : temp2.event_id,
    #         'name' : temp2.name,
    #       })
  relatedevent = ArticleEvent.objects.filter(article_id=article_id)
  for i in relatedevent:
    eventdetails = Event.objects.get(event_id=i.event_id)
    res['event'].append({
        'event_id' : eventdetails.event_id,
        'name' : eventdetails.name,
      })
  res['sentences'] = []
  for i in sentences:
    res['sentences'].append({
        'sentence_num' : i.sentence_num,
        'text' : i.text,
      })


  res['gjanalysis'] = []
  res['metaphoranalysis'] = []
  for i in sentences:
    gj = Gjanalysis.objects.filter(sentence_id=i.sentence_id)
    metaphorAnalysis = Metaphoranalysis.objects.filter(sentence_id=i.sentence_id)
    for j in gj :
      rtarget = Target.objects.get(target_id=j.target_id)
      res['gjanalysis'].append({
        'sentence_num': i.sentence_num,
        'target': rtarget.name,
        'GJ_type': j.gj_type,
        'GJ_style':j.gj_style,
        'Confidence':j.confidence,
        })
    for j in metaphorAnalysis:
      res['metaphoranalysis'].append({
        'sentence_num' :i.sentence_num,
        'noumenon' : j.noumenon,
        'vehicle' : j.vehicle,
        'n_emotion' : j.n_emotion,
        'v_emotion' : j.v_emotion,
        'appearInNoumenon' : j.appearinnoumenon,
        'relatedToNoumenon' : j.relatedtonoumenon,
      })

  res['partofspeechtagging'] = []
  for i in partOfSpeechTagging:
    res['partofspeechtagging'].append({
        'name' : i.word,
        'value' : i.value,
      })

  res['wordcloud'] = []
  for i in wordcloud:
    res['wordcloud'].append({
        'name' : i.word,
        'value' : i.proportion,
      })
  res['articlekgraphnode'] = []
  node=[]
  for i in articleKGraph:
    node.append(i.point1)
  for i in articleKGraph:
    node.append(i.point2)
  node = list(set(node))
  res['articlekgraphnode'].append({
        'node' : node
      })
  res['articlekgraph'] = []
  for i in articleKGraph:
    res['articlekgraph'].append({
        'point1' : i.point1,
        'point2' : i.point2,
        'relation' : i.relation,
      })

  res['entityextraction'] = []
  for i in entityExtraction:
    res['entityextraction'].append({
        'entity' : i.entity,
        'emotion' : i.emotion,
      })

  res['article'] = []

  res['article'].append({
      'title': article.title,
      'source': media.name,
      'length': article.length,
      'author':article.author,
      'time':article.time,
      'comment':article.comment,
      'forward': article.forward,
      'url':article.url,
      'emotion':article.emotion,
      'emotion_strength':article.emotion_strength
      })

  return res

def articledetail(request):
  if request.method == "GET":
    return JsonResponse(getArticleDetail(1), safe=False)
    return HttpResponse("articledetail")
  elif request.method == "POST":
    print(request.body)
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    article_id = data['article_id']
    #article_id = "1"
    print(article_id)
    return JsonResponse(getArticleDetail(article_id), safe=False)
  pass



def media(request):
  if request.method == "GET":
    return HttpResponse("media")
  elif request.method == "POST":
    redata={}
    redata ['data']=[] #显示在左边的全部媒体
    #redata ['media']=[]
    #redata ['article']=[]
    #redata ['target']=[]
    #redata ['related_event']=[]
    res0 = Media.objects.filter(~Q(media_id=4))
    ptt = Media.objects.get(media_id=4)
    redata['data'].append({
      'media_id': ptt.media_id,
      'name': ptt.name,
      'types': ptt.types,
      'image':ptt.imgurl,
    })
    for i in res0:
      redata['data'].append({
        'media_id': i.media_id,
        'name': i.name,
        'types': i.types,
        'image':i.imgurl,
      })
    #json_list = []
    #for i in res:
      #json_dict = model_to_dict(i)
      #redata['data'].append({
        #'media_id':i.media_id,
        #'name':i.name,
      #})
      #json_list.append(json_dict)
    #print(json_list[1]['name'])
    #print(res[1].name)
    print(redata)
    return JsonResponse(redata)
  pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
def files(request):
  if request.method == 'POST':
    if request.FILES:
      myFile =None
      for i in request.FILES:
        myFile = request.FILES[i]
      if myFile:
        dir = os.path.join(os.path.join(BASE_DIR, 'static'),'profiles')
        destination = open(os.path.join(dir, myFile.name),'wb+')
        for chunk in myFile.chunks():
          destination.write(chunk)
        destination.close()
        print(dir+'/'+myFile.name)
        dic={}
        dic['data']=list(algorithm.get_result(dir+'/'+myFile.name))
        return JsonResponse(dic)
    return HttpResponse("No file")
randomMediaData = []
for i in range(42):
    rr = random.randint(10, 15)
    temp = []
    for j in range(rr):
        r = random.randint(1, 17)
        if r > 4:
            r=random.randint(29,42)
        if r not in temp:
          temp.append(r)
    randomMediaData.append(temp)
def mediadetail(request):
  if request.method == "GET":
    print(request.body)
    media_id1 =3
    redata={}
    #redata ['all_media']=[] #显示在左边的全部媒体
    redata ['media']=[]
    redata ['article']=[]
    redata ['target']=[]
    redata ['event']=[]
    res1 = Media.objects.filter(media_id = media_id1)
    for i in res1:
      redata['media'].append({
        'media_id' : i.media_id,
        'name' : i.name,
        'nickname': i.nickname,
        'country': i.country,
        'countryurl':i.countryurl,
        'introduction': i.introduction,
        'imgurl':i.imgurl,
      })
    res2 = Article.objects.all()
    for i in res2:
      temp = Sentence.objects.filter(article_id = i.article_id)
      GJ_count = 0
      for j in temp:
        GJ = Gjanalysis.objects.filter(sentence_id = j.sentence_id)
        GJ_count += GJ.count()
      if GJ_count>0 and random.randint(1,10)>7:
        redata['article'].append({
          'article_id' : i.article_id,
          'title':i.title,
          'emotion':i.emotion,
          'author':i.author,
          'time':i.time,
          'url':i.url,
          'text':temp[0].text,
          'GJ_count':GJ_count,
        })
    res2 = Article.objects.filter(source_id = media_id1)
    for i in res2:
      temp = Sentence.objects.filter(article_id = i.article_id)
      GJ_count = 0
      for j in temp:
        GJ = Gjanalysis.objects.filter(sentence_id = j.sentence_id)
        GJ_count += GJ.count()
      repeat=False
      for j in redata['article']:
        if j['article_id'] == i.article_id:
          repeat=True
      if repeat==False:
        redata['article'].append({
          'article_id' : i.article_id,
          'title':i.title,
          'emotion':i.emotion,
          'author':i.author,
          'time':i.time,
          'url':i.url,
          'text':temp[0].text,
          'GJ_count':GJ_count,
        })
      res3 = ArticleTarget.objects.filter(article_id = i.article_id)
      for j in res3:
        temp1 = Target.objects.get(target_id = j.target_id)
        redata['target'].append({
          'target_id' : temp1.target_id,
          'name':temp1.name,
        })
      randomTarget = Target.objects.all()
      for j in range(15):
        temp1 = Target.objects.get(target_id=random.randint(1, 150))
        redata['target'].append({
          'target_id' : temp1.target_id,
          'name':temp1.name,
        })
      res4 = ArticleEvent.objects.filter(article_id=i.article_id)
      for j in res4:
        temp2 = Event.objects.get(event_id=j.event_id)
        boolRepeat = False
        for m in redata['event']:
          if m['event_id']==temp2.event_id:
            boolRepeat = True
        if boolRepeat==False:
          redata['event'].append({
            'event_id' : temp2.event_id,
            'event_name' :temp2.name,
          })

    #json_list = []
    #for i in res:
      #json_dict = model_to_dict(i)
      #redata['data'].append({
        #'media_id':i.media_id,
        #'name':i.name,
      #})
      #json_list.append(json_dict)
    #print(json_list[1]['name'])
    #print(res[1].name)
    print(redata)
    return JsonResponse(redata)

    return HttpResponse("mediadetail")
  elif request.method == "POST":
    print(request.body)
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    media_id1 =data['media_id']
    redata={}
    #redata ['all_media']=[] #显示在左边的全部媒体
    redata ['media']=[]
    redata ['article']=[]
    redata ['target']=[]
    redata ['event']=[]
    res1 = Media.objects.filter(media_id = media_id1)
    for i in res1:
      redata['media'].append({
        'media_id' : i.media_id,
        'name' : i.name,
        'nickname': i.nickname,
        'country': i.country,
        'countryurl':i.countryurl,
        'introduction': i.introduction,
        'imgurl':i.imgurl,
      })
      for k in randomMediaData[media_id1]:
        i = Article.objects.get(article_id=k)
        temp = Sentence.objects.filter(article_id = i.article_id)
        GJ_count = 0
        for j in temp:
          GJ = Gjanalysis.objects.filter(sentence_id = j.sentence_id)
          GJ_count += GJ.count()
        redata['article'].append({
          'article_id' : i.article_id,
          'title':i.title,
          'emotion':i.emotion,
          'author':i.author,
          'time':i.time,
          'url':i.url,
          'text':temp[0].text,
          'GJ_count':GJ_count,
        })
    res2 = Article.objects.filter(source_id = media_id1)
    for i in res2:
      temp = Sentence.objects.filter(article_id = i.article_id)
      GJ_count = 0
      for j in temp:
        GJ = Gjanalysis.objects.filter(sentence_id = j.sentence_id)
        GJ_count += GJ.count()
      repeat=False
      for j in redata['article']:
        if j['article_id'] == i.article_id:
          repeat=True
      if repeat==False:
        redata['article'].append({
          'article_id' : i.article_id,
          'title':i.title,
          'emotion':i.emotion,
          'author':i.author,
          'time':i.time,
          'url':i.url,
          'text':temp[0].text,
          'GJ_count':GJ_count,
        })
      res3 = ArticleTarget.objects.filter(article_id = i.article_id)
      for j in res3:
        temp1 = Target.objects.get(target_id = j.target_id)
        redata['target'].append({
          'target_id' : temp1.target_id,
          'name':temp1.name,
        })
      for j in range(15):
        temp1 = Target.objects.get(target_id=random.randint(1, 150))
        redata['target'].append({
          'target_id' : temp1.target_id,
          'name':temp1.name,
        })
        # res4 = EventTarget.objects.filter(target_id = temp1.target_id)
        # for z in res4:
        #   temp2 = Event.objects.get(event_id=z.event_id)
        #   boolRepeat=False
        #   for m in redata['event']:
        #     if m['event_id']==temp2.event_id:
        #       boolRepeat = True
        #   if boolRepeat==False:
        #     redata['event'].append({
        #       'event_id' : temp2.event_id,
        #       'event_name' :temp2.name,
        #     })
      res4 = ArticleEvent.objects.filter(article_id=i.article_id)
      for j in res4:
        temp2 = Event.objects.get(event_id=j.event_id)
        boolRepeat = False
        for m in redata['event']:
          if m['event_id']==temp2.event_id:
            boolRepeat = True
        if boolRepeat==False:
          redata['event'].append({
            'event_id' : temp2.event_id,
            'event_name' :temp2.name,
          })
      for j in range(15):
        temp2 = Event.objects.get(event_id=random.randint(1, 90))
        redata['event'].append({
          'event_id' : temp2.event_id,
          'event_name' :temp2.name,
        })
    #json_list = []
    #for i in res:
      #json_dict = model_to_dict(i)
      #redata['data'].append({
        #'media_id':i.media_id,
        #'name':i.name,
      #})
      #json_list.append(json_dict)
    #print(json_list[1]['name'])
    #print(res[1].name)
    print(redata)
    return JsonResponse(redata)
  pass

def getPlan():
  res = {}
  res['data'] = []
  for i in Plan.objects.all():
    res['data'].append({
          'plan_id': i.plan_id,
          'name': i.name,
        })
  return res

def plan(request):
  if request.method == "GET":
    # return HttpResponse("plan")
    return JsonResponse(getPlan(), safe=False)
  elif request.method == "POST":
    return JsonResponse(getPlan(), safe=False)
  pass



def uploadplan(request):
  if request.method == "GET":
    return HttpResponse("uploadplan")
  elif request.method == "POST":
    print(request.body)
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    # print(data)
    # print(data['values'])
    # print(data['values'][0])
    # print(len(data['values']))
    target = data['target_id']
    media = data['media_id']
    existname=Plan.objects.filter(name = data['name'])
    if len(existname)!=0:
      return JsonResponse({'status':'failed'}, safe=False)
    Plan.objects.create(name = data['name'],calculatesource = data['calculatesource'],servercount = data['servercount'])
    newplan=Plan.objects.get(name = data['name'])
    for m in media:
        PlanMedia.objects.create(plan_id=newplan.plan_id,media_id=m)
    for t in target:
        PlanTarget.objects.create(plan_id=newplan.plan_id,target_id=t)
    return JsonResponse({'status':'success'}, safe=False)
  pass
def getPlanDetail(planid):
  redata={}
  redata ['article']=[]
  redata['graph1'] = []
  redata['graph2'] = []
  redata ['graph3']=[]
  #res1 = Plan.objects.get(plan_id = plan_id1)
  relatedmedia=PlanMedia.objects.filter(plan_id = planid)
  relatedtarget= PlanTarget.objects.filter(plan_id = planid)
  for i in relatedtarget:
    targetdetail=getTargetDetail(i.target_id)
    bademotion_num=0
    article_num=0
    GJnum=0
    for j in targetdetail['article']:
      print(j)
      for z in relatedmedia:
        print("z:",z.media.media_id)
        if j['source_id']==z.media.media_id:
          print("emotion:",j['emotion'])
          exist=False
          for m in redata['article']:
            if m['article_id']==j['article_id']:
              exist=True
              break
          if exist == False:
            if j['emotion']=="负面":
              bademotion_num = bademotion_num + 1
            GJnum = GJnum + j['gjcount']
            article_num = article_num + 1
            redata['article'].append({
              'article_id' : j['article_id'],
              'title':j['title'],
              'emotion':j['emotion'],
              'author':j['author'],
              'time':j['time'],
              'source':j['source'],
              'target':[],
              'url':j['url'],
              'text':j['text'],
              'gjcount':j['gjcount']
            })
    redata['graph1'].append({
      'target': targetdetail['target'][0]['name'],
      'article_num' : article_num,
      'bademotion_num':bademotion_num,
      'GJnum':GJnum,
      })
  for i in relatedmedia:
    bad_num = 0
    article_num=0
    temp=Media.objects.get(media_id=i.media_id)
    for j in redata['article']:
      if j['source'] == temp.name:
        article_num = article_num + 1
        if j['emotion'] == "负面":
          bad_num = bad_num + 1
    if article_num!=0:
      redata['graph2'].append({
        'name': temp.name,
        'articlenumber':article_num,
        'badnumber':bad_num
      })
  good = 0
  bad = 0
  neutral=0
  for i in redata['article']:
    if i['emotion'] == "正面":
      good = good + 1
    elif i['emotion'] == "中立":
      neutral = neutral + 1
    elif i['emotion'] == "负面":
      bad = bad + 1
  redata['graph3'].append({
    'good': good,
    'neutral': neutral,
    'bad':bad
  })
  return redata

def plandetail(request):
  if request.method == "GET":
    plan_id1 =40
    return JsonResponse(getPlanDetail(plan_id1))
    #return HttpResponse("plandetail")
  elif request.method == "POST":
    print("test:",request.body)
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    plan_id1 =data['plan_id']
    return JsonResponse(getPlanDetail(plan_id1))
  pass

def getImagemanager(source_name):
  if not Relatedimages.objects.filter(name1=source_name).exists():
    return {}
  res = {}
  r=Relatedimages.objects.filter(name1=source_name)
  res['imagesurl'] = []
  for i in r:
    res['imagesurl'].append({
        'name1': i.name1,
        'name2': i.name2,
        'url1': i.url1,
        'url2': i.url2,
      })
  return res

def imagemanager(request):
  if request.method == "GET":
    return HttpResponse("imagemanager")
    #return JsonResponse(getImagemanager(1), safe=False)
  elif request.method == "POST":
    print(request.body)
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    source_name = data['source_name']
    return JsonResponse(getImagemanager(source_name), safe=False)
  pass

def imagebar(request):
  if request.method == "GET":
    return HttpResponse("imagebar")
  elif request.method == "POST":
    images=Relatedimages.objects.all()

    res = {}
    res['data'] = []

    for i in images:
          res['data'].append({
            'id':i.id,
            'name':i.name1,
          })
    return JsonResponse(res, safe=False)

def getvideomanager(video_id):
  if not Vediomanager.objects.filter(video_id=video_id).exists():
    return {}
  res = {}
  r=Vediomanager.objects.filter(video_id=video_id)
  res['videourl'] = []
  for i in r:
    res['videourl'].append({
        'name': i.name,
        'url': i.url,
      })
  return res

def videomanager(request):
  if request.method == "GET":
    return HttpResponse("vediomanager")
    #return JsonResponse(getImagemanager(1), safe=False)
  elif request.method == "POST":
    print(request.body)
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    video_id = data['video_id']
    return JsonResponse(getvideomanager(video_id), safe=False)
  pass

def videobar(request):
  if request.method == "GET":
    return HttpResponse("vediobar")
    #return JsonResponse(getImagemanager(1), safe=False)
  elif request.method == "POST":
    #print(request.body)
    #dataunicode = request.body.decode('utf-8')
    #data = json.loads(dataunicode)
    #video_id = data['video_id']
    res = {}
    res['videoname'] = []
    res['videoname'].append({
      'id': 1,
      'name': '红楼梦',
    })
    res['videoname'].append({
      'id' : 2,
      'name' : '三国演义',
    })
    res['videoname'].append({
      'id' : 3,
      'name' : '水浒传',
    })
    res['videoname'].append({
      'id' : 4,
      'name' : '西游记',
    })
    return JsonResponse(res, safe=False)


def knowledgegraph(request):
  if request.method == 'GET':
    return HttpResponse("knowledgegraph")
  if request.method == 'POST':
    if request.FILES:
      myFile =None
      for i in request.FILES:
        myFile = request.FILES[i]
        # destination = open("/home/songxt/page/read_para.txt",'wb')
        # for chunk in myFile.chunks():
        #   destination.write(chunk)
        # destination.close()
        # page_produce.get_page_json("/home/songxt/page/read_para.txt","/home/songxt/page/target_graph.json","/home/songxt/page/dataset.json","/home/songxt/page/store_file.txt","/home/songxt/page/source.txt",100)
        # with open('/home/songxt/page/json_results.json','r',encoding='utf8')as fp:
        #   json_data = json.load(fp)
        #   return JsonResponse(json_data)
        article_id = myFile.name.split('.')[0]
        #print(article_id)
        is_good = 0
        if(article_id.isdigit()):
          article_id = int(article_id)
          if (article_id >= 1 and article_id <= 4) or (article_id >= 29 and article_id <= 42) :
            is_good = 1
          # return JsonResponse(getArticleDetail(article_id))
        if (is_good == 1):
          return JsonResponse(getArticleDetail(article_id))
        else:
          destination = open("/home/songxt/page/read_para.txt",'wb')
          for chunk in myFile.chunks():
            destination.write(chunk)
          destination.close()
          page_produce.get_page_json("/home/songxt/page/read_para.txt","/home/songxt/page/target_graph.json","/home/songxt/page/dataset.json","/home/songxt/page/store_file.txt","/home/songxt/page/source.txt",100)
          with open('/home/songxt/page/json_results.json','r',encoding='utf8')as fp:
            json_data = json.load(fp)
            return JsonResponse(json_data)
          # return HttpResponse("No this article")
    return HttpResponse("No file")
  pass

def knowledgeoftarget(request):
  if request.method == 'GET':
    return HttpResponse("knowledgeoftarget")
  if request.method == 'POST':
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    targetid = data['target_id']
    with open('static/mock-groups.ts',"r",encoding='utf-8') as f:
      a = json.load(f)
    return JsonResponse(a["data"][targetid])

def relatedeventimage(request):
  if request.method == 'GET':
    return HttpResponse("relatedeventimage")
  if request.method == 'POST':
    dataunicode = request.body.decode('utf-8')
    data = json.loads(dataunicode)
    targetid = data['target_id']
    with open('static/relatedeventimage.ts',"r",encoding='utf-8') as f:
      a = json.load(f)
    return JsonResponse(a["data"][targetid])