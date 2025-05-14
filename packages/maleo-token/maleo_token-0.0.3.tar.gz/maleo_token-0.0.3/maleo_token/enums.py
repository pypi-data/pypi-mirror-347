from enum import StrEnum

class MaleoTokenEnums:
    class ClientControllerType(StrEnum):
        HTTP = "http"

    class IdentifierType(StrEnum):
        USERNAME = "username"
        EMAIL = "email"
        PHONE = "phone"