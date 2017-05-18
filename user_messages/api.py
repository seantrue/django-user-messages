from django.contrib.messages import constants
from django.db import models


def add_message(user, level, message, extra_tags='', *,
                deliver_once=True, meta=None):
    from user_messages.models import Message

    Message.objects.create(
        message={
            'level': level,
            'message': str(message),
            'extra_tags': extra_tags,
        },
        deliver_once=deliver_once,
        meta=meta or {},
        **{'user' if isinstance(user, models.Model) else 'user_id': user}
    )


def get_messages(user):
    from user_messages.models import Message

    return Message.objects.filter(
        user=user,
        delivered_at__isnull=True,
    )


def _create_shortcut(level):
    def helper(user, message, extra_tags='', deliver_once=True, meta=None):
        add_message(user, level, message, extra_tags=extra_tags,
                    deliver_once=deliver_once, meta=meta)
    return helper


debug = _create_shortcut(constants.DEBUG)
info = _create_shortcut(constants.INFO)
success = _create_shortcut(constants.SUCCESS)
warning = _create_shortcut(constants.WARNING)
error = _create_shortcut(constants.ERROR)