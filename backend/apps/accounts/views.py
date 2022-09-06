from django.shortcuts import render
from celery.result import AsyncResult
from config.tasks import vote_status_update


def celery_test(request):
    task_id = vote_status_update.delay(1)

    result = AsyncResult(task_id)
    print('result:', result, ' : ', result.state, ' : ', result.ready())

    context = {'result': result}

    return render(request, 'accounts/celery_test.html', context)
