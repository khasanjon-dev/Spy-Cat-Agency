from django.db import models


class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Mission(models.Model):
    cat = models.ForeignKey(
        SpyCat,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="missions",
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Mission #{self.id}"


class Target(models.Model):
    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name="targets",
    )
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} (mission={self.mission_id})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        mission = self.mission
        if (
            mission.targets.exists()
            and not mission.targets.filter(is_completed=False).exists()
        ):
            if not mission.is_completed:
                mission.is_completed = True
                mission.save(update_fields=["is_completed"])
