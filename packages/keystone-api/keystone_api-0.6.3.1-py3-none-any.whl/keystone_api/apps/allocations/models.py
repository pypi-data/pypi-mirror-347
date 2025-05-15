"""ORM for application specific database models.

Model objects are used to define the expected schema for individual database
tables and provide an object-oriented interface for executing database logic.
Each model reflects a different database and defines low-level defaults for how
the associated table/fields/records are presented by parent interfaces.
"""

from __future__ import annotations

import abc
import os
from datetime import date

from auditlog.registry import auditlog
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import truncatechars

from apps.allocations.managers import AllocationManager
from apps.research_products.models import Grant, Publication
from apps.users.models import Team, User

__all__ = [
    'Allocation',
    'AllocationRequest',
    'AllocationReview',
    'Attachment',
    'Cluster',
    'Comment',
    'TeamModelInterface',
]


class TeamModelInterface:
    """Interface class for database models affiliated with a team."""

    @abc.abstractmethod
    def get_team(self) -> Team:
        """Return the user team tied to the current record."""


@auditlog.register()
class Allocation(TeamModelInterface, models.Model):
    """User service unit allocation."""

    requested = models.PositiveIntegerField()
    awarded = models.PositiveIntegerField(null=True, blank=True)
    final = models.PositiveIntegerField(null=True, blank=True)

    cluster: Cluster = models.ForeignKey('Cluster', on_delete=models.CASCADE)
    request: AllocationRequest = models.ForeignKey('AllocationRequest', on_delete=models.CASCADE)

    objects = AllocationManager()

    def get_team(self) -> Team:
        """Return the user team tied to the current record."""

        return self.request.team

    def __str__(self) -> str:  # pragma: nocover
        """Return a human-readable summary of the allocation."""

        return f'{self.cluster} allocation for {self.request.team}'


@auditlog.register()
class AllocationRequest(TeamModelInterface, models.Model):
    """User request for additional service units on one or more clusters."""

    class StatusChoices(models.TextChoices):
        """Enumerated choices for the `status` field."""

        PENDING = 'PD', 'Pending'
        APPROVED = 'AP', 'Approved'
        DECLINED = 'DC', 'Declined'
        CHANGES = 'CR', 'Changes Requested'

    title = models.CharField(max_length=250)
    description = models.TextField(max_length=20_000)
    submitter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='submitted_allocationrequest_set')
    submitted = models.DateField(auto_now=True)
    status = models.CharField(max_length=2, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    active = models.DateField(null=True, blank=True)
    expire = models.DateField(null=True, blank=True)

    team: Team = models.ForeignKey(Team, on_delete=models.CASCADE)
    assignees: User = models.ManyToManyField(User, blank=True, related_name='assigned_allocationrequest_set')
    publications: Publication = models.ManyToManyField(Publication, blank=True)
    grants: Grant = models.ManyToManyField(Grant, blank=True)

    def clean(self) -> None:
        """Validate the model instance.

        Raises:
            ValidationError: When the model instance data is not valid.
        """

        if self.active and self.expire and self.active >= self.expire:
            raise ValidationError('The expiration date must come after the activation date.')

    def get_team(self) -> Team:
        """Return the user team tied to the current record."""

        return self.team

    def get_days_until_expire(self) -> int:
        """Calculate the number of days until this request expires."""

        return (self.expire - date.today()).days if self.expire else None

    def __str__(self) -> str:  # pragma: nocover
        """Return the request title as a string."""

        return truncatechars(self.title, 100)


@auditlog.register(exclude_fields=["last_modified"])
class AllocationReview(TeamModelInterface, models.Model):
    """Reviewer feedback for an allocation request."""

    class StatusChoices(models.TextChoices):
        """Enumerated choices for the `status` field."""

        APPROVED = 'AP', 'Approved'
        DECLINED = 'DC', 'Declined'
        CHANGES = 'CR', 'Changes Requested'

    status = models.CharField(max_length=2, choices=StatusChoices.choices)
    last_modified = models.DateTimeField(auto_now=True)

    request: AllocationRequest = models.ForeignKey(AllocationRequest, on_delete=models.CASCADE)
    reviewer: User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)

    def get_team(self) -> Team:
        """Return the user team tied to the current record."""

        return self.request.team

    def __str__(self) -> str:  # pragma: nocover
        """Return a human-readable identifier for the allocation request."""

        return f'{self.reviewer} review for \"{self.request.title}\"'


@auditlog.register()
class Attachment(TeamModelInterface, models.Model):
    """File data uploaded by users."""

    file = models.FileField(upload_to='allocations')
    name = models.CharField(max_length=250, blank=True)
    uploaded = models.DateTimeField(auto_now=True)

    request = models.ForeignKey('AllocationRequest', on_delete=models.CASCADE)

    def save(self, *args, **kwargs) -> None:
        """Persist the ORM instance to the database"""

        # Set the default name to match the file path
        if not self.name:
            self.name = os.path.basename(self.file.path)

        super().save(*args, **kwargs)

    def get_team(self) -> Team:
        """Return the user team tied to the current record."""

        return self.request.team


@auditlog.register()
class Cluster(models.Model):
    """A slurm cluster and it's associated management settings."""

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=150, null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: nocover
        """Return the cluster name as a string."""

        return str(self.name)


@auditlog.register()
class Comment(models.Model):
    """Comments associated with allocation reviews."""

    content = models.TextField(max_length=2_000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)

    request = models.ForeignKey('AllocationRequest', on_delete=models.CASCADE, related_name='comments')

    def get_team(self) -> Team:
        """Return the user team tied to the current record."""

        return self.request.team

    def __str__(self) -> str:
        """Return a string representation of the comment."""

        return f'Comment by {self.user} made on request "{self.request.title[:50]}"'
