# Bot Development Plan

## Overview

This document outlines the development approach for the Telegram bot that serves as the student-facing interface for the software engineering toolkit. The bot provides access to lab scores, course information, and intelligent assistance through natural language queries.

## Task 1: Project Scaffolding

Establish the foundational project structure with a clean separation of concerns. The bot entry point (`bot.py`) handles Telegram-specific logic and CLI test mode. Handlers reside in a dedicated directory, completely decoupled from the Telegram transport layer. This architecture enables offline testing via `--test` mode and simplifies unit testing. Configuration is loaded from environment variables via `config.py`, supporting both development (`.env.bot.example`) and production (`.env.bot.secret`) environments.

## Task 2: Backend Integration

Implement service layer components in `bot/services/` for communicating with the LMS backend API and LLM services. The `LmsClient` handles authenticated HTTP requests to fetch student scores, lab information, and course data. The `LlmClient` provides natural language understanding capabilities for intent recognition. Both clients implement retry logic and error handling for production resilience.

## Task 3: Intent Routing

Develop an intent classification system that maps user messages to appropriate handlers. Simple commands (`/start`, `/help`, `/health`) use direct routing. Natural language queries are processed through the LLM to determine intent, then routed to specialized handlers (scores lookup, lab info, FAQ). This hybrid approach balances performance for common commands with flexibility for open-ended queries.

## Task 4: Deployment

Containerize the bot using Docker Compose alongside the backend and frontend services. Configure health checks, logging, and graceful shutdown. Set up systemd service or supervisor for process management on the VM. Implement CI/CD pipeline for automated testing and deployment on merge to main branch.

## Testing Strategy

- Unit tests for handlers using pytest
- Integration tests with mocked API responses
- Manual verification via `--test` mode before each deployment
- End-to-end testing in Telegram after deployment
