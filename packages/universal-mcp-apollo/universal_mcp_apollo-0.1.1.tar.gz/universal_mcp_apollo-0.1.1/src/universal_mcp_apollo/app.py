from typing import Any
from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration

class ApolloApp(APIApplication):
    def __init__(self, integration: Integration = None, **kwargs) -> None:
        super().__init__(name='apollo', integration=integration, **kwargs)
        self.base_url = "{{card_base_url}}"

    def get_cards(self, page=None, limit=None, id=None, accountId=None, cardId=None, document=None, status=None, startCreateDate=None, endCreateDate=None, startCancelDate=None, endCancelDate=None, startEmbossDate=None, endEmbossDate=None) -> dict[str, Any]:
        """
        Retrieves a list of cards filtered by parameters such as ID, account ID, status, date ranges, and pagination settings.

        Args:
            page (string): Página atual Example: '1'.
            limit (string): Limite de registros por página Example: '10'.
            id (string): Id do registro Example: '5e6b6d256148e88ab095270b'.
            accountId (string): Id da conta do core brancário Example: '{{account_id}}'.
            cardId (string): Id do cartão Example: '{{card_id}}'.
            document (string): Documento Example: '52401224408'.
            status (string): Status do cartão (processing/ created/ active/ blocked/ canceled) Example: 'blocked'.
            startCreateDate (string): Data inicial da criação do cartão Example: '2020-04-06'.
            endCreateDate (string): Data final da criação do cartão Example: '2020-04-06'.
            startCancelDate (string): Data inicial do cancelamento do cartão Example: '2020-04-06'.
            endCancelDate (string): Data final do cancelamento do cartão Example: '2020-04-16'.
            startEmbossDate (string): Data inicial do emboçamento do cartão Example: '2020-04-02'.
            endEmbossDate (string): Data final do emboçamento do cartão Example: '2020-04-20'.

        Returns:
            dict[str, Any]: Get Cards - 200

        Tags:
            Apollo Card API
        """
        url = f"{self.base_url}/cards"
        query_params = {k: v for k, v in [('page', page), ('limit', limit), ('id', id), ('accountId', accountId), ('cardId', cardId), ('document', document), ('status', status), ('startCreateDate', startCreateDate), ('endCreateDate', endCreateDate), ('startCancelDate', startCancelDate), ('endCancelDate', endCancelDate), ('startEmbossDate', startEmbossDate), ('endEmbossDate', endEmbossDate)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def card_request(self, accountId=None, cardId=None, externalPrivateLabelAccountId=None, partner=None) -> dict[str, Any]:
        """
        Creates a new card using the API and returns relevant information, requiring an API key in the request header.

        Args:
            accountId (string): accountId Example: '5e668a09605f73004fa22f6e'.
            cardId (string): cardId Example: '5e95cac932796f1ebcbc31d3'.
            externalPrivateLabelAccountId (string): externalPrivateLabelAccountId Example: '123456677'.
            partner (object): partner
                Example:
                ```json
                {
                  "accountId": "5e668a09605f73004fa22f6e",
                  "cardId": "5e95cac932796f1ebcbc31d3",
                  "externalPrivateLabelAccountId": "123456677",
                  "partner": {
                    "externalPartnerId": "c4e9dc79-a9f7-4b64-bd0b-16c9c8da7c2f",
                    "name": "Banco Z",
                    "urlBase": "https://xyz-core-api.baas.solutions",
                    "urnAuthorizeTransaction": "/card/transaction",
                    "urnInformationTransaction": "/card/information",
                    "urnInternationalTransaction": "/card/transaction/international"
                  }
                }
                ```

        Returns:
            dict[str, Any]: Create - Status 200

        Tags:
            Apollo Authorize API, important
        """
        request_body = {
            'accountId': accountId,
            'cardId': cardId,
            'externalPrivateLabelAccountId': externalPrivateLabelAccountId,
            'partner': partner,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/cards"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def webhook_card_created(self, cardId=None, bin=None, id=None, last4Digits=None, privateLabelAccount=None, token=None, validThru=None) -> Any:
        """
        Notifies when a new card is created by sending a POST request to the "/cards/webhook-card-created" endpoint.

        Args:
            cardId (string): Identifies the specific card associated with the webhook event being processed. Example: '{{card_id}}'.
            bin (string): bin
            id (string): id Example: 'fd8c5e2e-055a-434b-95f3-d0975989532a'.
            last4Digits (string): last4Digits
            privateLabelAccount (object): privateLabelAccount
            token (string): token
            validThru (string): validThru
                Example:
                ```json
                {
                  "bin": null,
                  "id": "fd8c5e2e-055a-434b-95f3-d0975989532a",
                  "last4Digits": null,
                  "privateLabelAccount": {
                    "accountId": "ed775fa1-6156-4577-812e-931ff7c430ab",
                    "codeProposal": null,
                    "createdAt": "0001-01-01T00:00:00",
                    "creditCards": [
                      {
                        "bin": "230993",
                        "expirationDate": "0525",
                        "id": "5cdafd15-da66-4ed0-b206-f84a118eb508",
                        "last4Digits": "9997",
                        "status": "created",
                        "token": "4caad3bc-fefb-4ee9-84e0-ca91e5d31189"
                      }
                    ],
                    "dateProposal": "0001-01-01T00:00:00",
                    "embossingName": null,
                    "financialInstitutionId": null,
                    "id": "fd8c5e2e-055a-434b-95f3-d0975989532a",
                    "logo": null,
                    "org": null,
                    "paymentMethodId": null,
                    "reference": null,
                    "status": null,
                    "updatedAt": "0001-01-01T00:00:00"
                  },
                  "token": null,
                  "validThru": null
                }
                ```

        Returns:
            Any: API response data.

        Tags:
            Apollo Card API
        """
        request_body = {
            'bin': bin,
            'id': id,
            'last4Digits': last4Digits,
            'privateLabelAccount': privateLabelAccount,
            'token': token,
            'validThru': validThru,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/cards/webhook-card-created"
        query_params = {k: v for k, v in [('cardId', cardId)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def try_webhook_card_created(self, card_id) -> Any:
        """
        Retrieves information about a specific card using its ID after a webhook card creation event.

        Args:
            card_id (string): card_id

        Returns:
            Any: API response data.

        Tags:
            Apollo Card API
        """
        if card_id is None:
            raise ValueError("Missing required parameter 'card_id'")
        url = f"{self.base_url}/cards/try-webhook-card-created/{card_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_card(self, card_id) -> dict[str, Any]:
        """
        Retrieves details for a specific card identified by its unique ID using the provided API key for authentication.

        Args:
            card_id (string): card_id

        Returns:
            dict[str, Any]: Get - Status 200

        Tags:
            Apollo Card API, important
        """
        if card_id is None:
            raise ValueError("Missing required parameter 'card_id'")
        url = f"{self.base_url}/cards/{card_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def block(self, card_id, isVirtual=None) -> Any:
        """
        Updates the blocking status of a specified card using the PATCH method and returns a success status.

        Args:
            card_id (string): card_id
            isVirtual (boolean): isVirtual
                Example:
                ```json
                {
                  "isVirtual": true
                }
                ```

        Returns:
            Any: Block - Status 204

        Tags:
            Apollo Card API, important
        """
        if card_id is None:
            raise ValueError("Missing required parameter 'card_id'")
        request_body = {
            'isVirtual': isVirtual,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/cards/{card_id}/block"
        query_params = {}
        response = self._patch(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def unblock(self, card_id, isVirtual=None) -> Any:
        """
        Unblocks a specified card and updates its status to allow transactions using the PATCH method.

        Args:
            card_id (string): card_id
            isVirtual (boolean): isVirtual
                Example:
                ```json
                {
                  "isVirtual": false
                }
                ```

        Returns:
            Any: Unblock - Status 204

        Tags:
            Apollo Card API
        """
        if card_id is None:
            raise ValueError("Missing required parameter 'card_id'")
        request_body = {
            'isVirtual': isVirtual,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/cards/{card_id}/unblock"
        query_params = {}
        response = self._patch(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def cancel(self, card_id, description=None, reason=None) -> Any:
        """
        Cancels the specified card using the provided identifier and returns a no-content response upon success.

        Args:
            card_id (string): card_id
            description (string): description Example: 'Perda'.
            reason (string): reason
                Example:
                ```json
                {
                  "description": "Perda",
                  "reason": "P"
                }
                ```

        Returns:
            Any: Cancel - Status 204

        Tags:
            Apollo Card API
        """
        if card_id is None:
            raise ValueError("Missing required parameter 'card_id'")
        request_body = {
            'description': description,
            'reason': reason,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/cards/{card_id}/cancel"
        query_params = {}
        response = self._patch(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def virtual_card_create(self, card_id) -> dict[str, Any]:
        """
        Creates a virtual representation of a card identified by `{card_id}` using the provided API key.

        Args:
            card_id (string): card_id

        Returns:
            dict[str, Any]: Status 200

        Tags:
            Apollo Card API
        """
        if card_id is None:
            raise ValueError("Missing required parameter 'card_id'")
        url = f"{self.base_url}/cards/{card_id}/virtual"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def virtual_card_security_code(self, card_id) -> dict[str, Any]:
        """
        Retrieves the security code for a specified virtual card (identified by card_id) using an API key for authentication.

        Args:
            card_id (string): card_id

        Returns:
            dict[str, Any]: Get - Status 200

        Tags:
            Apollo Card API
        """
        if card_id is None:
            raise ValueError("Missing required parameter 'card_id'")
        url = f"{self.base_url}/cards/{card_id}/virtual/security-code"
        response = self._get(url)
        response.raise_for_status()
        return response.json()

    def card_password_create(self, card_id, password=None, passwordConfirm=None) -> Any:
        """
        Updates the password for a specific card, identified by `{card_id}`, using a POST request to the `/cards/{card_id}/password` endpoint, with authentication provided via an `apikey` in the request header.

        Args:
            card_id (string): card_id
            password (string): password Example: '1234'.
            passwordConfirm (string): passwordConfirm
                Example:
                ```json
                {
                  "password": "1234",
                  "passwordConfirm": "1234"
                }
                ```

        Returns:
            Any: Block - Status 204

        Tags:
            Apollo Card API
        """
        if card_id is None:
            raise ValueError("Missing required parameter 'card_id'")
        request_body = {
            'password': password,
            'passwordConfirm': passwordConfirm,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/cards/{card_id}/password"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def card_password_change(self, card_id, password=None, passwordConfirm=None, passwordOld=None) -> Any:
        """
        Updates the password for the specified card using the provided apikey and returns a success status.

        Args:
            card_id (string): card_id
            password (string): password Example: '1234'.
            passwordConfirm (string): passwordConfirm Example: '1234'.
            passwordOld (string): passwordOld
                Example:
                ```json
                {
                  "password": "1234",
                  "passwordConfirm": "1234",
                  "passwordOld": "1234"
                }
                ```

        Returns:
            Any: Block - Status 204

        Tags:
            Apollo Card API
        """
        if card_id is None:
            raise ValueError("Missing required parameter 'card_id'")
        request_body = {
            'password': password,
            'passwordConfirm': passwordConfirm,
            'passwordOld': passwordOld,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/cards/{card_id}/password"
        query_params = {}
        response = self._patch(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def webhook_autorize(self, acquirer_code=None, additional_data=None, authorization_code_reason=None, capture=None, card_acceptor=None, card_id=None, cardholder_billing=None, mti=None, pan=None, pinblock=None, pos_data=None, processing_code=None, settlement_date=None, settlement_value=None, stan=None) -> Any:
        """
        Authorizes a card transaction via a POST request to the endpoint, supporting idempotency through a header key.

        Args:
            acquirer_code (string): acquirer_code Example: '013445'.
            additional_data (string): additional_data
            authorization_code_reason (string): authorization_code_reason Example: '00'.
            capture (object): capture
            card_acceptor (object): card_acceptor
            card_id (string): card_id Example: '52c6ed22-b256-4365-ad56-a7f64868bf0b'.
            cardholder_billing (object): cardholder_billing
            mti (string): mti Example: '0100'.
            pan (string): pan Example: 'xxxxxxxxxxx11962'.
            pinblock (string): pinblock Example: '000000xxxxxxxxx0'.
            pos_data (string): pos_data Example: '1025108006000826NN18 8JG'.
            processing_code (string): processing_code Example: '000000'.
            settlement_date (string): settlement_date Example: '2020-05-14T00:00:00.000Z'.
            settlement_value (object): settlement_value
            stan (string): stan
                Example:
                ```json
                {
                  "acquirer_code": "013445",
                  "additional_data": "",
                  "authorization_code_reason": "00",
                  "capture": {
                    "country": "GBR",
                    "entry_mode": "812",
                    "pos_capture_time": "2020-05-14T22:04:41.000",
                    "scheme_capture_time": "2020-05-14T20:04:41.000Z",
                    "value": {
                      "amount": 10000,
                      "currency": "USD"
                    }
                  },
                  "card_acceptor": {
                    "city": "London",
                    "country_or_us_state": "GBR",
                    "mcc": "5817",
                    "merchant_id": "5xxxxxxxxx203433",
                    "name": "PADDLE.NET* PADDLE",
                    "terminal_id": ""
                  },
                  "card_id": "52c6ed22-b256-4365-ad56-a7f64868bf0b",
                  "cardholder_billing": {
                    "amount": 60000,
                    "conversion_rate": "65856650",
                    "currency": "BRL"
                  },
                  "mti": "0100",
                  "pan": "xxxxxxxxxxx11962",
                  "pinblock": "000000xxxxxxxxx0",
                  "pos_data": "1025108006000826NN18 8JG",
                  "processing_code": "000000",
                  "settlement_date": "2020-05-14T00:00:00.000Z",
                  "settlement_value": {
                    "amount": 10000,
                    "currency": "USD"
                  },
                  "stan": "22xxxxx"
                }
                ```

        Returns:
            Any: API response data.

        Tags:
            Apollo Authorize API
        """
        request_body = {
            'acquirer_code': acquirer_code,
            'additional_data': additional_data,
            'authorization_code_reason': authorization_code_reason,
            'capture': capture,
            'card_acceptor': card_acceptor,
            'card_id': card_id,
            'cardholder_billing': cardholder_billing,
            'mti': mti,
            'pan': pan,
            'pinblock': pinblock,
            'pos_data': pos_data,
            'processing_code': processing_code,
            'settlement_date': settlement_date,
            'settlement_value': settlement_value,
            'stan': stan,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/cards/authorize"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def webhook_authorize(self, account_id=None, amount=None, card_acceptor=None, currency=None, date=None, last_4_digits=None, stan=None, status=None) -> Any:
        """
        Processes a card transaction using the provided API key and returns a success status upon completion.

        Args:
            account_id (string): account_id
            amount (number): amount Example: '0'.
            card_acceptor (object): card_acceptor
            currency (string): currency Example: 'BRL'.
            date (string): date
            last_4_digits (string): last_4_digits
            stan (string): stan
            status (string): status
                Example:
                ```json
                {
                  "account_id": "",
                  "amount": 0,
                  "card_acceptor": {
                    "Name": "",
                    "city": "",
                    "country_or_us_state": "",
                    "mcc": "",
                    "merchant_id": "",
                    "terminal_id": ""
                  },
                  "currency": "BRL",
                  "date": "",
                  "last_4_digits": "",
                  "stan": "",
                  "status": "approved"
                }
                ```

        Returns:
            Any: API response data.

        Tags:
            Core API
        """
        request_body = {
            'account_id': account_id,
            'amount': amount,
            'card_acceptor': card_acceptor,
            'currency': currency,
            'date': date,
            'last_4_digits': last_4_digits,
            'stan': stan,
            'status': status,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/card/transaction"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def webhook_authorize_information(self, account_id=None, amount=None, card_acceptor=None, currency=None, date=None, international=None, last_4_digits=None, stan=None) -> Any:
        """
        Submits card information to the API using an "apikey" header for authentication and returns a success status upon completion.

        Args:
            account_id (string): account_id
            amount (number): amount Example: '0'.
            card_acceptor (object): card_acceptor
            currency (string): currency Example: 'BRL'.
            date (string): date
            international (object): international
            last_4_digits (string): last_4_digits
            stan (string): stan
                Example:
                ```json
                {
                  "account_id": "",
                  "amount": 0,
                  "card_acceptor": {
                    "Name": "",
                    "city": "",
                    "country_or_us_state": "",
                    "mcc": "",
                    "merchant_id": "",
                    "terminal_id": ""
                  },
                  "currency": "BRL",
                  "date": "",
                  "international": {
                    "capture_amount": 0,
                    "capture_currency": "",
                    "conversion_rate": "",
                    "settlement_amount": 0,
                    "settlement_currency": ""
                  },
                  "last_4_digits": "",
                  "stan": ""
                }
                ```

        Returns:
            Any: API response data.

        Tags:
            Core API
        """
        request_body = {
            'account_id': account_id,
            'amount': amount,
            'card_acceptor': card_acceptor,
            'currency': currency,
            'date': date,
            'international': international,
            'last_4_digits': last_4_digits,
            'stan': stan,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/card/information"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def webhook_international_transactions(self, Date=None) -> dict[str, Any]:
        """
        Retrieves data linked to the specified date using a GET request at the "/adefinir" endpoint, authenticated via an API key in the header.

        Args:
            Date (string): Data da transação Example: '2020-01-20'.

        Returns:
            dict[str, Any]: 200 OK

        Tags:
            Core API
        """
        url = f"{self.base_url}/adefinir"
        query_params = {k: v for k, v in [('Date', Date)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_tools(self):
        return [
            self.get_cards,
            self.card_request,
            self.webhook_card_created,
            self.try_webhook_card_created,
            self.get_card,
            self.block,
            self.unblock,
            self.cancel,
            self.virtual_card_create,
            self.virtual_card_security_code,
            self.card_password_create,
            self.card_password_change,
            self.webhook_autorize,
            self.webhook_authorize,
            self.webhook_authorize_information,
            self.webhook_international_transactions
        ]
