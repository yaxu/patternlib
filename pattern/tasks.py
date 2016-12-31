from django_q.tasks import (
    async, result
)
from django_q.brokers import get_broker
import runpattern

broker = get_broker()

def run_render_and_upload(code):
    action_id = async('patterns.render_and_upload', code)
    return result(action_id)
