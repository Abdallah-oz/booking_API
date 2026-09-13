class AppException(Exception):
    """Exception de base pour toutes les erreurs métier de l'application."""
    def __init__(self, detail: str):
        self.detail = detail


class NotFoundException(AppException):
    """Levée quand une ressource demandée n'existe pas."""
    pass


class PermissionDeniedException(AppException):
    """Levée quand l'utilisateur n'a pas le droit d'effectuer une action."""
    pass


class ConflictException(AppException):
    """Levée quand une action entre en conflit avec l'état actuel (ex: chambre indisponible)."""
    pass