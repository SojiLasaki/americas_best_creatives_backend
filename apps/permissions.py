from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """Full platform access."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_super_admin)


class IsAdminOrSuperAdmin(BasePermission):
    """Super Admin or Admin role."""

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
            and request.user.role in ('super_admin', 'admin')
        )


class IsAgentOrAdmin(BasePermission):
    """Agent, Admin, or Super Admin."""

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
            and request.user.role in ('super_admin', 'admin', 'agent')
        )


class IsCustomer(BasePermission):
    """Customer role."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_customer)


class IsDesigner(BasePermission):
    """Designer role."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_designer)


class IsAccountant(BasePermission):
    """Accountant role."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_accountant)


class IsCustomerSupport(BasePermission):
    """Customer Support role."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_customer_support)


class IsOwnerOrAdmin(BasePermission):
    """Owner of the object or admin/super-admin."""

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role in ('super_admin', 'admin'):
            return True
        # Support objects that have a `customer` or `user` attribute
        owner = getattr(obj, 'customer', None) or getattr(obj, 'user', None)
        return owner == request.user


class IsSameStationAdminOrSuperAdmin(BasePermission):
    """Admin sees only own station; Super Admin sees all."""

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_super_admin:
            return True
        if request.user.role == 'admin':
            try:
                user_station = request.user.profile.station
                obj_station = getattr(obj, 'station', None)
                return user_station == obj_station
            except Exception:
                return False
        return False
