# llm-fragments-zohoticket

[LLM plugin](https://llm.datasette.io/en/stable/plugins/index.html) for pulling ticket conversations from [Zoho Desk](https://www.zoho.com/desk/).

## Installation

```bash
llm install llm-fragments-zohoticket
```

### Setting Up Zoho Desk API Credentials

1. **Create a Self Client**  
   Go to the [Zoho API Console](https://api-console.zoho.com/) and create a Self Client to obtain your `client_id` and `client_secret`.

2. **Retrieve Your Organisation ID**  
   In the Zoho Desk interface, navigate to:  
   **Settings > Developer Space > APIs > API Authentication**  
   to find your `organisation_id`.

3. **Set Environment Variables**  
   Add the following to your environment:

   - `ZOHODESK_CLIENT_ID` – Your Zoho API `client_id`
   - `ZOHODESK_CLIENT_SECRET` – Your Zoho API `client_secret`
   - `ZOHODESK_ORG_ID` – Your Zoho Desk `organisation_id`

## Usage

```bash
llm -f zohoticket:12345678 "summarize this conversation."
```
