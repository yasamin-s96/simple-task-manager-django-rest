from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
import pytest
from model_bakery import baker
from datetime import timedelta, datetime
import re

from task.models import Project, Task

User = get_user_model()


@pytest.fixture
def create_task(auth_user):
    def do_create_task(user=auth_user, quantity=None, fill_optional=False, **kwargs):

        return baker.make(
            Task, user=user, _quantity=quantity, _fill_optional=fill_optional, **kwargs
        )

    return do_create_task


@pytest.fixture
def extract_date():
    def do_extract_date(date_string):
        match = re.search(r"(\d{4}-\d{2}-\d{2})", date_string)
        return datetime.strptime(match.group(1), "%Y-%m-%d").date() if match else None

    return do_extract_date


@pytest.fixture
def extract_ids():
    def do_extract_ids(data):
        return [obj["id"] for obj in data]

    return do_extract_ids


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

    def test_if_creating_with_unrelated_projects_returns_400(
        self, client, other_user, authenticate
    ):
        project = baker.make(Project, user=other_user)
        task = {"description": "test", "project": project.id}

        response = client.post(f"/tasks/", task)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestTaskList:
    def test_if_the_list_belongs_to_the_user_returns_200(
        self, client, create_task, extract_ids, authenticate, auth_user, other_user
    ):
        other_users_tasks = create_task(user=other_user, quantity=5)
        current_users_tasks = create_task(quantity=5)

        response = client.get("/tasks/")
        assert len(response.data) == 5

        response_task_ids = extract_ids(response.data)
        current_users_task_ids = [task.id for task in current_users_tasks]

        assert response.status_code == status.HTTP_200_OK
        assert response_task_ids == current_users_task_ids


@pytest.mark.django_db
class TestRetrieveTask:
    def test_if_existing_id_returns_200(self, client, create_task, authenticate):
        task = create_task()

        response = client.get(f"/tasks/{task.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert "description" in response.data

    def test_if_nonexistent_id_returns_404(self, client, create_task, authenticate):
        task = create_task()
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
        self, client, create_task, authenticate
    ):
        task = create_task()

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
        self, client, create_task, authenticate
    ):
        task = create_task()
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


@pytest.mark.django_db
class TestTodayList:
    def test_if_list_belongs_to_today(
        self, client, authenticate, create_task, extract_ids
    ):
        # Tasks in this endpoint belong to the dates before till today
        yesterday_tasks = create_task(
            quantity=5, due_date=timezone.now() - timedelta(days=1)
        )
        today_tasks = create_task(quantity=5, due_date=timezone.now())
        tomorrow_tasks = create_task(
            quantity=5, due_date=timezone.now() + timedelta(days=1)
        )

        today_task_ids = [task.id for task in today_tasks]
        yesterday_task_ids = [task.id for task in yesterday_tasks]

        response = client.get("/today/")

        assert response.status_code == status.HTTP_200_OK

        response_task_ids = extract_ids(response.data)
        assert response_task_ids == yesterday_task_ids + today_task_ids
        assert all(task.id not in response_task_ids for task in tomorrow_tasks)

    def test_if_today_date_is_set_if_not_passed(
        self, client, authenticate, extract_date
    ):
        task = {"description": "test"}

        response = client.post("/today/", task)

        assert response.status_code == status.HTTP_201_CREATED
        date = extract_date(response.data["due_date"])
        assert date == timezone.now().date()


@pytest.mark.django_db
class TestTomorrowList:
    def test_if_list_belongs_to_tomorrow(
        self, client, authenticate, create_task, extract_ids
    ):
        today_tasks = create_task(quantity=5, due_date=timezone.now())
        tomorrow_tasks = create_task(
            quantity=5, due_date=timezone.now() + timedelta(days=1)
        )

        response = client.get("/tomorrow/")
        assert response.status_code == status.HTTP_200_OK
        response_task_ids = extract_ids(response.data)
        assert all(task.id not in response_task_ids for task in today_tasks)
        assert all(task.id in response_task_ids for task in tomorrow_tasks)

    def test_if_tomorrow_date_gets_added_to_due_date(
        self, client, authenticate, extract_date
    ):
        task = {"description": "test"}

        response = client.post("/tomorrow/", task)

        assert response.status_code == status.HTTP_201_CREATED
        date = extract_date(response.data["due_date"])
        assert date == (timezone.now() + timedelta(days=1)).date()


@pytest.mark.django_db
class TestPlannedList:
    def test_if_list_belongs_to_planned(
        self, client, authenticate, create_task, extract_ids
    ):
        """
        The planned task list should only contain the tasks which their due date is set.
        """
        tasks_with_unspecified_due_date = create_task(quantity=5)
        tasks_with_specified_due_date = create_task(quantity=5, fill_optional=True)

        response = client.get("/planned/")

        assert response.status_code == status.HTTP_200_OK

        response_task_ids = extract_ids(response.data)
        assert all(
            task.id not in response_task_ids for task in tasks_with_unspecified_due_date
        )
        assert all(
            task.id in response_task_ids for task in tasks_with_specified_due_date
        )

    def test_if_today_date_is_set_if_not_passed(
        self, client, authenticate, extract_date
    ):
        task = {"description": "test"}

        response = client.post("/planned/", task)

        assert response.status_code == status.HTTP_201_CREATED
        date = extract_date(response.data["due_date"])
        assert date == timezone.now().date()


@pytest.mark.django_db
class TestCompletedTasks:
    def test_if_only_completed_tasks_are_fetched_returns_200(
        self, client, authenticate, create_task, extract_ids
    ):
        completed_tasks = create_task(quantity=5, status="complete")
        incomplete_tasks = create_task(quantity=5, status="pending")

        response = client.get("/completed-tasks/")
        assert response.status_code == status.HTTP_200_OK

        response_task_ids = extract_ids(response.data)
        assert all(task.id in response_task_ids for task in completed_tasks)
        assert all(task.id not in response_task_ids for task in incomplete_tasks)

    def test_if_post_is_not_allowed_returns_405(self, client, authenticate):
        response = client.post("/completed-tasks/", {})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_if_owner_attempts_update_returns_200(
        self, client, create_task, authenticate
    ):
        task = create_task(status="complete")
        modification = {"description": "a"}

        response = client.put(f"/completed-tasks/{task.id}/", modification)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["description"] == "a"

    def test_if_nonowner_attempts_update_returns_404(
        self, client, create_task, authenticate, other_user
    ):
        task = create_task(user=other_user, status="complete")
        modification = {"description": "a"}

        response = client.put(f"/completed-tasks/{task.id}/", modification)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_owner_attempts_delete_returns_204(
        self, client, create_task, authenticate
    ):
        task = create_task(status="complete")

        response = client.delete(f"/completed-tasks/{task.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_nonowner_attempts_delete_returns_404(
        self, client, create_task, authenticate, other_user
    ):
        task = create_task(user=other_user, status="complete")

        response = client.delete(f"/completed-tasks/{task.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
