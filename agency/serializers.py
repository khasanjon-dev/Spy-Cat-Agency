from rest_framework import serializers

from .models import SpyCat, Mission, Target
from .services import is_valid_breed


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ["id", "name", "years_of_experience", "breed", "salary"]

    def validate_years_of_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        return value

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

    def validate_breed(self, value):
        if not is_valid_breed(value):
            raise serializers.ValidationError(
                "Invalid cat breed according to TheCatAPI."
            )
        return value

    def update(self, instance, validated_data):
        allowed_fields = {"salary"}
        extra_fields = set(validated_data.keys()) - allowed_fields
        if extra_fields:
            raise serializers.ValidationError("Only salary can be updated.")
        return super().update(instance, validated_data)


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["id", "mission", "name", "country", "notes", "is_completed"]
        read_only_fields = ["id", "mission"]

    def validate(self, attrs):
        instance: Target | None = self.instance
        mission = instance.mission if instance else None

        if instance:
            mission = instance.mission
            target_completed = instance.is_completed
            mission_completed = mission.is_completed

            notes_incoming = "notes" in attrs
            is_completed_incoming = "is_completed" in attrs

            if mission_completed or target_completed:
                if notes_incoming or is_completed_incoming:
                    raise serializers.ValidationError(
                        "Notes or completion status cannot be updated when target or mission is completed."
                    )
        return attrs


class MissionCreateTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["name", "country", "notes", "is_completed"]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Target name is required.")
        return value

    def validate_country(self, value):
        if not value:
            raise serializers.ValidationError("Country is required.")
        return value


class MissionSerializer(serializers.ModelSerializer):
    targets = MissionCreateTargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ["id", "cat", "is_completed", "targets", "created_at"]
        read_only_fields = ["id", "is_completed", "created_at"]

    def validate_targets(self, value):
        if not (1 <= len(value) <= 3):
            raise serializers.ValidationError(
                "Mission must have between 1 and 3 targets."
            )
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop("targets")
        mission = Mission.objects.create(**validated_data)

        for t in targets_data:
            Target.objects.create(mission=mission, **t)
        return mission


class MissionDetailSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, read_only=True)
    cat = SpyCatSerializer(read_only=True)

    class Meta:
        model = Mission
        fields = ["id", "cat", "is_completed", "targets", "created_at"]
