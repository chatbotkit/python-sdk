from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class IntegrationClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.widget = WidgetClient(client)
        self.slack = SlackClient(client)
        self.discord = DiscordClient(client)
        self.whatsapp = WhatsAppClient(client)
        self.telegram = TelegramClient(client)
        self.messenger = MessengerClient(client)
        self.instagram = InstagramClient(client)
        self.notion = NotionClient(client)
        self.sitemap = SitemapClient(client)
        self.support = SupportClient(client)
        self.extract = ExtractClient(client)
        self.twilio = TwilioClient(client)
        self.email = EmailClient(client)
        self.mcp_server = McpServerClient(client)
        self.skill_server = SkillServerClient(client)
        self.microsoft_teams = MicrosoftTeamsClient(client)
        self.google_chat = GoogleChatClient(client)
        self.trigger = TriggerClient(client)


class WidgetClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationWidgetListParams | Request | None = None,
    ) -> Response[types.IntegrationWidgetListResponse, types.IntegrationWidgetListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/widget/list",
            query=request,
            parse=types.IntegrationWidgetListResponse.from_dict,
            stream_parse=types.IntegrationWidgetListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationWidgetFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/widget/{integration_id}/fetch",
            parse=types.IntegrationWidgetFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationWidgetCreateRequest | Request,
    ) -> Response[types.IntegrationWidgetCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/widget/create",
            record=request,
            parse=types.IntegrationWidgetCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationWidgetUpdateRequest | Request,
    ) -> Response[types.IntegrationWidgetUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/widget/{integration_id}/update",
            record=request,
            parse=types.IntegrationWidgetUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationWidgetDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/widget/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationWidgetDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationWidgetSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/widget/{integration_id}/setup",
            record=request or {},
            parse=types.IntegrationWidgetSetupResponse.from_dict,
        )


class SlackClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationSlackListParams | Request | None = None,
    ) -> Response[types.IntegrationSlackListResponse, types.IntegrationSlackListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/slack/list",
            query=request,
            parse=types.IntegrationSlackListResponse.from_dict,
            stream_parse=types.IntegrationSlackListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationSlackFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/slack/{integration_id}/fetch",
            parse=types.IntegrationSlackFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationSlackCreateRequest | Request,
    ) -> Response[types.IntegrationSlackCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/slack/create",
            record=request,
            parse=types.IntegrationSlackCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationSlackUpdateRequest | Request,
    ) -> Response[types.IntegrationSlackUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/slack/{integration_id}/update",
            record=request,
            parse=types.IntegrationSlackUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationSlackDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/slack/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationSlackDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationSlackSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/slack/{integration_id}/setup",
            record=request or {},
            parse=types.IntegrationSlackSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.SlackInitiateRequest | Request,
    ) -> Response[types.SlackInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/slack/{integration_id}/initiate",
            record=request,
            parse=types.SlackInitiateResponse.from_dict,
        )


class DiscordClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationDiscordListParams | Request | None = None,
    ) -> Response[types.IntegrationDiscordListResponse, types.IntegrationDiscordListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/discord/list",
            query=request,
            parse=types.IntegrationDiscordListResponse.from_dict,
            stream_parse=types.IntegrationDiscordListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationDiscordFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/discord/{integration_id}/fetch",
            parse=types.IntegrationDiscordFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationDiscordCreateRequest | Request,
    ) -> Response[types.IntegrationDiscordCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/discord/create",
            record=request,
            parse=types.IntegrationDiscordCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationDiscordUpdateRequest | Request,
    ) -> Response[types.IntegrationDiscordUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/discord/{integration_id}/update",
            record=request,
            parse=types.IntegrationDiscordUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationDiscordDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/discord/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationDiscordDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationDiscordSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/discord/{integration_id}/setup",
            record=request or {},
            parse=types.IntegrationDiscordSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.DiscordInitiateRequest | Request,
    ) -> Response[types.DiscordInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/discord/{integration_id}/initiate",
            record=request,
            parse=types.DiscordInitiateResponse.from_dict,
        )


class WhatsAppClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationWhatsAppListParams | Request | None = None,
    ) -> Response[types.IntegrationWhatsAppListResponse, types.IntegrationWhatsAppListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/whatsapp/list",
            query=request,
            parse=types.IntegrationWhatsAppListResponse.from_dict,
            stream_parse=types.IntegrationWhatsAppListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationWhatsAppFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/whatsapp/{integration_id}/fetch",
            parse=types.IntegrationWhatsAppFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationWhatsAppCreateRequest | Request,
    ) -> Response[types.IntegrationWhatsAppCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/whatsapp/create",
            record=request,
            parse=types.IntegrationWhatsAppCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationWhatsAppUpdateRequest | Request,
    ) -> Response[types.IntegrationWhatsAppUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/whatsapp/{integration_id}/update",
            record=request,
            parse=types.IntegrationWhatsAppUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationWhatsAppDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/whatsapp/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationWhatsAppDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationWhatsAppSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/whatsapp/{integration_id}/setup",
            record=request or {},
            parse=types.IntegrationWhatsAppSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.WhatsappInitiateRequest | Request,
    ) -> Response[types.WhatsappInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/whatsapp/{integration_id}/initiate",
            record=request,
            parse=types.WhatsappInitiateResponse.from_dict,
        )


class TelegramClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationTelegramListParams | Request | None = None,
    ) -> Response[types.IntegrationTelegramListResponse, types.IntegrationTelegramListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/telegram/list",
            query=request,
            parse=types.IntegrationTelegramListResponse.from_dict,
            stream_parse=types.IntegrationTelegramListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationTelegramFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/telegram/{integration_id}/fetch",
            parse=types.IntegrationTelegramFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationTelegramCreateRequest | Request,
    ) -> Response[types.IntegrationTelegramCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/telegram/create",
            record=request,
            parse=types.IntegrationTelegramCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationTelegramUpdateRequest | Request,
    ) -> Response[types.IntegrationTelegramUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/telegram/{integration_id}/update",
            record=request,
            parse=types.IntegrationTelegramUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationTelegramDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/telegram/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationTelegramDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationTelegramSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/telegram/{integration_id}/setup",
            record=request or {},
            parse=types.IntegrationTelegramSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.TelegramInitiateRequest | Request,
    ) -> Response[types.TelegramInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/telegram/{integration_id}/initiate",
            record=request,
            parse=types.TelegramInitiateResponse.from_dict,
        )


class MessengerClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationMessengerListParams | Request | None = None,
    ) -> Response[types.IntegrationMessengerListResponse, types.IntegrationMessengerListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/messenger/list",
            query=request,
            parse=types.IntegrationMessengerListResponse.from_dict,
            stream_parse=types.IntegrationMessengerListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationMessengerFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/messenger/{integration_id}/fetch",
            parse=types.IntegrationMessengerFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationMessengerCreateRequest | Request,
    ) -> Response[types.IntegrationMessengerCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/messenger/create",
            record=request,
            parse=types.IntegrationMessengerCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationMessengerUpdateRequest | Request,
    ) -> Response[types.IntegrationMessengerUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/messenger/{integration_id}/update",
            record=request,
            parse=types.IntegrationMessengerUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationMessengerDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/messenger/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationMessengerDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationMessengerSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/messenger/{integration_id}/setup",
            record=request or {},
            parse=types.IntegrationMessengerSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.MessengerInitiateRequest | Request,
    ) -> Response[types.MessengerInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/messenger/{integration_id}/initiate",
            record=request,
            parse=types.MessengerInitiateResponse.from_dict,
        )


class InstagramClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationInstagramListParams | Request | None = None,
    ) -> Response[types.IntegrationInstagramListResponse, types.IntegrationInstagramListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/instagram/list",
            query=request,
            parse=types.IntegrationInstagramListResponse.from_dict,
            stream_parse=types.IntegrationInstagramListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationInstagramFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/instagram/{integration_id}/fetch",
            parse=types.IntegrationInstagramFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationInstagramCreateRequest | Request,
    ) -> Response[types.IntegrationInstagramCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/instagram/create",
            record=request,
            parse=types.IntegrationInstagramCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationInstagramUpdateRequest | Request,
    ) -> Response[types.IntegrationInstagramUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/instagram/{integration_id}/update",
            record=request,
            parse=types.IntegrationInstagramUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationInstagramDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/instagram/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationInstagramDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationInstagramSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/instagram/{integration_id}/setup",
            record=request or {},
            parse=types.IntegrationInstagramSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.InstagramInitiateRequest | Request,
    ) -> Response[types.InstagramInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/instagram/{integration_id}/initiate",
            record=request,
            parse=types.InstagramInitiateResponse.from_dict,
        )


class NotionClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationNotionListParams | Request | None = None,
    ) -> Response[types.IntegrationNotionListResponse, types.IntegrationNotionListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/notion/list",
            query=request,
            parse=types.IntegrationNotionListResponse.from_dict,
            stream_parse=types.IntegrationNotionListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationNotionFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/notion/{integration_id}/fetch",
            parse=types.IntegrationNotionFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationNotionCreateRequest | Request,
    ) -> Response[types.IntegrationNotionCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/notion/create",
            record=request,
            parse=types.IntegrationNotionCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationNotionUpdateRequest | Request,
    ) -> Response[types.IntegrationNotionUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/notion/{integration_id}/update",
            record=request,
            parse=types.IntegrationNotionUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationNotionDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/notion/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationNotionDeleteResponse.from_dict,
        )

    def sync(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationNotionSyncResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/notion/{integration_id}/sync",
            record=request or {},
            parse=types.IntegrationNotionSyncResponse.from_dict,
        )


class SitemapClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationSitemapListParams | Request | None = None,
    ) -> Response[types.IntegrationSitemapListResponse, types.IntegrationSitemapListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/sitemap/list",
            query=request,
            parse=types.IntegrationSitemapListResponse.from_dict,
            stream_parse=types.IntegrationSitemapListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationSitemapFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/sitemap/{integration_id}/fetch",
            parse=types.IntegrationSitemapFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationSitemapCreateRequest | Request,
    ) -> Response[types.IntegrationSitemapCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/sitemap/create",
            record=request,
            parse=types.IntegrationSitemapCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationSitemapUpdateRequest | Request,
    ) -> Response[types.IntegrationSitemapUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/sitemap/{integration_id}/update",
            record=request,
            parse=types.IntegrationSitemapUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationSitemapDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/sitemap/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationSitemapDeleteResponse.from_dict,
        )

    def sync(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationSitemapSyncResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/sitemap/{integration_id}/sync",
            record=request or {},
            parse=types.IntegrationSitemapSyncResponse.from_dict,
        )


class SupportClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationSupportListParams | Request | None = None,
    ) -> Response[types.IntegrationSupportListResponse, types.IntegrationSupportListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/support/list",
            query=request,
            parse=types.IntegrationSupportListResponse.from_dict,
            stream_parse=types.IntegrationSupportListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationSupportFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/support/{integration_id}/fetch",
            parse=types.IntegrationSupportFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationSupportCreateRequest | Request,
    ) -> Response[types.IntegrationSupportCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/support/create",
            record=request,
            parse=types.IntegrationSupportCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationSupportUpdateRequest | Request,
    ) -> Response[types.IntegrationSupportUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/support/{integration_id}/update",
            record=request,
            parse=types.IntegrationSupportUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationSupportDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/support/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationSupportDeleteResponse.from_dict,
        )


class ExtractClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationExtractListParams | Request | None = None,
    ) -> Response[types.IntegrationExtractListResponse, types.IntegrationExtractListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/extract/list",
            query=request,
            parse=types.IntegrationExtractListResponse.from_dict,
            stream_parse=types.IntegrationExtractListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationExtractFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/extract/{integration_id}/fetch",
            parse=types.IntegrationExtractFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationExtractCreateRequest | Request,
    ) -> Response[types.IntegrationExtractCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/extract/create",
            record=request,
            parse=types.IntegrationExtractCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationExtractUpdateRequest | Request,
    ) -> Response[types.IntegrationExtractUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/extract/{integration_id}/update",
            record=request,
            parse=types.IntegrationExtractUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationExtractDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/extract/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationExtractDeleteResponse.from_dict,
        )


class TwilioClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationTwilioListParams | Request | None = None,
    ) -> Response[types.IntegrationTwilioListResponse, types.IntegrationTwilioListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/twilio/list",
            query=request,
            parse=types.IntegrationTwilioListResponse.from_dict,
            stream_parse=types.IntegrationTwilioListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationTwilioFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/twilio/{integration_id}/fetch",
            parse=types.IntegrationTwilioFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationTwilioCreateRequest | Request,
    ) -> Response[types.IntegrationTwilioCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/twilio/create",
            record=request,
            parse=types.IntegrationTwilioCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationTwilioUpdateRequest | Request,
    ) -> Response[types.IntegrationTwilioUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/twilio/{integration_id}/update",
            record=request,
            parse=types.IntegrationTwilioUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationTwilioDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/twilio/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationTwilioDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationTwilioSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/twilio/{integration_id}/setup",
            record=request or {},
            parse=types.IntegrationTwilioSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.TwilioInitiateRequest | Request,
    ) -> Response[types.TwilioInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/twilio/{integration_id}/initiate",
            record=request,
            parse=types.TwilioInitiateResponse.from_dict,
        )


class EmailClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.EmailIntegrationListParams | Request | None = None,
    ) -> Response[types.EmailIntegrationListResponse, types.EmailIntegrationListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/email/list",
            query=request,
            parse=types.EmailIntegrationListResponse.from_dict,
            stream_parse=types.EmailIntegrationListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.EmailIntegrationFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/email/{integration_id}/fetch",
            parse=types.EmailIntegrationFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.EmailIntegrationCreateRequest | Request,
    ) -> Response[types.EmailIntegrationCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/email/create",
            record=request,
            parse=types.EmailIntegrationCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.EmailIntegrationUpdateRequest | Request,
    ) -> Response[types.EmailIntegrationUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/email/{integration_id}/update",
            record=request,
            parse=types.EmailIntegrationUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.EmailIntegrationDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/email/{integration_id}/delete",
            record=request or {},
            parse=types.EmailIntegrationDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.EmailIntegrationSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/email/{integration_id}/setup",
            record=request or {},
            parse=types.EmailIntegrationSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.EmailInitiateRequest | Request,
    ) -> Response[types.EmailInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/email/{integration_id}/initiate",
            record=request,
            parse=types.EmailInitiateResponse.from_dict,
        )


class McpServerClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.IntegrationMCPServerListParams | Request | None = None,
    ) -> Response[types.IntegrationMCPServerListResponse, types.IntegrationMCPServerListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/mcpserver/list",
            query=request,
            parse=types.IntegrationMCPServerListResponse.from_dict,
            stream_parse=types.IntegrationMCPServerListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.IntegrationMCPServerFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/mcpserver/{integration_id}/fetch",
            parse=types.IntegrationMCPServerFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.IntegrationMCPServerCreateRequest | Request,
    ) -> Response[types.IntegrationMCPServerCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/mcpserver/create",
            record=request,
            parse=types.IntegrationMCPServerCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.IntegrationMCPServerUpdateRequest | Request,
    ) -> Response[types.IntegrationMCPServerUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/mcpserver/{integration_id}/update",
            record=request,
            parse=types.IntegrationMCPServerUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.IntegrationMCPServerDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/mcpserver/{integration_id}/delete",
            record=request or {},
            parse=types.IntegrationMCPServerDeleteResponse.from_dict,
        )


class SkillServerClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.SkillServerIntegrationListParams | Request | None = None,
    ) -> Response[types.SkillServerIntegrationListResponse, types.SkillServerIntegrationListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/skillserver/list",
            query=request,
            parse=types.SkillServerIntegrationListResponse.from_dict,
            stream_parse=types.SkillServerIntegrationListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.SkillServerIntegrationFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/skillserver/{integration_id}/fetch",
            parse=types.SkillServerIntegrationFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.SkillServerIntegrationCreateRequest | Request,
    ) -> Response[types.SkillServerIntegrationCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/skillserver/create",
            record=request,
            parse=types.SkillServerIntegrationCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.SkillServerIntegrationUpdateRequest | Request,
    ) -> Response[types.SkillServerIntegrationUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/skillserver/{integration_id}/update",
            record=request,
            parse=types.SkillServerIntegrationUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.SkillServerIntegrationDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/skillserver/{integration_id}/delete",
            record=request or {},
            parse=types.SkillServerIntegrationDeleteResponse.from_dict,
        )


class MicrosoftTeamsClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.MicrosoftteamsIntegrationListParams | Request | None = None,
    ) -> Response[types.MicrosoftteamsIntegrationListResponse, types.MicrosoftteamsIntegrationListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/microsoftteams/list",
            query=request,
            parse=types.MicrosoftteamsIntegrationListResponse.from_dict,
            stream_parse=types.MicrosoftteamsIntegrationListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.MicrosoftteamsIntegrationFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/microsoftteams/{integration_id}/fetch",
            parse=types.MicrosoftteamsIntegrationFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.MicrosoftteamsIntegrationCreateRequest | Request,
    ) -> Response[types.MicrosoftteamsIntegrationCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/microsoftteams/create",
            record=request,
            parse=types.MicrosoftteamsIntegrationCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.MicrosoftteamsIntegrationUpdateRequest | Request,
    ) -> Response[types.MicrosoftteamsIntegrationUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/microsoftteams/{integration_id}/update",
            record=request,
            parse=types.MicrosoftteamsIntegrationUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.MicrosoftteamsIntegrationDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/microsoftteams/{integration_id}/delete",
            record=request or {},
            parse=types.MicrosoftteamsIntegrationDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.MicrosoftteamsIntegrationSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/microsoftteams/{integration_id}/setup",
            record=request or {},
            parse=types.MicrosoftteamsIntegrationSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.TeamsInitiateRequest | Request,
    ) -> Response[types.TeamsInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/microsoftteams/{integration_id}/initiate",
            record=request,
            parse=types.TeamsInitiateResponse.from_dict,
        )


class GoogleChatClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.GooglechatIntegrationListParams | Request | None = None,
    ) -> Response[types.GooglechatIntegrationListResponse, types.GooglechatIntegrationListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/googlechat/list",
            query=request,
            parse=types.GooglechatIntegrationListResponse.from_dict,
            stream_parse=types.GooglechatIntegrationListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.GooglechatIntegrationFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/googlechat/{integration_id}/fetch",
            parse=types.GooglechatIntegrationFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.GooglechatIntegrationCreateRequest | Request,
    ) -> Response[types.GooglechatIntegrationCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/googlechat/create",
            record=request,
            parse=types.GooglechatIntegrationCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.GooglechatIntegrationUpdateRequest | Request,
    ) -> Response[types.GooglechatIntegrationUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/googlechat/{integration_id}/update",
            record=request,
            parse=types.GooglechatIntegrationUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.GooglechatIntegrationDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/googlechat/{integration_id}/delete",
            record=request or {},
            parse=types.GooglechatIntegrationDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.GooglechatIntegrationSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/googlechat/{integration_id}/setup",
            record=request or {},
            parse=types.GooglechatIntegrationSetupResponse.from_dict,
        )

    def initiate(
        self,
        integration_id: str,
        request: types.GooglechatInitiateRequest | Request,
    ) -> Response[types.GooglechatInitiateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/googlechat/{integration_id}/initiate",
            record=request,
            parse=types.GooglechatInitiateResponse.from_dict,
        )


class TriggerClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.TriggerIntegrationListParams | Request | None = None,
    ) -> Response[types.TriggerIntegrationListResponse, types.TriggerIntegrationListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/integration/trigger/list",
            query=request,
            parse=types.TriggerIntegrationListResponse.from_dict,
            stream_parse=types.TriggerIntegrationListStreamItem.from_dict,
        )

    def fetch(self, integration_id: str) -> Response[types.TriggerIntegrationFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/trigger/{integration_id}/fetch",
            parse=types.TriggerIntegrationFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.TriggerIntegrationCreateRequest | Request,
    ) -> Response[types.TriggerIntegrationCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/integration/trigger/create",
            record=request,
            parse=types.TriggerIntegrationCreateResponse.from_dict,
        )

    def update(
        self,
        integration_id: str,
        request: types.TriggerIntegrationUpdateRequest | Request,
    ) -> Response[types.TriggerIntegrationUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/trigger/{integration_id}/update",
            record=request,
            parse=types.TriggerIntegrationUpdateResponse.from_dict,
        )

    def delete(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.TriggerIntegrationDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/trigger/{integration_id}/delete",
            record=request or {},
            parse=types.TriggerIntegrationDeleteResponse.from_dict,
        )

    def setup(
        self,
        integration_id: str,
        request: Request | None = None,
    ) -> Response[types.TriggerIntegrationSetupResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/trigger/{integration_id}/setup",
            record=request or {},
            parse=types.TriggerIntegrationSetupResponse.from_dict,
        )

    def invoke(
        self,
        integration_id: str,
        request: types.TriggerIntegrationInvokeRequest | Request,
    ) -> Response[types.TriggerIntegrationInvokeResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/integration/trigger/{integration_id}/invoke",
            record=request,
            parse=types.TriggerIntegrationInvokeResponse.from_dict,
        )
