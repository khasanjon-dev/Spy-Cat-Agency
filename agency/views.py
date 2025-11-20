from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import SpyCat, Mission, Target
from .serializers import (
    SpyCatSerializer,
    MissionSerializer,
    MissionDetailSerializer,
    TargetSerializer,
)


class SpyCatViewSet(viewsets.ModelViewSet):
    """
    Spy Cats:
    - create
    - list
    - retrieve
    - update (PATCH: only salary)
    - destroy
    """

    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    """
    Missions:
    - POST /missions/ (with targets)
    - GET /missions/
    - GET /missions/{id}/
    - DELETE /missions/{id}/ (if not assigned to cat)
    - POST /missions/{id}/assign_cat/
    """

    queryset = Mission.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MissionDetailSerializer
        return MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat is not None:
            return Response(
                {
                    "detail": "Cannot delete a mission that is already assigned to a cat."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        cat_id = request.data.get("cat_id")

        if not cat_id:
            return Response(
                {"detail": "cat_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cat = SpyCat.objects.get(id=cat_id)
        except SpyCat.DoesNotExist:
            return Response(
                {"detail": "Cat not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        active_mission_exists = (
            Mission.objects.filter(cat=cat, is_completed=False)
            .exclude(id=mission.id)
            .exists()
        )

        if active_mission_exists:
            return Response(
                {"detail": "This cat already has an active mission."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        mission.cat = cat
        mission.save(update_fields=["cat"])
        return Response(
            MissionDetailSerializer(mission).data, status=status.HTTP_200_OK
        )


class TargetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Targets:
    - list
    - retrieve
    - update (PATCH)
    - destroy
    - create: DISABLED (must be via mission)
    """

    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def create(self, request, *args, **kwargs):
        # Targets must be created as part of mission creation
        return Response(
            {"detail": "Targets must be created as part of a mission."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
