# 🚆 weiche

This is an unofficial library wrapper around the API of the
Deutsche Bahn (DB) website for identifying connections.
It returns **realtime**, **live** data.
If you do not need this in your project I strongly recommend
not to use this API as it might break any moment if DB changes
the API for getting station and train connections.

It has a API compatibility layer to the
[`schiene`](https://pypi.org/project/schiene/) package for
easy drop-in replacement as
[`schiene`](https://pypi.org/project/schiene/) no longer
works.

## Requirements

- Python 3.10 and above
- requests package for the synchronous API and Schiene wrapper
- aiohttp for the asynchronous API

## Features

- Get connections between two stations
- Search stations by name
- Get station information

## Setup

$ python -m venv /path/to/venv
$ /path/to/venv/bin/python -m pip install weiche[sync,async,schiene]

## Usage

### Use the synchronous API

```python
from datetime import datetime
from weiche import SynchronousApi

api = SynchronousApi()

amsterdam_query = api.search_locations('Amsterdam', limit=1)
amsterdam = amsterdam_query[0]
munich_query = api.search_locations('München Hbf', limit=1)
munich = munich_query[0]

api.search_connections(
    at=datetime(2025,5,10,18,0,0),
    from_location=munich.id,
    to_location=amsterdam.id,
    limit=10,
)
```

You can also add an HTTP proxy to connect via as Bahn tends to block server ip addresses.

```python
from weiche import SynchronousApi

api = SynchronousApi(proxy="192.168.0.1:8888")
```

<details>
<summary>Response from Synchronous API</summary>

The return format is an object which can also be found in the
[objects.py](./src/weiche/objects.py) file.

Look for the [`Connection`](./src/weiche/objects.py#L175) class
and see the API definition there.

</details>

### Use the asynchronous API

```python
import asyncio
from datetime import datetime
from weiche import AsynchronousApi

async def search():
    api = AsynchronousApi()

    amsterdam_query = await api.search_locations('Amsterdam', limit=1)
    amsterdam = amsterdam_query[0]
    munich_query = await api.search_locations('München Hbf', limit=1)
    munich = munich_query[0]

    return await api.search_connections(
        at=datetime(2025,5,10,18,0,0),
        from_location=munich.id,
        to_location=amsterdam.id,
        limit=10,
    )

asyncio.get_event_loop().run_until_complete(search())
```

You can also add an HTTP proxy to connect via as Bahn tends to block server ip addresses.

```python
from weiche import AsynchronousApi

api = AsynchronousApi(proxy="192.168.0.1:8888")
```

<details>
<summary>Response from Asynchronous API</summary>

The return format is an object which can also be found in the
[objects.py](./src/weiche/objects.py) file.

Look for the [`Connection`](./src/weiche/objects.py#L175)
class and see the API definition there.

</details>

### Use the `schiene` compatibility layer

```python
from weiche import Schiene

Schiene().connections('Mannheim HbF', 'Stuttgart HbF')
```

You can also add an HTTP proxy to connect via as Bahn tends to block server ip addresses.

```python
from weiche import Schiene

api = Schiene(proxy="192.168.0.1:8888")
```

<details>
<summary>Response from Schiene Layer</summary>

```python
[{'arrival': '15:47',
  'canceled': False,
  'departure': '14:30',
  'details': '',
  'price': 55.0,
  'products': ['ICE'],
  'time': '01:16',
  'transfers': 0,
  'ontime': True,
  'delay': None},
 {'arrival': '16:21',
  'canceled': False,
  'departure': '14:38',
  'details': '',
  'price': 50.99,
  'products': ['SBAHN', 'ICE'],
  'time': '01:42',
  'transfers': 1,
  'ontime': True,
  'delay': None},
 {'arrival': '16:25',
  'canceled': False,
  'departure': '14:46',
  'details': '',
  'price': 50.99,
  'products': ['ICE', 'REGIONAL'],
  'time': '01:23',
  'transfers': 1,
  'ontime': True,
  'delay': None},
 {'arrival': '16:45',
  'canceled': False,
  'departure': '15:31',
  'details': '',
  'price': 55.0,
  'products': ['ICE'],
  'time': '01:14',
  'transfers': 0,
  'ontime': True,
  'delay': None},
 {'arrival': '17:27',
  'canceled': False,
  'departure': '15:34',
  'details': '',
  'price': 55.0,
  'products': ['ICE', 'REGIONAL'],
  'time': '01:53',
  'transfers': 1,
  'ontime': True,
  'delay': None},
 {'arrival': '17:15',
  'canceled': False,
  'departure': '15:35',
  'details': '',
  'price': 21.8,
  'products': ['REGIONAL', 'REGIONAL'],
  'time': '01:40',
  'transfers': 1,
  'ontime': True,
  'delay': None},
 {'arrival': '17:44',
  'canceled': False,
  'departure': '15:35',
  'details': '',
  'price': 21.8,
  'products': ['REGIONAL', 'REGIONAL'],
  'time': '02:09',
  'transfers': 1,
  'ontime': True,
  'delay': None},
 {'arrival': '17:33',
  'canceled': False,
  'departure': '15:36',
  'details': '',
  'price': 24.99,
  'products': ['SBAHN', 'ICE'],
  'time': '02:06',
  'transfers': 1,
  'ontime': False,
  'delay': {'delay_departure': 0, 'delay_arrival': 9}},
 {'arrival': '18:20',
  'canceled': False,
  'departure': '16:38',
  'details': '',
  'price': 47.99,
  'products': ['SBAHN', 'ICE'],
  'time': '01:42',
  'transfers': 1,
  'ontime': True,
  'delay': None},
 {'arrival': '18:24',
  'canceled': False,
  'departure': '16:46',
  'details': '',
  'price': 50.99,
  'products': ['ICE', 'REGIONAL'],
  'time': '01:38',
  'transfers': 1,
  'ontime': True,
  'delay': None}]
```

</details>
