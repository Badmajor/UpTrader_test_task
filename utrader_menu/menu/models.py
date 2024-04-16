from django.db import models
from django.utils.text import slugify


class BaseMenu(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Menu(BaseMenu):
    pass


class MenuItem(BaseMenu):
    menu = models.ForeignKey(Menu,
                             on_delete=models.CASCADE,
                             related_name='items')
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children')

    named_url = models.CharField(max_length=255,
                                 blank=True,
                                 null=True)

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        if not self.named_url:
            self.named_url = f'{slugify(self.menu)}_{slugify(self.name)}'
        super().save()

    @property
    def children(self):
        return self.children.all()
