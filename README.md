# COMP7940 Project - CloudTrip AI Bot

## 1. Project Overview

**CloudTrip AI Bot** is a Telegram-based AI travel concierge designed to help users with travel planning and travel problem-solving through natural-language interaction.

The bot is powered by the **HKBU AI API**, logs interactions to **Azure Cosmos DB for MongoDB**, exposes a **FastAPI health endpoint** for monitoring, runs as a **Docker Compose multi-service application**, is deployed on **AWS EC2**, and supports **automatic redeployment through GitHub Actions**.

This project was developed by evolving the chatbot foundation from the labs into a more complete cloud system, with cloud hosting, data logging, monitoring, containerization, and CI/CD automation. The project directly aligns with the COMP7940 project requirement of building a cloud-deployed Telegram chatbot using an LLM API, a cloud database, Git, container technologies, and monitoring. 

---

## 2. Core Features

### Feature 1: Travel Itinerary Planning
Users can ask the chatbot to generate practical travel itineraries, destination suggestions, and travel preparation advice.

Example requests:
- `Plan a 3-day Tokyo trip for me`
- `Suggest a weekend itinerary in Sydney`
- `What should I pack for Bangkok in July?`

### Feature 2: Travel Problem-Solving Support
Users can ask about practical travel problems and receive simple action-oriented advice.

Example requests:
- `What should I do if my flight is delayed?`
- `It is raining in Tokyo. What indoor activities can I do?`
- `I lost my passport abroad. What should I do first?`

These two features are meaningful travel-concierge prototypes and fit the project guideline that suggests domains such as a travel concierge and 1–2 meaningful features. :contentReference[oaicite:1]{index=1}

---

## 3. System Architecture

The overall architecture is:

**Telegram User**  
→ **Telegram Bot Worker**  
→ **HKBU AI API**  
→ **Azure Cosmos DB for MongoDB**  
→ **FastAPI Health Service**  
→ **Docker Compose**  
→ **AWS EC2**  
→ **GitHub Actions CI/CD**

### Services
The project uses a two-service structure:

- **bot**: handles Telegram polling, user messages, AI requests, and cloud logging
- **api**: provides health and readiness endpoints for monitoring

This design supports better separation of concerns and reflects a small multi-service cloud architecture.

---

## 4. Tech Stack

### Application Layer
- Python 3.12
- python-telegram-bot
- FastAPI
- Requests

### AI Layer
- HKBU AI API

### Database Layer
- Azure Cosmos DB for MongoDB

### Deployment Layer
- Docker
- Docker Compose
- AWS EC2

### DevOps
- GitHub
- GitHub Actions

---

## 5. Project Structure

```text
comp7940-project/
├─ .github/
│  └─ workflows/
│     └─ deploy.yml
├─ app/
│  ├─ models/
│  │  └─ message_log.py
│  ├─ routes/
│  │  └─ health.py
│  ├─ services/
│  │  ├─ llm_service.py
│  │  └─ log_service.py
│  ├─ __init__.py
│  ├─ bot.py
│  ├─ config.py
│  ├─ db.py
│  └─ main.py
├─ docs/
├─ .dockerignore
├─ .gitignore
├─ docker-compose.yml
├─ Dockerfile
├─ README.md
├─ requirements.txt
└─ run_bot.py
```

---

## 6. How It Works
1.A user sends a message to the bot in Telegram.
2.The bot receives the message through Telegram polling.
3.The message is sent to the HKBU AI API using a travel-concierge system prompt.
4.The AI-generated response is returned to the user.
5.The request and response are logged to Azure Cosmos DB for MongoDB.
6.The system health can be checked through the FastAPI /health endpoint.
7.The application runs in Docker containers and is deployed on AWS EC2.
8.New code pushed to GitHub can trigger automatic redeployment through GitHub Actions.

This workflow closely matches the project’s suggested design pattern of Telegram + LLM + logging + CI/CD + monitoring.

---

## 7. Environment Variables

Create a .env file in the project root with the following fields:

`TELEGRAM_BOT_TOKEN=your_telegram_bot_token`

`HKBU_API_KEY=your_hkbu_api_key`


`HKBU_BASE_URL=your_hkbu_base_url`

`HKBU_MODEL=your_hkbu_model`

`HKBU_API_VER=your_hkbu_api_version`


`MONGODB_URI=your_azure_cosmos_mongodb_uri`

`MONGODB_DB_NAME=cloudcampus_ai`

`MONGODB_COLLECTION_NAME=message_logs`


`ADMIN_TELEGRAM_USER_ID=your_telegram_user_id`

`APP_ENV=production`

`PORT=8000`

Important:
Do not commit .env, .pem, or virtual environment folders to GitHub.

---

## 8. Local Development
Install dependencies

`python -m venv venv`

Windows:

venv\Scripts\activate

Then install packages:

`pip install -r requirements.txt`

Run FastAPI service

`uvicorn app.main:app --reload`

Run Telegram bot worker

`python run_bot.py`

Test health endpoint

Open:

`http://127.0.0.1:8000/health`

---

## 9. Docker Deployment
Build and run with Docker Compose

`docker compose up --build`

Or run in detached mode:

`docker compose up -d --build`

`Check running containers`

`docker compose ps`

View logs

`docker compose logs -f`

Or:

`docker compose logs -f api`

`docker compose logs -f bot`

-----

## 10. AWS EC2 Deployment

The project is deployed on AWS EC2 using Docker Compose.

Typical deployment steps

Launch and connect to an EC2 instance

Install Docker

Clone the GitHub repository

Create a .env file on EC2

Run:
`docker compose up -d --build`

`Check deployment status`

`docker compose ps`

`docker compose logs --tail=50 api`

`docker compose logs --tail=50 bot`

Health check

Open:

`http://<EC2-PUBLIC-DNS>:8000/health`

This extends the EC2 deployment logic from Lab 4 and the Docker containerization approach from Lab 6.

---

## 11. CI/CD with GitHub Actions

A GitHub Actions workflow is configured in:

`.github/workflows/deploy.yml`

Workflow behavior

- Whenever code is pushed to the main branch, GitHub Actions:

- Checks out the repository

- Loads the EC2 SSH private key from GitHub Secrets

- Connects to the EC2 instance

- Pulls the latest code

- Rebuilds Docker Compose services

- Restarts the application

This extends the CI/CD automation practice from Lab 5 into the final project.

Required GitHub Secrets

`EC2_HOST`

`EC2_USER`

`EC2_KEY`

---

## 12. Monitoring and Logging
Health Monitoring

The API service provides:

`/health`

`/ready`

These endpoints can be used to check whether the service is running correctly.

Container Monitoring

Operational status can be monitored through:

`docker compose ps`

`docker compose logs -f`

`Database Logging`

Each chatbot interaction is recorded in Azure Cosmos DB for MongoDB, including:

- Telegram user ID

- username

- user message

- bot reply

- response time

- status

- timestamp

This supports debugging, observability, and service traceability. The project brief specifically requires cloud database logging and monitoring.

---

## 13. Cost Awareness

The system was designed to be lightweight and cost-aware.

AWS

Cloud hosting cost was monitored through the AWS Billing dashboard.
At the time of reporting:

Month-to-date AWS cost: USD 5.98
Forecasted monthly AWS cost: USD 13.86
Azure

Azure Cosmos DB for MongoDB was monitored through Azure Cost Analysis.
At the time of reporting:

Azure Cosmos DB cost: less than USD 0.01

This lightweight architecture helps control unnecessary cloud spending while still fulfilling the technical requirements.

---

## 14. Challenges Encountered

During development and deployment, several practical issues were encountered and solved:

Telegram polling conflicts caused by multiple bot instances
Docker daemon and Compose plugin issues on EC2
Buildx / Docker Compose build compatibility problems
HKBU API timeout and parameter compatibility issues
Telegram reply length limits for long AI responses

Solving these issues improved the robustness of the system and strengthened the cloud engineering quality of the project.

---

## 15. Project Requirement Mapping

This project satisfies the main technical requirements as follows:

Telegram chatbot → implemented and tested successfully

Cloud database logging → Azure Cosmos DB for MongoDB

Cloud hosting → AWS EC2

LLM API → HKBU AI API

Git management → GitHub repository

Container technologies → Docker + Docker Compose

Monitoring → FastAPI health endpoint + Docker logs

Cost awareness → AWS Billing + Azure Cost Analysis

These requirements are explicitly stated in the COMP7940 project brief.

## 16. Screenshots

Add the following screenshots in the docs/ folder or directly in the report/slides:

- Telegram conversation

- /start and /help

- Travel itinerary response

- Travel problem-solving response

- Azure MongoDB logging record

- /health endpoint in browser

- docker compose ps on EC

- GitHub Actions successful deployment

- AWS cost screenshot

- Azure cost screenshot

---

## 17. Author Information

Student Name: CHEN Ka Shing
Student ID: 25456261
Bot Username: @Jerry2025_bot
Repository: https://github.com/dennyeer/comp7940-project