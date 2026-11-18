\# Agentic AI Flight Search Workflow



```mermaid

flowchart TD

&#x20;   A\[User Natural-Language Request] --> B\[FastAPI Agent Endpoint]

&#x20;   B --> C\[AI Agent Controller]

&#x20;   C --> D\[Qwen3 LLM]

&#x20;   D --> E\[Select Appropriate Tool]

&#x20;   E --> F\[Python Tool Validation]

&#x20;   F --> G{Tool Permitted and Arguments Valid?}

&#x20;   G -->|No| H\[Return Safe Error]

&#x20;   G -->|Yes| I\[Execute Approved Flight Tool]

&#x20;   I --> J\[Existing Backend and MySQL]

&#x20;   J --> K\[Return Tool Results]

&#x20;   K --> D

&#x20;   D --> L\[Generate Natural-Language Response]

&#x20;   L --> M\[Display Flight Recommendations]

&#x20;   M --> N\[User Reviews Flight]

&#x20;   N --> O\[Existing Booking Workflow]

&#x20;   O --> P\[User Confirmation Before Booking]

