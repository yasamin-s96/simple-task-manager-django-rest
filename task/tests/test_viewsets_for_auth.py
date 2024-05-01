from rest_framework import status
from django.urls import reverse
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        reverse("task-detail", args=[1]),
        reverse("project-detail", args=[1]),
        reverse("tag-detail", args=[1]),
    ],
)
def test_if_detail_endpoints_reject_anonymous_user_returns_401(client, url):
    delete_response = client.delete(url)

    assert delete_response.status_code == status.HTTP_401_UNAUTHORIZED

    put_response = client.put(url)

    assert put_response.status_code == status.HTTP_401_UNAUTHORIZED

    get_response = client.get(url)

    assert get_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        reverse("today-list"),
        reverse("planned-list"),
        reverse("task-list"),
        reverse("tomorrow-list"),
        reverse("project-list"),
        reverse("tag-list"),
        reverse("completed_task-list"),
    ],
)
def test_if_list_endpoints_reject_anonymous_user_returns_401(client, url):
    get_response = client.get(url)

    assert get_response.status_code == status.HTTP_401_UNAUTHORIZED

    post_response = client.post(url)

    assert post_response.status_code == status.HTTP_401_UNAUTHORIZED
