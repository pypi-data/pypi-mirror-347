from pydantic import BaseModel, Field
from maleo_foundation.types import BaseTypes
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums
from maleo_token.enums import MaleoTokenEnums

class MaleoTokenParametersTransfers:
    class Base(BaseModel):
        system_role:MaleoMetadataSystemRoleEnums.SystemRole = Field(..., description="System role")
        organization_key:BaseTypes.OptionalString = Field(..., description="Organization's Key")
        identifier_type:MaleoTokenEnums.IdentifierType = Field(..., description="Identifier's type")
        identifier_value:str = Field(..., description="Identifier's value")
        password:str = Field(..., description="Password")