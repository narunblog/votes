from __future__ import absolute_import, unicode_literals
from apps.votes.models import Vote
from django.utils import timezone
from celery import shared_task


@shared_task
def vote_status_update(pk):
    vote = Vote.objects.get(pk=pk)
    now = timezone.now()
    start_datetime = vote.start_datetime
    end_datetime = vote.end_datetime

    if now < start_datetime:
        vote.status = 0
        vote_status_update.apply_async((vote.id,), eta=start_datetime)
    elif start_datetime <= now <= end_datetime:
        vote.status = 1
        vote_status_update.apply_async((vote.id,), eta=end_datetime)
    elif end_datetime < now:
        vote.status = 2
    else:
        pass
    vote.save()
    print('{}ステータスを更新しました。 値:{}'.format(vote.title, vote.status))
