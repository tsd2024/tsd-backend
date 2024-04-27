class PlayerNotFoundException(Exception):
    pass


class LobbyNotFoundException(Exception):
    pass


class CardNotAvailableException(Exception):
    pass


class RevealNotReadyException(Exception):
    pass


class NotAdminException(Exception):
    pass


class CancelNotAvailableException(Exception):
    pass

class MissingTokenException(Exception):
    pass

class InvalidTokenException(Exception):
    pass
