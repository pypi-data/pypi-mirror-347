# llm-fragments-zohoticket

[LLM plugin](https://llm.datasette.io/en/stable/plugins/index.html) for pulling ticket conversations from [Zoho Desk](https://www.zoho.com/desk/).

## Installation

```bash
llm install llm-fragments-zohoticket
```

## Setup

1. Create a Self Client and obtain your `client_id` and `client_secret` from https://api-console.zoho.com/
2. Obtain the `organisation_id` from Settings > Developer Space > APIs > API Authentication
3. Provide the `client_id` as `ZOHODESK_CLIENT_ID`, `client_secret` as `ZOHODESK_CLIENT_SECRET` and `organisation_id` as `ZOHODESK_ORG_ID` in your environment.

## Usage

```bash
llm -f zohoticket:12345678 "summarize this conversation."
```
