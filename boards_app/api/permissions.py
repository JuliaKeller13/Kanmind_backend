from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedBoardUser(IsAuthenticated):
    """Require authentication for board operations."""