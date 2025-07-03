# Job Search Web Application

![ER Diagram](docs/ER%20Diagram.png)

A comprehensive job search platform built with microservices architecture.

## Architecture

- **API Gateway**: Routes requests to appropriate services
- **Job Posting Service**: Manages job postings and admin operations
- **Job Search Service**: Handles job search and filtering
- **Notification Service**: Manages job alerts and notifications
- **AI Agent Service**: Provides AI-powered job search assistance

## Services

### API Gateway (Port 8080)
- Routes requests to appropriate microservices
- Handles authentication and authorization
- Provides unified API interface

### Job Posting Service (Port 8000)
- CRUD operations for job postings
- Admin approval workflow
- Integration with notification system

### Job Search Service (Port 8001)
- Advanced job search with filters
- Search history tracking
- Redis caching for performance

### Notification Service (Port 8002)
- Job alert management
- Email notifications
- Background workers for processing

### AI Agent Service (Port 8003)
- AI-powered chat interface
- Natural language job search
- Command parsing and execution

## Technologies

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL, MongoDB
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **AI**: OpenAI GPT
- **Frontend**: React
- **Containerization**: Docker, Docker Compose

## Getting Started

1. Clone the repository
2. Install dependencies: `docker-compose up --build`
3. Access the application at `http://localhost:3000`

## API Documentation

- API Gateway: `http://api_gateway:8080/docs`
- Job Posting: `http://job_posting_service:8000/docs`
- Job Search: `http://job_search_service:8001/docs`
- Notification: `http://notification_service:8002/docs`
- AI Agent: `http://ai_agent:8003/docs`

## Development

Each service can be developed independently. See individual service READMEs for specific instructions.
