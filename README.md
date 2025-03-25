# Wallets API

## Features

- Create and retrieve wallets
- Record transactions (credit or debit)
- Filter and sort wallets and transactions
- JSON:API-compliant request/response format
- PostgreSQL as the database backend
- Docker-based deployment

---


### Setup and Run
`docker compose up --build`

Access: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## API Endpoints (JSON:API format)

All requests and responses must follow the JSON:API specification.

### Create Wallet

```bash
  curl -X POST http://localhost:8000/api/v1/wallets/ \
-H "Content-Type: application/vnd.api+json" \
-H "Accept: application/vnd.api+json" \
-d '{
  "data": {
    "type": "wallets",
    "attributes": {
      "label": "Main Wallet"
    }
  }
}'

```

### List Wallets

```bash
  curl -X GET http://localhost:8000/api/v1/wallets/ \
-H "Accept: application/vnd.api+json"
```

### Retrieve Wallet

```bash
  curl -X GET http://localhost:8000/api/v1/wallets/1/ \
-H "Accept: application/vnd.api+json"

```

### Create Transaction


```bash
  curl -X POST http://localhost:8000/api/v1/transactions/ \
-H "Content-Type: application/vnd.api+json" \
-H "Accept: application/vnd.api+json" \
-d '{
  "data": {
    "type": "transactions",
    "attributes": {
      "amount": "250.00",
      "txid": "abc1234"
    },
    "relationships": {
      "wallet": {
        "data": {
          "type": "wallets",
          "id": "1"
        }
      }
    }
  }
}'

```

### List Transactions

```bash
  curl -X GET http://localhost:8000/api/v1/transactions/ \
-H "Accept: application/vnd.api+json"

```


### 🧪 Code Coverage Report
`python -m coverage run -m pytest src`

| Module                        | Statements | Missed | Coverage    |
|-------------------------------|------------|--------|-------------|
| `core/__init__.py`            | 0          | 0      | 100%        |
| `core/settings.py`            | 25         | 0      | 100%        |
| `tests/__init__.py`           | 0          | 0      | 100%        |
| `tests/conftest.py`           | 9          | 1      | 89%         |
| `tests/wallets/__init__.py`   | 0          | 0      | 100%        |
| `tests/wallets/factories.py`  | 13         | 0      | 100%        |
| `wallets/__init__.py`         | 0          | 0      | 100%        |
| `wallets/admin.py`            | 8          | 0      | 100%        |
| `wallets/apps.py`             | 4          | 0      | 100%        |
| `wallets/models.py`           | 19         | 2      | 89%         |
| **TOTAL**                     | **78**     | **3**  | **96%**     |
