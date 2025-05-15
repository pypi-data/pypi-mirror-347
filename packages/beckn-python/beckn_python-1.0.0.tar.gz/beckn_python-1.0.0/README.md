# Beckn Protocol client for Python

### Installation

```bash
pip install beckn-python
```

or use the OG package manager:

```bash
uv add beckn-python
```

### Usage

```python
from beckn_python 
  import Transaction,
      # Meta, Registry

client = Transaction.ApiClient(
    configuration=Transaction.Configuration(
        host="https://api.example.com",
        api_key="example",
    )
)

data = Transaction.BecknApplicationPlatformBAPApi(
        client=client
    ).on_search_post(
        Transaction.OnSearch(
            context=Transaction.OnSearchContext(), 
            message=Transaction.OnSearchMessage()
        )
    )

print(data)
```