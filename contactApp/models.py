from django.db import models

from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.utils import timezone
from datetime import datetime

import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Create your models here.


class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='招聘岗位')
    description = models.TextField(verbose_name='岗位要求')
    publish_date = models.DateTimeField(
        max_length=20, default=timezone.now, verbose_name='发布时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '招聘广告'
        verbose_name_plural = '招聘广告'
        ordering = ('-publish_date', )


class Resume(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    person_id = models.CharField(max_length=30, verbose_name='身份证号')
    sex = models.CharField(max_length=5, default='男', verbose_name='性别')
    email = models.EmailField(max_length=30, verbose_name='邮箱')
    birth = models.DateField(max_length=20, default=datetime.strftime(
        datetime.now(), '%Y-%m-%d'), verbose_name='出生日期')
    edu = models.CharField(max_length=5, default='本科', verbose_name='学历')
    school = models.CharField(max_length=40, verbose_name='毕业院校')
    major = models.CharField(max_length=40, verbose_name='专业')
    position = models.CharField(max_length=40, verbose_name='申请职位')
    experience = models.TextField(blank=True, null=True, verbose_name='学习或工作经历')
    photo = models.ImageField(upload_to='contact/recruit/%Y_%m_%d')
    grade_list = (
        (1, '未审'),
        (2, '通过'),
        (3, '未通过'),
    )
    status = models.IntegerField(choices=grade_list, default=1, verbose_name='面试成绩')
    publish_date = models.DateTimeField(max_length=20, default=timezone.now, verbose_name='提交时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '简历'
        verbose_name_plural = '简历'
        ordering = ('status', '-publish_date')


# 单击保存按钮前触发信号
@receiver(post_init, sender=Resume)
def before_save_resume(sender, instance, **kwargs):
    instance._original_status = instance.status


# 单击保存按钮后触发信息
@receiver(post_save, sender=Resume)
def post_save_resume(sender, instance, **kwargs):
    email = instance.email
    EMAIL_FROM = '2435128850@qq.com'
    if instance._original_status == 1 and instance.status == 2:
        email_title = '通知；恒达科技招聘初试结果'
        email_body = '恭喜您通过本企业初试！'
        send_mail(email_title, email_body, EMAIL_FROM, [email])
        save_to_docx(instance)
    elif instance._original_status == 1 and instance.status == 3:
        email_title = '通知：恒达科技招聘初试结果'
        email_body = '很遗憾，您未能通过本企业初试，感谢您的关注。'
        send_mail(email_title, email_body, EMAIL_FROM, [email])


# 将简历保存到本地Word文档中
def save_to_docx(resume: Resume):
    root = os.getcwd()
    temp_path = os.path.join(root, r'media\contact\recruit.docx')
    temp = DocxTemplate(temp_path)

    context = {
        'name': resume.name,
        'personID': resume.person_id,
        'sex': resume.sex,
        'birth': resume.birth,
        'email': resume.email,
        'edu': resume.edu,
        'school': resume.school,
        'major': resume.major,
        'position': resume.position,
        'experience': resume.experience,
        'photo': InlineImage(temp, resume.photo, width=Mm(30), height=Mm(40))
    }

    temp.render(context)
    filename = os.path.join(root, r'media\contact\recruit', f'{resume.name}_{resume.id}.docx')
    temp.save(filename)
