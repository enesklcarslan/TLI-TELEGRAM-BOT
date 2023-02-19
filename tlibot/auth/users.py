from datetime import datetime
from typing import Optional

import requests

from client.api import TLIBotApiClient


class User:
    def __init__(self, id, username, first_name):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.is_at_step = 0
        self.updated_at = datetime.now()

    def set_step(self, step):
        self.is_at_step = step
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"{self.id} - {self.username}"

    def __str__(self):
        return f"{self.id} - {self.username}"


class UserList:
    def __init__(self):
        self.users = []

    def add_user(self, id, username, first_name):
        first_name = first_name.capitalize()
        user = User(id, username, first_name)
        self.users.append(user)
        return user

    def get_user(self, id) -> Optional[User]:
        for user in self.users:
            if user.id == id:
                return user
        return None

    def get_or_create(self, id, username, first_name):
        created = False
        local_user = users_list.get_user(id)
        if local_user is None:
            local_user = users_list.add_user(id, username, first_name)
            created = True
        return created, local_user

    def get_users(self):
        return self.users

    def remove_user(self, id):
        for user in self.users:
            if user.id == id:
                self.users.remove(user)
                return True
        return False

    def remove_inactive_users(self):
        for user in self.users:
            if (datetime.now() - user.updated_at).days > 2:
                self.users.remove(user)
                user_resource_map.pop(user.id)

    def __repr__(self):
        return f"{self.users}"

    def __str__(self):
        return f"{self.users}"


class Resource:
    def __init__(self):
        self.author = None
        self.uploader = None
        self.course = None
        self.description = None
        self.title = None
        self.tags = []
        self.resource_file = None

    def set_uploader(self, uploader):
        self.uploader = uploader

    def set_author(self, author):
        self.author = author

    def set_uploader(self, uploader):
        self.uploader = uploader

    def set_course(self, course):
        self.course = course

    def set_description(self, description):
        self.description = description

    def set_title(self, title):
        self.title = title

    def set_tags(self, tags):
        for tag in tags:
            self.tags.append(tag)

    def set_file(self, resource_file):
        self.file = resource_file

    def upload_to_tli(self):
        return TLIBotApiClient.upload_resource(
            self.author,
            self.uploader,
            self.course,
            self.description,
            self.title,
            self.tags,
            self.file,
        )


users_list = UserList()

user_resource_map: dict[User, Resource] = dict()
