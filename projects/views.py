import base64

from django.core.files.base import ContentFile
from jwt_auth.decorators import login_required
from profiles.models import Profile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Field,
    Link,
    Project,
    ProjectMember,
    ProjectRequest,
    ProjectStar,
    Tool,
    ToolCategory,
)
from .serializers import (
    DiscussionSerializer01,
    FieldSerializer01,
    ProjectSerializer01,
    ProjectSerializer02,
)


@api_view(["GET"])
def get_fields_name_list(request):
    Fields = Field.objects.all()
    serializer = FieldSerializer01(Fields, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_projects_list(request):
    projects = Project.objects.all()[:30]
    serializer = ProjectSerializer01(projects, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_filtered_projects_list(request):
    categories = request.query_params["categories"].split(";")
    fields = request.query_params["fields"].split(";")

    projects = Project.objects.filter(category__in=categories, fields__name__in=fields).distinct()
    serializer = ProjectSerializer01(projects, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_projects_categories_list(request):
    categories = [
        {"value": category[0], "readable": category[1]} for category in Project.get_project_categories_choices()
    ]
    return Response(categories)


@api_view(["POST"])
@login_required
def create_project(request):
    profile = request.user.profile

    try:
        category = request.data["category"].strip()
        name = request.data["name"].strip()
        slogan = request.data["slogan"].strip()
        fields_name = request.data["fields"]
        fields = Field.objects.filter(name__in=fields_name)
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    if not (len(name) and len(slogan)):
        return Response("Todos os campos devem ser preenchidos!", status=status.HTTP_400_BAD_REQUEST)

    if len(name) > 50 or len(slogan) > 125:
        return Response("Respeite os limites de caracteres de cada campo!", status=status.HTTP_400_BAD_REQUEST)

    if len(fields) == 0:
        return Response("Selecione pelo menos uma área de atuação válida!", status=status.HTTP_400_BAD_REQUEST)

    if category not in Project.get_project_categories_choices(index=0):
        return Response("Categoria do projeto inválida!", status=status.HTTP_400_BAD_REQUEST)

    project = Project.objects.create(category=category, name=name, slogan=slogan)
    project.fields.set(fields)
    project.save()

    ProjectMember.objects.create(profile=profile, project=project, role="admin")

    return Response("success")


@api_view(["GET"])
def get_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado", status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer02(project)

    return Response(serializer.data)


@api_view(["PUT"])
@login_required
def edit_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado", status=status.HTTP_404_NOT_FOUND)

    try:
        project_membership = ProjectMember.objects.get(profile=request.user.profile, project=project)
    except:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    if project_membership.role != "admin":
        return Response("Somente admins podem editar o projeto!", status=status.HTTP_401_UNAUTHORIZED)

    try:
        image = request.data["image"]
        name = request.data["name"].strip()
        category = request.data["category"].strip()
        slogan = request.data["slogan"].strip()
        fields_name = request.data["fields"]
        fields = Field.objects.filter(name__in=fields_name)
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    if len(name) > 50 or len(slogan) > 125:
        return Response("Respeite os limites de caracteres de cada campo!", status=status.HTTP_400_BAD_REQUEST)

    if category != "" and category not in Project.get_project_categories_choices(index=0):
        return Response("Categoria do projeto inválida!", status=status.HTTP_400_BAD_REQUEST)

    if len(fields) == 0:
        return Response("Selecione pelo menos uma área de atuação válida!", status=status.HTTP_400_BAD_REQUEST)

    if image is not None:
        format, imgstr = image.split(";base64,")
        img_format = format.split("/")[-1]
        project_image = ContentFile(base64.b64decode(imgstr), name=f"{project.name}.{img_format}")
        project.image = project_image

    project.name = name
    project.category = category
    project.slogan = slogan
    project.fields.set(fields)

    project.save()

    return Response("success")


@api_view(["POST"])
@login_required
def invite_users_to_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    try:
        project_membership = ProjectMember.objects.get(profile=request.user.profile, project=project)
    except:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    if project_membership.role != "admin":
        return Response("Somente admins podem convidar usuários para o projeto!", status=status.HTTP_401_UNAUTHORIZED)

    try:
        usernames = request.data["usernames"]
        message = request.data["message"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    profiles = Profile.objects.filter(user__username__in=usernames)
    if not profiles.exists():
        return Response("Nenhum usuário foi encontrado!", status=status.HTTP_400_BAD_REQUEST)

    if ProjectRequest.objects.filter(type="invitation", project=project, profile__in=profiles).exists():
        return Response("Usuário já convidado!", status=status.HTTP_400_BAD_REQUEST)

    for profile in profiles:
        ProjectRequest.objects.create(type="invitation", message=message, project=project, profile=profile)

    return Response("success")


@api_view(["DELETE"])
@login_required
def uninvite_user_from_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    try:
        project_membership = ProjectMember.objects.get(profile=request.user.profile, project=project)
    except:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    if project_membership.role != "admin":
        return Response("Somente admins podem retirar convite para o projeto!", status=status.HTTP_401_UNAUTHORIZED)

    try:
        username = request.data["username"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        profile = Profile.objects.get(user__username=username)
    except:
        return Response("Usuário não encontrado!", status=status.HTTP_404_NOT_FOUND)

    try:
        invitation = ProjectRequest.objects.get(project=project, profile=profile, type="invitation")
    except:
        return Response("Convite não encontrado!", status=status.HTTP_404_NOT_FOUND)

    invitation.delete()

    return Response("success")


@api_view(["POST"])
@login_required
def ask_to_join_project(request, project_id):
    try:
        message = request.data["message"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    profile = request.user.profile

    if profile in project.members_profiles:
        return Response("Você já está no projeto!", status=status.HTTP_400_BAD_REQUEST)

    if profile in project.pending_invited_profiles:
        return Response("O projeto já te convidou!", status=status.HTTP_400_BAD_REQUEST)

    if ProjectRequest.objects.filter(type="entry_request", project=project, profile=profile).exists():
        return Response("Você já pediu para entrar no projeto!", status=status.HTTP_400_BAD_REQUEST)

    ProjectRequest.objects.create(type="entry_request", message=message, project=project, profile=profile)

    return Response("success")


@api_view(["DELETE"])
@login_required
def remove_user_from_project(request, project_id):
    try:
        username = request.data["username"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    try:
        my_project_membership = ProjectMember.objects.get(profile=request.user.profile, project=project)
    except:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    if my_project_membership.role != "admin":
        return Response("Somente admins podem retirar convite para o projeto!", status=status.HTTP_401_UNAUTHORIZED)

    try:
        profile = Profile.objects.get(user__username=username)
        project_membership = ProjectMember.objects.get(profile=profile, project=project)
    except:
        return Response("Usuário não encontrado!", status=status.HTTP_404_NOT_FOUND)

    project_membership.delete()

    return Response("success")


@api_view(["PUT"])
@login_required
def reply_project_invitation(request):
    profile = request.user.profile

    try:
        reply = request.data["reply"]
        project_id = request.data["project_id"]

        project = Project.objects.get(pk=project_id)
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    if profile.type == "student":

        if not profile.student in project.pending_invited_students.all():
            return Response("O projeto não te convidou!", status=status.HTTP_400_BAD_REQUEST)

        project.pending_invited_students.remove(profile.student)

        if reply == "accept":
            project.students.add(profile.student)

    elif profile.type == "mentor":

        if not profile.mentor in project.pending_invited_mentors.all():
            return Response("O projeto não te convidou!", status=status.HTTP_400_BAD_REQUEST)

        project.pending_invited_mentors.remove(profile.mentor)

        if reply == "accept":
            project.mentors.add(profile.mentor)

    project.save()

    return Response("success")


@api_view(["DELETE"])
@login_required
def reply_project_entering_request(request):
    try:
        reply = request.data["reply"]
        request_id = request.data["request_id"]

        project_request = ProjectRequest.objects.get(pk=request_id)
        project = project_request.project
        profile = project_request.profile
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        project_membership = ProjectMember.objects.get(profile=request.user.profile, project=project)
    except:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    if project_membership.role != "admin":
        return Response("Somente admins podem retirar convite para o projeto!", status=status.HTTP_401_UNAUTHORIZED)

    project_request.delete()

    if reply == "accept":
        ProjectMember.objects.create(profile=profile, project=project, role="member")

    return Response("success")


@api_view(["PATCH"])
@login_required
def edit_project_description(request, project_id):
    try:
        description = request.data["description"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    if len(str(description)) > 20000:
        return Response("A descrição superou o limite de caracteres!", status=status.HTTP_400_BAD_REQUEST)

    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    try:
        project_membership = ProjectMember.objects.get(profile=request.user.profile, project=project)
    except:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    if project_membership.role != "admin":
        return Response("Somente admins podem retirar convite para o projeto!", status=status.HTTP_401_UNAUTHORIZED)

    project.description = description
    project.save()

    return Response("success")


@api_view(["POST"])
@login_required
def star_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    if ProjectStar.objects.filter(profile=request.user.profile, project=project).exists():
        return Response("Você não pode curtir o mesmo projeto mais de uma vez!", status=status.HTTP_400_BAD_REQUEST)

    ProjectStar.objects.create(profile=request.user.profile, project=project)

    return Response("success")


@api_view(["DELETE"])
@login_required
def unstar_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    try:
        project_star = ProjectStar.objects.get(profile=request.user.profile, project=project)
    except:
        return Response("Curtida não encontrada!", status=status.HTTP_404_NOT_FOUND)

    project_star.delete()

    return Response("success")


@api_view(["PATCH"])
@login_required
def leave_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    profile = request.user.profile

    try:
        project_membership = ProjectMember.objects.get(profile=profile, project=project)
    except:
        return Response("Você não faz parte do projeto!", status=status.HTTP_400_BAD_REQUEST)

    project_membership.delete()

    return Response("success")


@api_view(["POST"])
@login_required
def create_link(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    if not request.user.profile in project.members_profiles:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    try:
        name = request.data["name"].strip()
        href = request.data["href"].strip()
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    if name == "" or href == "":
        return Response("Todos os campos devem ser preenchidos!", status=status.HTTP_400_BAD_REQUEST)

    if len(name) > 100 or len(href) > 1000:
        return Response("Respeite os limites de caracteres de cada campo!", status=status.HTTP_400_BAD_REQUEST)

    Link.objects.create(name=name, href=href, project=project)

    return Response("success")


@api_view(["DELETE"])
@login_required
def delete_link(request, link_id):
    try:
        link = Link.objects.get(pk=link_id)
    except:
        return Response("Link não encontrado!", status=status.HTTP_404_NOT_FOUND)

    if not request.user.profile in link.project.members_profiles:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    link.delete()

    return Response("success")


@api_view(["POST"])
@login_required
def create_tool(request, project_id):
    try:
        category_name = request.data["category"].strip()
        name = request.data["name"].strip()
        href = request.data["href"].strip()
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    try:
        category = ToolCategory.objects.get(project=project, name=category_name)
    except:
        return Response("Categoria não encontrada!", status=status.HTTP_404_NOT_FOUND)

    if not request.user.profile in project.members_profiles:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    if name == "" or href == "":
        return Response("Todos os campos devem ser preenchidos!", status=status.HTTP_400_BAD_REQUEST)

    if len(name) > 100 or len(href) > 1000:
        return Response("Respeite os limites de caracteres de cada campo!", status=status.HTTP_400_BAD_REQUEST)

    Tool.objects.create(category=category, name=name, href=href)

    return Response("success")


@api_view(["DELETE"])
@login_required
def delete_tool(request, tool_id):
    try:
        tool = Tool.objects.get(pk=tool_id)
    except:
        return Response("Ferramenta não encontrada!", status=status.HTTP_404_NOT_FOUND)

    if not request.user.profile in tool.category.project.members_profiles:
        return Response("Você não faz parte do projeto!", status=status.HTTP_401_UNAUTHORIZED)

    tool.delete()

    return Response("success")


@api_view(["POST"])
@login_required
def create_project_discussion(request, project_id):
    try:
        title = request.data["title"].strip()
        body = request.data["body"].strip()
        category = request.data["category"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    if len(title) > 125 or len(body) > 1000:
        return Response("Respeite os limites de caracteres de cada campo!", status=status.HTTP_400_BAD_REQUEST)

    if category not in Discussion.get_discussion_categories_choices(0):
        return Response("Categoria inválida!", status=status.HTTP_400_BAD_REQUEST)

    if title == "" or body == "":
        return Response("Todos os campos devem ser preenchidos!", status=status.HTTP_400_BAD_REQUEST)

    Discussion.objects.create(title=title, body=body, category=category, project=project, profile=request.user.profile)

    return Response("success")


@api_view(["GET"])
def get_project_discussions(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return Response("Projeto não encontrado!", status=status.HTTP_404_NOT_FOUND)

    serializer = DiscussionSerializer01(project.discussions, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_project_discussion(request, discussion_id):
    try:
        discussion = Discussion.objects.get(pk=discussion_id)
    except:
        return Response("Discussão não encontrada", status=status.HTTP_404_NOT_FOUND)

    serializer = DiscussionSerializer01(discussion)

    return Response(serializer.data)


@api_view(["DELETE"])
@login_required
def delete_project_discussion(request):
    try:
        discussion_id = request.data["discussion_id"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        discussion = Discussion.objects.get(pk=discussion_id)
        project = discussion.project
    except:
        return Response("Discussão não encontrada!", status=status.HTTP_404_NOT_FOUND)

    is_project_member = request.user.profile in project.members_profiles

    if request.user.profile != discussion.profile and not is_project_member:
        return Response("Você não pode deletar essa discussão!", status=status.HTTP_400_BAD_REQUEST)

    discussion.delete()

    return Response("success")


@api_view(["POST"])
@login_required
def star_discussion(request, discussion_id):
    try:
        discussion = Discussion.objects.get(pk=discussion_id)
    except:
        return Response("Discussão não encontrada!", status=status.HTTP_404_NOT_FOUND)

    if DiscussionStar.objects.filter(profile=request.user.profile, discussion=discussion).exists():
        return Response("Você não pode curtir a mesma discussão mais de uma vez!", status=status.HTTP_400_BAD_REQUEST)

    DiscussionStar.objects.create(profile=request.user.profile, discussion=discussion)

    return Response("success")


@api_view(["DELETE"])
@login_required
def unstar_discussion(request, discussion_id):
    try:
        discussion = Discussion.objects.get(pk=discussion_id)
    except:
        return Response("Discussão não encontrada!", status=status.HTTP_404_NOT_FOUND)

    try:
        discussion_star = DiscussionStar.objects.get(profile=request.user.profile, discussion=discussion)
    except:
        return Response("Curtida não encontrada!", status=status.HTTP_404_NOT_FOUND)

    discussion_star.delete()

    return Response("success")


@api_view(["POST"])
@login_required
def reply_discussion(request, discussion_id):
    try:
        content = request.data["content"]
    except:
        return Response("Dados inválidos!", status=status.HTTP_400_BAD_REQUEST)

    try:
        discussion = Discussion.objects.get(pk=discussion_id)
    except:
        return Response("Discussão não encontrada!", status=status.HTTP_404_NOT_FOUND)

    if len(content) < 3:
        return Response("O comentário não pode ter menos de 3 caracteres!", status=status.HTTP_400_BAD_REQUEST)

    if len(content) > 300:
        return Response("Respeite o limite de caracteres!", status=status.HTTP_400_BAD_REQUEST)

    DiscussionReply.objects.create(content=content, profile=request.user.profile, discussion=discussion)

    return Response("success")


@api_view(["DELETE"])
@login_required
def delete_discussion_reply(request, reply_id):
    try:
        reply = DiscussionReply.objects.get(pk=reply_id)
    except:
        return Response("Comentário não encontrado!", status=status.HTTP_404_NOT_FOUND)

    if reply.profile != request.user.profile:
        return Response("O comentário não é seu!", status=status.HTTP_401_UNAUTHORIZED)

    reply.delete()

    return Response("success")
