from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedTaskUser(IsAuthenticated):
    """Require authentication for task operations."""