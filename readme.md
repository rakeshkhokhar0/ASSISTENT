A small assistant for managing daily task 

## Description

A local, offline-first AI-powered task and study planning assistant built with Python.
The system manages daily sessions, task priorities, pauses, resumes, and completion tracking, with optional AI-assisted day planning using a locally hosted LLM via Ollama. Designed for learning-focused workflows, extensible architecture, and full user control over task execution.

## Project Overview

This project is designed as a personal productivity and study assistant that combines:
Deterministic task management logic
Session-based daily workflows
Controlled AI assistance for planning (not autonomous execution)
Offline operation using locally hosted language models
The system emphasizes user control, transparency, and extensibility.
## Features

1. Core Task Management

    Daily session (day) start and end
    Session-scoped task planning
    Task lifecycle management:
    Pending
    Active
    Paused (break or task switch)
    Completed
    Skipped
    Single active task enforcement
    Priority-based task ordering
    Task descriptions for better context

2. Task Control Commands

    Start tasks with priority awareness
    Pause tasks for breaks
    Resume paused tasks
    Switch between tasks safely
    Mark tasks as completed
    Skip tasks explicitly
    View current task status
    List tasks by:
        Today
        Specific date
        All sessions

3. AI-Assisted Planning (Optional)

    AI-generated daily study/task plans
    Uses a locally hosted LLM (via Ollama)
    Structured plan generation (name, priority, description)
    Priority normalization and validation
    User confirmation before saving plans
    Safe fallback if AI output is invalid

4. Offline-First Design

    No internet required for core features
    Local database storage
    Local LLM integration
    Full control over data and execution

5. Clean Architecture

Clear separation of concerns:
    taskmanager → command orchestration
    planner → AI planning logic
    model_interface → model integration
    database → persistence layer

Easy to extend or replace components
Model-agnostic design (Ollama now, cloud models later)

## Project Structure

    app.py                 # Application entry point
    taskmanager.py         # Command handling and orchestration
    planner.py             # AI-assisted day planning logic
    model_interface.py     # Local/remote model integration
    command.py             # Command parsing and definitions
    database.py            # Database helpers and queries
    database_connection.py # SQLite connection management
    help.py                # Only for testing purposes
    README.md

## Prerequisites

Python 3.9+
SQLite (built-in with Python)
Ollama (optional, for AI planning)
Install Ollama (optional)
https://ollama.com


Pull a model:

ollama pull phi3:mini

The application runs in interactive command mode.

## Example Workflow
day start
plan day
start <task name>
pause
continue
done
status
day end

AI planning always requires explicit user confirmation before tasks are saved.

## Design Principles

AI suggests, user decides
No silent state changes
No automatic task execution
Defensive validation of model output
Offline usability first
Simple, readable logic over automation

## Future Enhancements

User profile–aware planning
Carry-over logic for unfinished tasks
Progress analytics and summaries
Notifications and reminders
Optional cloud model support
UI or Telegram bot interface

## Installation

python app.py

## License

This project is intended for learning and personal use.
You may adapt or extend it as needed.



project is not completed yet
