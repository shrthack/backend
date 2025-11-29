# Shorthack Backend
 
Some docs for dev and deploy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shrthack/backend.git
   cd backend
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage

1. Start the database:
   ```bash
   docker-compose up -d postgres
   ```

2. Run database migrations:
   ```bash
   docker-compose up migrations
   ```

3. Run the application:
   ```bash
   poetry run python src/main.py
   ```

The API will be available at `http://localhost:8000`.

## Development

### Prerequisites

- Python 3.13+
- Poetry
- Docker and Docker Compose
- sqlc (for code generation from SQL)

### Setup Development Environment

1. Follow the installation steps above.

2. Install sqlc (if generating code from SQL queries):
   - Download from [sqlc.dev](https://sqlc.dev/)
   - Or use Docker: `docker run --rm -v $(pwd):/src -w /src kjconroy/sqlc generate`

3. Generate database code (if needed):
   ```bash
   sqlc generate
   ```
