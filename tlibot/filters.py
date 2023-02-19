from pyrogram import filters

from client.api import TLIBotApiClient
from tlibot.auth.users import users_list


def not_started(_, __, message):
    user = users_list.get_user(message.from_user.id)
    return not user


def step_factory(step):
    def step_filter(_, __, message):
        created, user = users_list.get_or_create(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
        )
        return user.is_at_step == step

    return filters.create(step_filter)


dersyukle = filters.create(lambda _, __, m: m.data == "dersyukle")
not_started = filters.create(not_started)
course_selected = filters.create(
    lambda _, __, m: m.data in TLIBotApiClient.get_courses().keys()
)
