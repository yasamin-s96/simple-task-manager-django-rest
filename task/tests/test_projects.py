from pydoc import cli
import stat
from urllib import response
from rest_framework import status
import pytest
from model_bakery import baker

from task.models import Project
from task.views import ProjectRelatedTaskViewSet


@pytest.fixture
def create_project(auth_user):
    def do_create_project(user=auth_user, quantity=None):
        return baker.make(Project, user=user, _quantity=quantity)

    return do_create_project


@pytest.mark.django_db
class TestProjectList:
    def test_if_owner_can_view_projects_returns_200(
        self, client, authenticate, auth_user, other_user, create_project
    ):
        other_user_projects = create_project(user=other_user, quantity=5)
        auth_user_projects = create_project(quantity=5)

        response = client.get("/projects/")

        assert len(response.data) == 5
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": project.id,
                "title": project.title,
            }
            for project in auth_user_projects
        ]


@pytest.mark.django_db
class TestCreateProject:
    def test_if_data_is_valid_returns_201(self, client, authenticate):
        project = {"title": "test_project"}

        response = client.post("/projects/", project)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {"id": response.data["id"], "title": project["title"]}

    def test_if_data_is_invalid_returns_400(self, client, authenticate):
        project = {"title": ""}

        response = client.post("/projects/", project)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveProject:
    def test_if_user_owns_the_project_returns_200(
        self, client, authenticate, auth_user, create_project
    ):
        project = create_project()

        response = client.get(f"/projects/{project.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": project.id,
            "title": project.title,
            "status": project.status,
        }

    def test_if_user_is_not_the_project_owner_returns_404(
        self, client, authenticate, other_user, create_project
    ):
        other_user_project = create_project(user=other_user)

        response = client.get(f"/projects/{other_user_project.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # if the project_id is invalid returns 404


# class TestUpdateProject
