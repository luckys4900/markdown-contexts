# Multi-Agent Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Master Agent (GPT-4)                        │
│  - Task orchestration                                            │
│  - Result integration                                            │
│  - User interaction                                              │
│  - Token usage: MINIMAL                                          │
└───────────┬─────────────────────────────────────────────────────┘
            │
            ├──────────────┬──────────────┬──────────────┬──────────────┐
            │              │              │              │              │
            ▼              ▼              ▼              ▼              ▼
    ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
    │ Collector │  │ Organizer │  │ Analyzer  │  │ Reporter  │  │   Scheduler│
    │  Agent    │  │  Agent    │  │  Agent    │  │  Agent    │  │   Agent   │
    │ (Free)    │  │ (Free)    │  │ (Free)    │  │ (Free)    │  │  (Free)   │
    └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
          │             │             │             │             │
          ▼             ▼             ▼             ▼             ▼
    ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
    │   inbox/  │  │   analysis/│  │  strategy/│  │  memory/  │  │  reports/ │
    │   scan    │  │  classify  │  │   analyze │  │  compare  │  │  generate │
    └───────────┘  └───────────┘  └───────────┘  └───────────┘  └───────────┘
```

## Processing Flow

```
User Input
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Collection (Parallel)                              │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│ │ File 1   │  │ File 2   │  │ File 3   │  │ File N   │    │
│ │ Collect  │  │ Collect  │  │ Collect  │  │ Collect  │    │
│ └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Organization (Parallel)                            │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│ │ YAML 1   │  │ YAML 2   │  │ YAML 3   │  │ YAML N   │    │
│ │ Add      │  │ Add      │  │ Add      │  │ Add      │    │
│ │ Classify │  │ Classify │  │ Classify │  │ Classify │    │
│ └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: Analysis (Parallel)                                │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│ │ Similar  │  │ Duplicate │  │ Content  │  │ Meta     │    │
│ │ Check    │  │ Check    │  │ Analysis │  │ Extract  │    │
│ └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 4: Reporting (Sequential)                             │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│ │ Report   │  │ Git Add  │  │ Git Push │                    │
│ │ Generate │  │ Commit   │  │          │                    │
│ └──────────┘  └──────────┘  └──────────┘                    │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
Result Summary → Master Agent → User
```

## Token Usage Optimization

```
┌─────────────────────────────────────────────────────────────────┐
│ Traditional Approach (Single Agent)                            │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ All files → Master Agent → Process → Result            │    │
│ │ Token: 100% (All content processed by expensive model) │    │
│ └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Multi-Agent Approach                                           │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Master: 10% (Orchestration only)                       │    │
│ │ Slaves: 90% (Content processing by free models)        │    │
│ │ Cost: ~90% reduction                                   │    │
│ └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Performance Comparison

| Metric | Single Agent | Multi-Agent | Improvement |
|--------|-------------|-------------|-------------|
| Processing Time | 100s | 25s | 4x faster |
| Token Usage (Master) | 100% | 10% | 90% reduction |
| Total Cost | $X | $0.1X | 90% cheaper |
| Scalability | Limited | High | Linear |

## Implementation Priority

1. **Week 1**: Basic multi-agent structure
   - Master-Slave communication
   - Task queue system

2. **Week 2**: Parallel processing
   - File collection parallelization
   - YAML addition parallelization

3. **Week 3**: Advanced features
   - Similarity detection
   - Duplicate elimination

4. **Week 4**: Optimization
   - Token monitoring
   - Performance tuning
