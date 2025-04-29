# Microweb

A minimalistic Python web framework inspired by Node.js Express, focused on simplicity and small size.

## Features

- Basic request routing
- Middleware support
- Core structure for handling requests and responses
- Organized into `core`, `lib`, and `middleware` modules

## Installation

Currently not published as a package. To use:
```bash
git clone https://github.com/mkormout/microweb.git
```
and import the necessary modules into your project.

## Example Usage

```python
from microweb.core.app import App

app = App()

# Example middleware
async def logger_middleware(req, res, next_func):
    print(f"{req.method} {req.path}")
    await next_func()

app.use(logger_middleware)

# Route handlers
def home(req, res):
    res.text('Hello, World!')

def submit(req, res):
    res.json({'message': 'Data received'})

# Register routes
app.route('/', 'GET', home)
app.route('/submit', 'POST', submit)

if __name__ == '__main__':
    app.listen('127.0.0.1', 8000)
```

## Project Structure

```
microweb/
│
├── core/         # Framework core (App, Request, Response)
├── lib/          # Helper libraries
├── middleware/   # Middleware support
└── __init__.py   # Initialization file
```

## Requirements

- Python 3.7+

## Project Status

This project is under active development and is not ready for production use.

## License

MIT License.
