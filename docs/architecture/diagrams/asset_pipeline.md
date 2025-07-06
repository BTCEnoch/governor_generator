# Asset Pipeline and Inscription Flow

This diagram illustrates how assets are processed from raw files through optimization, inscription, and P2P distribution.

```mermaid
graph TD
    subgraph Assets["Asset Pipeline"]
        Raw["Raw Assets<br/>.PSD, .AI files"]
        Proc["Processed Assets<br/>WebP, OGG"]
        Raw -->|"optimize-assets.sh"| Proc
    end

    subgraph Ordinals["Ordinal Assets"]
        Man["Manifests<br/>JSON indexes"]
        Temp["Templates<br/>Asset structures"]
        Insc["Inscriptions<br/>On-chain content"]
        Val["Validators<br/>Content checks"]
        
        Man --> Temp
        Temp -->|"inscribe-assets.sh"| Insc
        Insc -->|"verify"| Val
    end

    subgraph P2P["P2P Distribution"]
        Cache["Local Cache"]
        Index["Ordinal Indexer"]
        Sync["Sync Manager"]
        
        Index -->|"track"| Cache
        Sync -->|"update"| Cache
    end

    Proc -->|"prepare"| Man
    Insc -->|"distribute"| P2P
```

## Pipeline Components

### Asset Pipeline
- **Raw Assets**: Original source files (.PSD, .AI)
- **Processed Assets**: Optimized game-ready assets (WebP, OGG)

### Ordinal Assets
- **Manifests**: JSON indexes of assets
- **Templates**: Asset structure definitions
- **Inscriptions**: On-chain content storage
- **Validators**: Content verification tools

### P2P Distribution
- **Local Cache**: Client-side asset storage
- **Ordinal Indexer**: Tracks on-chain assets
- **Sync Manager**: Handles P2P synchronization 