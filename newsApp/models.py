from django.db import models
from DjangoUeditor.models import UEditorField
from django.utils import timezone

# Create your models here.


class MyNews(models.Model):
    NEWS_TYPE = (
        ('company', '企业要闻'),
        ('industry', '行业新闻'),
        ('notice', '通知公告'),
    )
    title = models.CharField(max_length=50, verbose_name='新闻标题')
    description = UEditorField(width=1000,
                               height=300, 
                               default='',
                               imagePath='News/images/', 
                               filePath='News/files/', 
                               verbose_name='内容')
    news_type = models.CharField(
        choices=NEWS_TYPE, max_length=50, verbose_name='新闻类型')
    publish_date = models.DateTimeField(
        max_length=20, default=timezone.now, verbose_name='发布时间')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = verbose_name
        ordering = ['-publish_date', ]
