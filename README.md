
# Barcode API Server

A lightweight API server for scanning barcodes from images using DaisyKit. This service accepts an image URL and returns an array of detected barcode types and values.

## Features

Detects multiple types of barcodes (QR Code, Code 128, etc.).

Accepts remote image URLs for processing.- Built with Flask and DaisyKit for efficient barcode scanning.
- Dockerized for easy deployment.

---

## Installation

### Prerequisites

- Python 3.10 or later
- Docker and Docker Compose (optional, for containerized setup)

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/barcode-api.git
   cd barcode-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python app.py
   ```

4. The server will be available at `http://127.0.0.1:5005`.

---

## Using Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Start the service:
   ```bash
   docker-compose up
   ```

3. The server will be accessible at `http://localhost:5005`.

---

## API Documentation

### Endpoint

**POST** `/scan-barcode`

### Request Body

Send a JSON object with the following structure:

```json
{
  "imageUrl": "https://example.com/path/to/image.jpg"
}
```

### Response

Returns a JSON object containing an array of detected barcodes:

```json
{
  "barcodes": [
    {
      "type": "QR_CODE",
      "value": "1234567890"
    },
    {
      "type": "CODE_128",
      "value": "ABCDEFG123"
    }
  ]
}
```

### Error Handling

Possible error responses:
- `400 Bad Request`: Missing or invalid `imageUrl`.
- `500 Internal Server Error`: An unexpected error occurred.

---

## Directory Structure

```
barcode-api/
│
├── app.py               # Main API server script
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build file
├── docker-compose.yml   # Docker Compose configuration
└── README.md            # Project documentation
```

---

## Author

Created by [FunTuan](https://github.com/funtuan).
                    