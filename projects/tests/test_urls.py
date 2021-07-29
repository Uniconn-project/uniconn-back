from django.test import TestCase
from django.urls import resolve

from ..views import *

BASE_URL = "/api/projects/"


class TestUrls(TestCase):
    def test_get_fields_name_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-fields-name-list").func, get_fields_name_list)

    def test_get_projects_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-projects-list").func, get_projects_list)

    def test_get_filtered_projects_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-filtered-projects-list").func, get_filtered_projects_list)

    def test_get_projects_categories_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-projects-categories-list").func, get_projects_categories_list)

    def test_create_project_url(self):
        self.assertEqual(resolve(BASE_URL + "create-project").func, create_project)

    def test_get_project_url(self):
        self.assertEqual(resolve(BASE_URL + "get-project/2").func, get_project)

    def test_edit_project_url(self):
        self.assertEqual(resolve(BASE_URL + "edit-project/4").func, edit_project)

    def test_invite_to_project_url(self):
        self.assertEqual(resolve(BASE_URL + "invite-users-to-project/1").func, invite_users_to_project)

    def test_uninvite_from_project_url(self):
        self.assertEqual(resolve(BASE_URL + "uninvite-user-from-project/8").func, uninvite_user_from_project)

    def test_ask_to_join_project_url(self):
        self.assertEqual(resolve(BASE_URL + "ask-to-join-project/52").func, ask_to_join_project)

    def test_remove_from_project_url(self):
        self.assertEqual(resolve(BASE_URL + "remove-user-from-project/1001").func, remove_user_from_project)

    def test_reply_project_invitation_url(self):
        self.assertEqual(resolve(BASE_URL + "reply-project-invitation").func, reply_project_invitation)

    def test_reply_project_entering_request_url(self):
        self.assertEqual(resolve(BASE_URL + "reply-project-entering-request").func, reply_project_entering_request)

    def test_edit_project_description_url(self):
        self.assertEqual(resolve(BASE_URL + "edit-project-description/918").func, edit_project_description)

    def test_star_project_url(self):
        self.assertEqual(resolve(BASE_URL + "star-project/1564").func, star_project)

    def test_unstar_project_url(self):
        self.assertEqual(resolve(BASE_URL + "unstar-project/14763844").func, unstar_project)

    def test_leave_project_url(self):
        self.assertEqual(resolve(BASE_URL + "leave-project/10").func, leave_project)

    def test_create_link_url(self):
        self.assertEqual(resolve(BASE_URL + "create-link/10").func, create_link)

    def test_delete_link_url(self):
        self.assertEqual(resolve(BASE_URL + "delete-link/10").func, delete_link)

    def test_create_tool_url(self):
        self.assertEqual(resolve(BASE_URL + "create-tool/10").func, create_tool)

    def test_delete_tool_url(self):
        self.assertEqual(resolve(BASE_URL + "delete-tool/10").func, delete_tool)

    def test_create_project_discussion_url(self):
        self.assertEqual(resolve(BASE_URL + "create-project-discussion/3").func, create_project_discussion)

    def test_get_project_discussions_url(self):
        self.assertEqual(resolve(BASE_URL + "get-project-discussions/3").func, get_project_discussions)

    def test_get_project_discussion_url(self):
        self.assertEqual(resolve(BASE_URL + "get-project-discussion/3").func, get_project_discussion)

    def test_delete_project_discussion_url(self):
        self.assertEqual(resolve(BASE_URL + "delete-project-discussion").func, delete_project_discussion)

    def test_star_discussion_url(self):
        self.assertEqual(resolve(BASE_URL + "star-discussion/1").func, star_discussion)

    def test_unstar_discussion_url(self):
        self.assertEqual(resolve(BASE_URL + "unstar-discussion/1").func, unstar_discussion)

    def test_reply_discussion_url(self):
        self.assertEqual(resolve(BASE_URL + "reply-discussion/1").func, reply_discussion)

    def test_delete_discussion_reply_url(self):
        self.assertEqual(resolve(BASE_URL + "delete-discussion-reply/1").func, delete_discussion_reply)

    def test_promote_project_member_to_admin_url(self):
        self.assertEqual(resolve(BASE_URL + "promote-project-member-to-admin/1").func, promote_project_member_to_admin)
