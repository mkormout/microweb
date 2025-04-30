# Microweb

A minimalistic web framework for **MicroPython**, inspired by Node.js Express and focused on simplicity and small size.

## Features

- Basic request routing similar to Express.js
- Middleware support
- Lightweight core for handling HTTP requests and responses
- Clear modular structure: `core`, `lib`, `middleware`

## Installation

Clone the repository and copy the needed files into your MicroPython project:

```bash
git clone https://github.com/mkormout/microweb.git
```

> Note: Microweb is intended for MicroPython environments, e.g., ESP32 or Raspberry Pi Pico W.

## Example Usage

```python
from microweb.core.app import App

app = App()

# Example middleware (synchronous for MicroPython compatibility)
def logger_middleware(req, res, next_func):
    print(f"{req.method} {req.path}")
    next_func()

app.use(logger_middleware)

# Route handlers
def home(req, res):
    res.text('Hello, World!')

def submit(req, res):
    res.json({'message': 'Data received'})

# Register routes
app.route('/', 'GET', home)
app.route('/submit', 'POST', submit)

# Run server
app.listen('0.0.0.0', 80)
```

## Project Structure

```
microweb/
│
├── core/         # Core framework components (App, Request, Response)
├── lib/          # Helper utilities
├── middleware/   # Middleware support
└── __init__.py   # Package initialization
```

## Requirements

- MicroPython (tested on ESP32)

## Project Status

This project is under active development and not yet production-ready.

## License

MIT License.
