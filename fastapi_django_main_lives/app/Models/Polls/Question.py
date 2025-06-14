"""
Laravel構造対応 Polls Models
============================

DjangoモデルをLaravel構造で管理
FastAPIとの統合に使用
"""

import os
import django
from django.conf import settings

# Django設定の確保
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()

from django.db import models


class Question(models.Model):
    """質問モデル"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    class Meta:
        app_label = 'polls'  # Djangoアプリケーション名を明示
        verbose_name = "質問"
        verbose_name_plural = "質問"
    
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """選択肢モデル"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'polls'  # Djangoアプリケーション名を明示
        verbose_name = "選択肢"
        verbose_name_plural = "選択肢"
    
    def __str__(self):
        return self.choice_text
