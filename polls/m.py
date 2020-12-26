# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=45, blank=True, null=True)
    forward = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emotion = models.CharField(max_length=45)
    emotion_strength = models.IntegerField()
    source = models.ForeignKey('Media', models.DO_NOTHING)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'article-target'


class Articlekgraph(models.Model):
    point1 = models.CharField(max_length=45)
    point2 = models.CharField(max_length=45)
    relation = models.CharField(max_length=45)
    article = models.ForeignKey(Article, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'articlekgraph'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Emotionalanalysis(models.Model):
    emotion1 = models.CharField(max_length=45, blank=True, null=True)
    emotion2 = models.CharField(max_length=45, blank=True, null=True)
    emotion3 = models.CharField(max_length=45, blank=True, null=True)
    rate1 = models.FloatField(blank=True, null=True)
    rate2 = models.FloatField(blank=True, null=True)
    rate3 = models.FloatField(blank=True, null=True)
    article = models.ForeignKey(Article, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'emotionalanalysis'


class Emotionaldistribution(models.Model):
    emotion = models.CharField(max_length=45, blank=True, null=True)
    target = models.ForeignKey('Target', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'emotionaldistribution'


class Entityextraction(models.Model):
    entity = models.CharField(max_length=45)
    emotion = models.CharField(max_length=45)
    article = models.ForeignKey(Article, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'entityextraction'


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    introduction = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    emotion = models.CharField(max_length=255, blank=True, null=True)
    resourcesnum = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'


class EventTarget(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING)
    target = models.ForeignKey('Target', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'event-target'


class Eventkeyword(models.Model):
    event_id = models.IntegerField(blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventkeyword'


class Eventkgraph(models.Model):
    point1 = models.CharField(max_length=45)
    point2 = models.CharField(max_length=45)
    ralation = models.CharField(max_length=45)
    event = models.ForeignKey(Event, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'eventkgraph'


class Eventrelationgraph(models.Model):
    point1 = models.CharField(max_length=45, blank=True, null=True)
    point2 = models.CharField(max_length=45, blank=True, null=True)
    relation = models.CharField(max_length=45, blank=True, null=True)
    event = models.ForeignKey(Event, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'eventrelationgraph'


class Eventsourcing(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    event = models.ForeignKey(Event, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'eventsourcing'


class Gjanalysis(models.Model):
    gj_id = models.AutoField(db_column='GJ_id', primary_key=True)  # Field name made lowercase.
    gj_type = models.CharField(db_column='GJ_type', max_length=45, blank=True, null=True)  # Field name made lowercase.
    gj_style = models.CharField(db_column='GJ_style', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sentence = models.ForeignKey('Sentence', models.DO_NOTHING)
    target = models.ForeignKey('Target', models.DO_NOTHING)
    confidence = models.FloatField(db_column='Confidence', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gjanalysis'


class Media(models.Model):
    media_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    country = models.CharField(max_length=45, blank=True, null=True)
    nickname = models.CharField(max_length=45, blank=True, null=True)
    introduction = models.CharField(max_length=500, blank=True, null=True)
    types = models.CharField(max_length=45, blank=True, null=True)
    imgurl = models.CharField(max_length=100, blank=True, null=True)
    countryurl = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media'


class Metaphoranalysis(models.Model):
    noumenon = models.CharField(max_length=45)
    vehicle = models.CharField(max_length=45)
    n_emotion = models.CharField(max_length=45)
    v_emotion = models.CharField(max_length=45)
    appearinnoumenon = models.IntegerField(db_column='appearInNoumenon')  # Field name made lowercase.
    relatedtonoumenon = models.IntegerField(db_column='relatedToNoumenon')  # Field name made lowercase.
    sentence = models.ForeignKey('Sentence', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'metaphoranalysis'


class Partofspeechtagging(models.Model):
    word = models.CharField(max_length=45, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    article = models.ForeignKey(Article, models.DO_NOTHING)

    class Meta:
        managed = False
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
    plan = models.ForeignKey(Plan, models.DO_NOTHING, blank=True, null=True)
    target = models.ForeignKey('Target', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan-target'


class Relatedimages(models.Model):
    name1 = models.CharField(max_length=50, blank=True, null=True)
    name2 = models.CharField(max_length=50, blank=True, null=True)
    url1 = models.CharField(max_length=255, blank=True, null=True)
    url2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relatedimages'


class Sentence(models.Model):
    sentence_id = models.AutoField(primary_key=True)
    sentence_num = models.IntegerField()
    text = models.CharField(max_length=10000)
    article = models.ForeignKey(Article, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sentence'


class Spreadingprocess(models.Model):
    point1 = models.CharField(max_length=45, blank=True, null=True)
    point2 = models.CharField(max_length=45, blank=True, null=True)
    relation = models.CharField(max_length=45, blank=True, null=True)
    event = models.ForeignKey(Event, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'spreadingprocess'


class Target(models.Model):
    target_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    types = models.CharField(max_length=45, blank=True, null=True)
    imgurl = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'target'


class Targetkgraph(models.Model):
    point1 = models.CharField(max_length=45, blank=True, null=True)
    point2 = models.CharField(max_length=45, blank=True, null=True)
    relation = models.CharField(max_length=45, blank=True, null=True)
    target = models.ForeignKey(Target, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'targetkgraph'


class User(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Vediomanager(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    video_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vediomanager'


class Wordcloud(models.Model):
    word = models.CharField(max_length=45)
    proportion = models.FloatField()
    article = models.ForeignKey(Article, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wordcloud'
