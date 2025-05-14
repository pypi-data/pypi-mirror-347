import os
import llm
import requests
from dataclasses import dataclass


@llm.hookimpl
def register_fragment_loaders(register):
    register("zohoticket", zohoticket_loader)


def zohoticket_loader(argument: str) -> llm.Fragment:
    """
    Load a Zoho Ticket as a fragment.

    Argument is the ticket ID.
    """

    client_id = os.getenv("ZOHODESK_CLIENT_ID", "")
    client_secret = os.getenv("ZOHODESK_CLIENT_SECRET", "")
    org_id = os.getenv("ZOHODESK_ORG_ID", "")

    messages = fetch_ticket_conversation(org_id, client_id, client_secret, argument)
    fragment = llm.Fragment(
        "\n".join(f"{message.actor}: {message.content}" for message in messages),
        source=f"Conversation for ticket {argument}",
    )
    return fragment


@dataclass
class TicketMessage:
    actor: str
    kind: str
    content: str


def fetch_ticket_conversation(
    org_id: str,
    client_id: str,
    client_secret: str,
    ticket_id: str,
) -> list[TicketMessage]:
    """
    Fetch the conversation of a Zoho ticket using the ticket ID.
    """
    url = f"https://desk.zoho.com/api/v1/tickets/{ticket_id}/conversations"

    access_token = obtain_access_token(org_id, client_id, client_secret)
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    payload = response.json()

    messages = []
    for thread in payload.get("data", []):
        thread_type = thread.get("type", "")
        author = thread.get("author", {}) or thread.get("commenter", {})
        author_type = author.get("type", "")
        summary = thread.get("summary", "") or thread.get("content", "")

        message = TicketMessage(
            actor=author_type.upper(), kind=thread_type.upper(), content=summary
        )
        messages.append(message)
    return messages


def obtain_access_token(
    org_id: str,
    client_id: str,
    client_secret: str,
) -> str:
    """
    Obtain an access token from Zoho using the client ID and secret.
    """

    if not org_id or not client_id or not client_secret:
        raise ValueError("Missing required credentials")

    url = "https://accounts.zoho.com/oauth/v2/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "Desk.tickets.READ",
        "soid": f"Desk.{org_id}",
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json().get("access_token", "")
