# Apollo MCP Server

An MCP Server for the Apollo API.

## 🛠️ Tool List

This is automatically generated from OpenAPI schema for the Apollo API.


| Tool | Description |
|------|-------------|
| `get_cards` | Retrieves a list of cards filtered by parameters such as ID, account ID, status, date ranges, and pagination settings. |
| `card_request` | Creates a new card using the API and returns relevant information, requiring an API key in the request header. |
| `webhook_card_created` | Notifies when a new card is created by sending a POST request to the "/cards/webhook-card-created" endpoint. |
| `try_webhook_card_created` | Retrieves information about a specific card using its ID after a webhook card creation event. |
| `get_card` | Retrieves details for a specific card identified by its unique ID using the provided API key for authentication. |
| `block` | Updates the blocking status of a specified card using the PATCH method and returns a success status. |
| `unblock` | Unblocks a specified card and updates its status to allow transactions using the PATCH method. |
| `cancel` | Cancels the specified card using the provided identifier and returns a no-content response upon success. |
| `virtual_card_create` | Creates a virtual representation of a card identified by `{card_id}` using the provided API key. |
| `virtual_card_security_code` | Retrieves the security code for a specified virtual card (identified by card_id) using an API key for authentication. |
| `card_password_create` | Updates the password for a specific card, identified by `{card_id}`, using a POST request to the `/cards/{card_id}/password` endpoint, with authentication provided via an `apikey` in the request header. |
| `card_password_change` | Updates the password for the specified card using the provided apikey and returns a success status. |
| `webhook_autorize` | Authorizes a card transaction via a POST request to the endpoint, supporting idempotency through a header key. |
| `webhook_authorize` | Processes a card transaction using the provided API key and returns a success status upon completion. |
| `webhook_authorize_information` | Submits card information to the API using an "apikey" header for authentication and returns a success status upon completion. |
| `webhook_international_transactions` | Retrieves data linked to the specified date using a GET request at the "/adefinir" endpoint, authenticated via an API key in the header. |
