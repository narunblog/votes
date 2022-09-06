from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json
from django.db.models import Sum


class JSONResponseRenderer(JSONRenderer):
    # media_type = 'text/plain'
    # media_type = 'application/json'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            'status': 'failure',
            'data': data,
            'message': '',
        }
        data = response_dict
        return json.dumps(data)
