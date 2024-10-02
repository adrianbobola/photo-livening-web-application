"""
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
"""

from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.db import transaction


class QueueItem(models.Model):
    """
    Trieda QueueItem sluzi na spravu uzivatelov cakajucich vo fronte na uvolnenie zdrojov pre spustenie aplikacie

    Attributes:
        user_token (string): Token uzivatela
        timestamp (datetime): Casova znamka zaradenia uzivatela do cakajucej fronty
        lastActivity_timestamp (datetime): Casova znamka poslednej aktivity uzivatela cakjuceho vo fronte
    """
    user_token = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    lastActivity_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'backend'

    def __str__(self):
        return f"{self.user_token} at {self.timestamp}"


def enqueue(user_token):
    """
    Vlozi uzivatela do cakajucej fronty
    """
    item = QueueItem(user_token=user_token)
    item.save()
    return item


def dequeue():
    """
    Vyberie uzivatela z fronty, ktory tam caka najdlhsi cas
    """
    item = QueueItem.objects.order_by('timestamp').first()
    if item is not None:
        user_token = item.user_token
        item.delete()
        return user_token
    else:
        return None


def get_user_position(user_token):
    """
    Sluzi na zistenie aktualnej pozicie uzivatela v cakacej fronte
    """
    with transaction.atomic():
        all_items = QueueItem.objects.select_for_update().order_by('timestamp')
        tokens_list = list(all_items.values_list('user_token', flat=True))
        try:
            # index zacina 0 a nemoze byt 0. v poradi
            position = tokens_list.index(user_token) + 1
            return position
        except ValueError:
            return None


def set_user_last_activity(user_token):
    """
    Sluzi na aktualizaciu casovej znamky poslednej aktivity uzivatela v cakacej fronte
    """
    item = QueueItem.objects.filter(user_token=user_token).first()
    if item:
        item.lastActivity_timestamp = timezone.now()
        item.save()


def remove_inactive_users():
    """
     Sluzi ku kontrole casovej znamky poslednej aktivity uzivatelov.
     Ak uzivatel je v cakacej fronte po dobu dlhsiu ako je 30 sekund bez odpovede, system vyhodnoti ze dany uzivatel
     odisiel a nema uz zaujem dalej cakat.
     Tymto dojde k jeho odstraneniu z cakacej fronty
     """
    now = timezone.now()
    time_limit = now - timedelta(seconds=30)
    old_items = QueueItem.objects.filter(lastActivity_timestamp__lt=time_limit)
    old_items.delete()
    return True
