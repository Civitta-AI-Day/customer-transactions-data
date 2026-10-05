"""Audit logging.

Convention: write audit entries only through record(); never create AuditLog directly in views.
"""

from .models import AuditLog


def record(user, action: str, target, **metadata) -> AuditLog:
    """Record that `user` performed `action` on `target` (any model instance)."""
    return AuditLog.objects.create(
        user=user,
        action=action,
        target_type=target._meta.label_lower,
        target_id=target.pk,
        metadata=metadata,
    )
