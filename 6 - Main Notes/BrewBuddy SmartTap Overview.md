2026-01-19 14:20


Tags: [[TigerTribe]], [[HNK-SMARTAP-BREWBUDDY]]

# Overview Architecture

```mermaid
graph LR
    %% Entry Point
    Main[main.py] --> API[API: chat.py]
    
    API --> Workflow[BeerOrderingWorkflow]
    
    %% Workflow Steps
    Workflow --> Prepare[Prepare]
    Prepare --> Parallel{Parallel}
    Parallel -->|1| Compliance[Compliance Check]
    Parallel -->|2| Extract[Info Extraction]
    Compliance --> Decision[Decision]
    Extract --> Decision
    Decision --> Finalize[Finalize]
    
    %% Services
    Compliance --> CompSvc[Compliance Service]
    Extract --> ExtrSvc[Extraction Service]
    Decision --> StateSvc[State Service]
    
    %% Agents
    CompSvc --> Agent[Agent Service]
    ExtrSvc --> Agent
    StateSvc --> Agent
    
    %% Infrastructure
    Agent --> Redis[(Redis)]
    Agent --> Blob[(Azure Blob)]
    Agent --> Prompts[Prompts]
    
    %% Styling
    style Workflow fill:#e1f5fe
    style Agent fill:#fff3e0
    style Redis fill:#ffebee
    style Blob fill:#ffebee
```
 

# References
