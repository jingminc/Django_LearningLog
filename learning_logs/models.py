from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""用户学习的主题。"""
class Topic(models.Model):
    text = models.CharField(max_length=200) #由字符组成的数据，即文本
    date_added = models.DateTimeField(auto_now_add=True) #记录日期和时间的数据
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    """返回模型的字符串表示。"""
    def __str__(self):
        return self.text #返回存储在属性text中的字符串

"""学到的有关某个主题的具体知识。"""
class Entry(models.Model):
    # 将每个条目关联到特定主题
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) # 级联删除
    # TextField 实例，字段的长度不受限制
    text = models.TextField()
    # 按创建顺序呈现条目，并在每个条目旁边放置时间戳。
    date_added = models.DateTimeField(auto_now_add=True)
    # Meta 存储用于管理模型的额外信息
    # 此处meta设置一个特殊属性，让Django在需要时使用Entries 来表示多个条目。
    class Meta: 
        verbose_name_plural = 'entries'
    
    """返回模型的字符串表示。"""
    def __str__(self):
        if len(self.text) > 50:
            return_str = f"{self.text[:50]}..."
        else:
            return_str = f"{self.text[:50]}"
        return return_str