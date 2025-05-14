from __future__ import annotations
from pydantic import Field
from maleo_foundation.managers.client.base import ClientServiceControllers

from maleo_token.client.controllers.http import MaleoTokenHTTPController
class MaleoTokenControllers(ClientServiceControllers):
    http:MaleoTokenHTTPController = Field(..., description="Token's http controller")