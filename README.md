# satnogs-network-observation-api

Python client wrapper for the [SatNOGS Network](https://network.satnogs.org) Observation API.

Provides typed access to satellite observations, ground stations, and transmitters with lazy cursor-based pagination.

Source API: [SatNOGS Network GitLab](https://gitlab.com/librespacefoundation/satnogs/satnogs-network)

## Installation

### From wheel (recommended)

```bash
pip install dist/satnogs_network_api-0.1.0-py3-none-any.whl
```

### From source

```bash
pip install .
```

### Using Make

```bash
make venv          # Create .venv, install deps
make wheel         # Build a wheel (creates venv if needed)
make test          # Run unit tests
make clean         # Remove build artifacts
```

### For development

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from satnogs_network_api import SatnogsNetworkClient

client = SatnogsNetworkClient()

for obs in client.observations.list(status="good", norad_cat_id=25544):
    print(obs.id, obs.transmitter_mode, obs.center_frequency)
```

## API Reference

See [API.md](API.md) for complete documentation of all wrapper functions with usage examples.

## License

AGPL-3.0
