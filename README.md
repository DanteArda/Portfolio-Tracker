
# Portfolio Tracker

A Portfolio Tracker, Benchmarker and Blender.


## Features

- Web Interface utilising Streamlit
- Automatic data blending via API keys
- Scalable for adding support to multiple Brokers
- Support for:
    - Cash
    - Stocks
    - Crypto




## Run Locally

Clone the project

```bash
  git clone https://github.com/DanteArda/Portfolio-Tracker.git
```

Go to the project directory

```bash
  cd Portfolio-Tracker
```

Install dependencies

```bash
  requirements.txt
```

Start the server

```bash
  streamlit run app.py
```


## Usage/Examples
### Self-Usage

#### Adding Support for custom Broker

in ```broker_response.py```, extend from ```Broker``` class

```
Example_Broker(Broker):
    def __init__(self, apiKey):
        super().__init__(apiKey)
```

Use ```super().get_response(url, params)``` or ```super().post_response(url, payload)``` to retrieve data via websocket


### Error Handling

In ```exception.py``` is all the potential errors to be raised

1. When retrieving a response via API, ```BadStatusCodeError``` will be raised if the request is not successful, you must specify all cases for all potential status codes
