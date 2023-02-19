# from functools import cache

import requests

from settings import BASE_URL


class TLIBotApiClient:
    @staticmethod
    # @cache
    def get_courses():
        response = requests.get(f"{BASE_URL}/v1/courses")
        if response.status_code != 200:
            courses = {}
        else:
            courses = {course["_id"]: course["name"] for course in response.json()}
        return courses

    @staticmethod
    def upload_resource(
        author, uploader, course, description, title, tags, resource_file
    ):
        payload = {
            "tags": tags,
            "title": title,
            "description": description,
            "author": author,
            "uploader": uploader,
            "course": course,
        }
        files = [("file", (resource_file.name, resource_file, "application/pdf"))]

        response = requests.request(
            "POST",
            f"{BASE_URL}/v1/lecture-notes",
            data=payload,
            files=files,
        )
        return response.status_code == 201

    # @staticmethod
    # def clear_courses_cache():
    #     TLIBotApiClient.get_courses.cache_clear()
