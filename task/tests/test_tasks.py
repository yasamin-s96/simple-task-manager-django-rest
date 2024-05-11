from pydoc import cli
from urllib import response
from django.contrib.auth import get_user_model
from rest_framework import status
import pytest
from model_bakery import baker

from task.models import Task

User = get_user_model()


@pytest.fixture
def create_task(auth_user):
    def do_create_task(user=auth_user, quantity=None):
        return baker.make(Task, user=user, _quantity=quantity)

    return do_create_task


@pytest.mark.django_db
class TestCreateTasks:
    def test_if_valid_data_returns_201(self, client, authenticate):
        task = {"description": "testing"}

        response = client.post("/tasks/", task)

        assert response.status_code == status.HTTP_201_CREATED
        assert "description" in response.data

    def test_if_invalid_data_returns_400(self, client, authenticate):
        task = {"description": ""}

        response = client.post("/tasks/", task)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "description" in response.data


@pytest.mark.django_db
class TestTaskList:
    def test_if_the_list_belongs_to_the_user_returns_200(
        self, client, create_task, authenticate, auth_user, other_user
    ):
        other_users_tasks = create_task(user=other_user, quantity=5)
        current_users_tasks = create_task(quantity=5)

        response = client.get("/tasks/")
        assert len(response.data) == 5

        response_task_ids = {task["id"] for task in response.data}
        current_users_task_ids = {task.id for task in current_users_tasks}

        assert response.status_code == status.HTTP_200_OK
        assert response_task_ids == current_users_task_ids


@pytest.mark.django_db
class TestRetrieveTask:
    def test_if_existing_id_returns_200(
        self, client, create_task, authenticate, auth_user
    ):
        task = create_task(user=auth_user)

        response = client.get(f"/tasks/{task.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert "description" in response.data

    def test_if_nonexistent_id_returns_404(
        self, client, create_task, authenticate, auth_user
    ):
        task = create_task(user=auth_user)
        task_id = task.id
        task.delete()

        response = client.get(f"/tasks/{task_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_not_owner_returns_404(
        self, client, create_task, authenticate, other_user
    ):
        task = create_task(user=other_user)

        response = client.get(f"/tasks/{task.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteTask:
    def test_if_owner_attempts_delete_returns_204(
        self, client, create_task, authenticate, auth_user
    ):
        task = create_task(user=auth_user)

        response = client.delete(f"/tasks/{task.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_nonowner_attempts_delete_returns_404(
        self, client, create_task, authenticate, other_user
    ):
        task = create_task(user=other_user)

        response = client.delete(f"/tasks/{task.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateTask:
    def test_if_owner_attempts_update_returns_200(
        self, client, create_task, authenticate, auth_user
    ):
        task = create_task(user=auth_user)
        modification = {"description": "a"}

        response = client.put(f"/tasks/{task.id}/", modification)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["description"] == "a"

    def test_if_nonowner_attempts_update_returns_404(
        self, client, create_task, authenticate, other_user
    ):
        task = create_task(user=other_user)
        modification = {"description": "a"}

        response = client.put(f"/tasks/{task.id}/", modification)

        assert response.status_code == status.HTTP_404_NOT_FOUND
