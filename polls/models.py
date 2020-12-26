# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `#managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# from django.contrib.auth.models import User


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    comment = models.CharField(max_length=45, blank=True, null=True)
    forward = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    source = models.ForeignKey('Media', models.DO_NOTHING)
    emotion = models.CharField(max_length=45)
    emotion_strength = models.IntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'article'

class ArticleEvent(models.Model):
    article = models.ForeignKey(Article, models.DO_NOTHING, blank=True, null=True)
    event = models.ForeignKey('Event', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article-event'

class ArticleTarget(models.Model):
    article = models.ForeignKey(Article, models.DO_NOTHING)
    target = models.ForeignKey('Target', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'article-target'


class Articlekgraph(models.Model):
    article = models.ForeignKey(Article, models.DO_NOTHING)
    point1 = models.CharField(max_length=45)
    point2 = models.CharField(max_length=45)
    relation = models.CharField(max_length=45)

    class Meta:
        #managed = False
        db_table = 'articlekgraph'


class Emotionalanalysis(models.Model):
    article = models.ForeignKey(Article, models.DO_NOTHING)
    emotion1 = models.CharField(max_length=45, blank=True, null=True)
    emotion2 = models.CharField(max_length=45, blank=True, null=True)
    emotion3 = models.CharField(max_length=45, blank=True, null=True)
    rate1 = models.FloatField(blank=True, null=True)
    rate2 = models.FloatField(blank=True, null=True)
    rate3 = models.FloatField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'emotionalanalysis'


class Emotionaldistribution(models.Model):
    target = models.ForeignKey('Target', models.DO_NOTHING)
    emotion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'emotionaldistribution'


class Entityextraction(models.Model):
    article = models.ForeignKey(Article, models.DO_NOTHING)
    entity = models.CharField(max_length=45)
    emotion = models.CharField(max_length=45)

    class Meta:
        #managed = False
        db_table = 'entityextraction'

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    introduction = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    emotion = models.CharField(max_length=255, blank=True, null=True)
    resourcesnum = models.IntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'event'

class Eventkeyword(models.Model):
    event_id = models.IntegerField(blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'eventkeyword'

# class Event(models.Model):
#     event_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=45)
#     introduction = models.CharField(max_length=45)

#     class Meta:
#         #managed = False
#         db_table = 'event'


class EventTarget(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING)
    target = models.ForeignKey('Target', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'event-target'


class Eventkgraph(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING)
    point1 = models.CharField(max_length=45)
    point2 = models.CharField(max_length=45)
    ralation = models.CharField(max_length=45)

    class Meta:
        #managed = False
        db_table = 'eventkgraph'


class Eventrelationgraph(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING)
    point1 = models.CharField(max_length=45, blank=True, null=True)
    point2 = models.CharField(max_length=45, blank=True, null=True)
    relation = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'eventrelationgraph'


class Eventsourcing(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING)
    time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'eventsourcing'


class Gjanalysis(models.Model):
    gj_id = models.AutoField(db_column='GJ_id', primary_key=True)  # Field name made lowercase.
    sentence = models.ForeignKey('Sentence', models.DO_NOTHING)
    target = models.ForeignKey('Target', models.DO_NOTHING)
    gj_type = models.CharField(db_column='GJ_type', max_length=45, blank=True, null=True)  # Field name made lowercase.
    gj_style = models.CharField(db_column='GJ_style', max_length=45, blank=True, null=True)  # Field name made lowercase.
    confidence = models.CharField(db_column='Confidence', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'gjanalysis'


class Media(models.Model):
    media_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    country = models.CharField(max_length=45, blank=True, null=True)
    nickname = models.CharField(max_length=45, blank=True, null=True)
    introduction = models.CharField(max_length=500, blank=True, null=True)
    types = models.CharField(max_length=45, blank=True, null=True)
    imgurl = models.CharField(max_length=100,blank=True,null = True)
    countryurl = models.CharField(max_length=255,blank=True,null = True)
    class Meta:
        #managed = False
        db_table = 'media'


class Metaphoranalysis(models.Model):
    sentence = models.ForeignKey('Sentence', models.DO_NOTHING)
    noumenon = models.CharField(max_length=45)
    vehicle = models.CharField(max_length=45)
    n_emotion = models.CharField(max_length=45)
    v_emotion = models.CharField(max_length=45)
    appearinnoumenon = models.IntegerField(db_column='appearInNoumenon')  # Field name made lowercase.
    relatedtonoumenon = models.IntegerField(db_column='relatedToNoumenon')  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'metaphoranalysis'


class Partofspeechtagging(models.Model):
    article = models.ForeignKey(Article, models.DO_NOTHING)
    word = models.CharField(max_length=45, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'partofspeechtagging'


class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    calculatesource = models.CharField(max_length=255, blank=True, null=True)
    servercount = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan'


class PlanMedia(models.Model):
    plan = models.ForeignKey(Plan, models.DO_NOTHING, blank=True, null=True)
    media = models.ForeignKey(Media, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan-media'


class PlanTarget(models.Model):
    #id = models.IntegerField(primary_key=True)
    plan = models.ForeignKey(Plan, models.DO_NOTHING, blank=True, null=True)
    target = models.ForeignKey('Target', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan-target'

class Sentence(models.Model):
    sentence_id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, models.DO_NOTHING)
    sentence_num = models.IntegerField()
    text = models.CharField(max_length=10000)

    class Meta:
        #managed = False
        db_table = 'sentence'


class Spreadingprocess(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING)
    point1 = models.CharField(max_length=45, blank=True, null=True)
    point2 = models.CharField(max_length=45, blank=True, null=True)
    relation = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'spreadingprocess'


class Target(models.Model):
    target_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    types = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    imgurl = models.CharField(max_length=100,blank=True,null = True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        #managed = False
        db_table = 'target'


class Targetkgraph(models.Model):
    target = models.ForeignKey(Target, models.DO_NOTHING)
    point1 = models.CharField(max_length=45, blank=True, null=True)
    point2 = models.CharField(max_length=45, blank=True, null=True)
    relation = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'targetkgraph'

class User(models.Model):
    #base_user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'user'
        
class Wordcloud(models.Model):
    article = models.ForeignKey(Article, models.DO_NOTHING)
    word = models.CharField(max_length=45)
    proportion = models.FloatField()

    class Meta:
        #managed = False
        db_table = 'wordcloud'

class Relatedimages(models.Model):
    name1 = models.CharField(max_length=50, blank=True, null=True)
    name2 = models.CharField(max_length=50, blank=True, null=True)
    url1 = models.CharField(max_length=255, blank=True, null=True)
    url2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'relatedimages'

class Vediomanager(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    video_id = models.IntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'vediomanager'