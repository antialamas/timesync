# System Architecture

This document was created by an AI.
Original prompt: Modify the system architecture to separate the Quantum Channel Simulator Core into two distinct modules
#AI_generated

Sources:
- src/main.py
- src/app.py
- src/parameter_server.py
- src/config/parameter_handler.py
- src/simulation/quantum_channel.py

## System Block Diagram

```mermaid
graph TB
    subgraph "Web Interface"
        A[Parameter Server] -->|Serves| B[Web UI]
        C[Flask App] -->|API Endpoints| B
        B -->|Parameters| C
    end

    subgraph "Configuration Management"
        D[Config Manager] -->|Validates| E[Parameter Specs]
        D -->|Loads/Saves| F[YAML Config Files]
    end

    subgraph "Quantum States Generator Core"
        G[State Generator] -->|States| H[Channel Effects]
        H -->|Detections| I[Detection Handler]
    end

    subgraph "Synchronization Simulator Core"
        N[Data Preprocessor] -->|Processed Data| O[Correlation Engine]
        O -->|Sync Results| P[Statistics Calculator]
    end

    subgraph "Visualization"
        K[Plot Generator] -->|Renders| L[Correlation Plots]
        K -->|Renders| M[Count Distribution]
    end

    C -->|Config| D
    D -->|Validated Config| G
    I -->|Detection Data| N
    P -->|Results| C
    P -->|Data| K

    classDef webComponent fill:#f9f,stroke:#333,stroke-width:2px
    classDef configComponent fill:#bbf,stroke:#333,stroke-width:2px
    classDef quantumComponent fill:#bfb,stroke:#333,stroke-width:2px
    classDef syncComponent fill:#fbf,stroke:#333,stroke-width:2px
    classDef vizComponent fill:#ffb,stroke:#333,stroke-width:2px

    class A,B,C webComponent
    class D,E,F configComponent
    class G,H,I quantumComponent
    class N,O,P syncComponent
    class K,L,M vizComponent
```

## Component Description

### 1. Web Interface Layer
- [`parameter_server.py`](../src/parameter_server.py) serves the parameter input interface
- [`app.py`](../src/app.py) provides REST API endpoints for simulation control
- Web UI allows parameter input and visualization of results

### 2. Configuration Management Layer
- [`parameter_handler.py`](../src/config/parameter_handler.py) handles parameter validation and configuration
- Manages parameter specifications and constraints
- Handles YAML config file operations

### 3. Quantum States Generator Core
- Components:
  - State Generator: Creates signal and decoy states with specified properties
  - Channel Effects: Applies loss, delay, and noise to quantum states
  - Detection Handler: Simulates Bob's detection system and records events
- Responsibilities:
  - Generation of quantum states with configurable properties
  - Simulation of channel effects and losses
  - Detection event recording and timestamping
  - Output format: Structured detection events data

### 4. Synchronization Simulator Core
- Components:
  - Data Preprocessor: Prepares detection data for correlation analysis
  - Correlation Engine: Performs timing synchronization algorithms
  - Statistics Calculator: Computes QBER and other metrics
- Responsibilities:
  - Processing of raw detection events
  - Time correlation analysis
  - Synchronization optimization
  - Statistical analysis and metrics calculation

### 5. Visualization Layer
- [`generate_plots.py`](../src/generate_plots.py) handles data visualization
- Produces correlation plots and count distributions
- Supports both interactive display and file output

## Development Plans

### Phase 1: Basic Interface Development
- Create parameter definition file (parameters.yaml)
  - Define all input parameters with metadata
  - Group parameters by category
  - Include validation rules and constraints
- Create parameter file parser
  - YAML parsing functionality
  - Parameter validation system
  - Default value handling
- Implement interface generator
  - Template-based HTML generation
  - Form generation from parameter definitions
  - Basic styling and layout
- Set up basic Python project structure
- Create minimal backend API endpoints

### Phase 2: Core Modules Setup
- Implement Quantum States Generator Core
  - State property calculator
  - Timing sequence generator
  - Pulse shape modulator
  - Channel effects simulator
  - Detection event handler
- Implement Synchronization Simulator Core
  - Data preprocessor
  - Correlation engine
  - Statistics calculator

### Phase 3: Module Testing
- Develop mock data generators
- Create unit tests for each module
- Implement integration tests between modules
- Set up automated testing pipeline

### Phase 4: Integration
- Connect Quantum States Generator to Synchronization Simulator
- Implement basic visualization system
- Connect web interface to backend
- End-to-end testing

### Phase 5: Optimization
- Profile and optimize simulation modules
- Implement caching system
- Add parallel processing capabilities

### Phase 6: Interface Refinement
- Enhance parameter input validation
- Add advanced visualization features
- Implement real-time parameter updates
- Add interactive data exploration tools
- Optimize UI/UX based on user feedback

## Testing Strategy

### Module Independence Testing
1. State Generator Testing
   - Use predefined state configurations
   - Verify state properties
   - Test with boundary conditions

2. Channel Effects Testing
   - Use mock quantum states
   - Validate channel transformations
   - Test extreme parameter cases

3. Detection Handler Testing
   - Use simulated channel output
   - Verify detection statistics
   - Test timestamp generation

4. Data Preprocessor Testing
   - Use mock detection data
   - Validate preprocessing steps
   - Test data format conversions

5. Correlation Engine Testing
   - Use synthetic data sets
   - Verify correlation algorithms
   - Test synchronization accuracy

6. Statistics Calculator Testing
   - Use known result sets
   - Validate statistical calculations
   - Test error handling

### Integration Testing
1. Generator-Channel Integration
   - Test state propagation
   - Verify property preservation
   - Validate combined effects

2. Channel-Detection Integration
   - Test detection response
   - Verify timing accuracy
   - Validate event recording

3. Preprocessor-Correlation Integration
   - Test data flow
   - Verify correlation input/output
   - Validate processing chain

4. Full System Integration
   - End-to-end testing
   - Performance validation
   - System stability verification

## Data Flow
1. User inputs parameters through web interface
2. Parameters are validated by Config Manager
3. Quantum States Generator Core simulates quantum state transmission
4. Detection events are passed to Synchronization Simulator Core
5. Results are calculated and sent back to web interface
6. Visualization layer renders plots of results

The system uses a highly modular architecture that separates concerns between quantum state generation, synchronization analysis, and visualization. Each module can be developed and tested independently using mock data or simplified processes.