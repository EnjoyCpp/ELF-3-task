# ND3 AI Image Processing Project

This project allows users to upload image data and get processed results using an AI model running on a virtual server.

## Project Structure

```
project/
├── backend/              # Flask API with AI model
│   ├── app.py            # Main Flask application
│   ├── model.h5          # AI model file
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Backend Docker configuration
│   ├── uploads/          # Temporary storage for uploaded images
│   └── processed/        # Storage for processed images
├── frontend/             # Vue.js frontend
│   ├── src/              # Source code
│   ├── public/           # Static assets
│   ├── package.json      # NPM dependencies
│   └── Dockerfile        # Frontend Docker configuration
└── docker-compose.yml    # Docker Compose configuration
```

## Requirements

- Docker and Docker Compose
- Alternatively: Node.js 16+ and Python 3.9

## Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/nd3-project.git
   cd nd3-project
   ```

2. Start the application:
   ```bash
   docker-compose up
   ```

3. Access the web interface at http://localhost:8080

## Manual Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Using the Application

1. Access the web interface at http://localhost:8080
2. Upload an image using the upload button
3. The AI model will process the image and display the results
4. You can view the processed image with annotations and the detailed analysis

## AI Model Details

This application uses the same AI model that was developed for ND1/ND2 tasks. The model has been exported as a .h5 file and is loaded by the Flask backend API.

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /upload` - Upload an image for processing. Returns JSON with processed image and analysis results.

## Development with Nix (Optional)

For reproducible development environments, you can use Nix:

1. Install Nix:
   ```bash
   sh <(curl -L https://nixos.org/nix/install) --daemon
   ```

2. Enable Flakes (if not already enabled):
   Add to your `~/.config/nix/nix.conf` or `/etc/nix/nix.conf`:
   ```
   experimental-features = nix-command flakes
   ```

3. Enter the development environment:
   ```bash
   nix develop
   ```