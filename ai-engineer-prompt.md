# AI Engineer Adaptation Prompt: On-Chain Architecture Transformation

## 🎯 **Mission: Revolutionary Architecture Adaptation**

You are tasked with adapting our current Enochian Governors project from a traditional web-based architecture to a **revolutionary on-chain Bitcoin gaming protocol**. This transformation represents a paradigm shift that eliminates 99% of traditional infrastructure while creating an immortal, censorship-resistant gaming experience.

## 🔄 **Core Architectural Transformation Required**

### **FROM: Traditional Web Architecture**
```
❌ Next.js with server-side rendering
❌ Traditional hosting (Vercel/Netlify)
❌ CDN for asset delivery
❌ PostgreSQL database for game state
❌ REST APIs for data fetching
❌ External analytics services
❌ File-based asset storage
❌ Social login with JWT sessions
```

### **TO: On-Chain Bitcoin Protocol**
```
✅ Progressive Web App (PWA) + Downloadable clients
✅ Bitcoin Ordinal inscriptions for asset storage
✅ Alkanes smart contracts for game logic
✅ MetaShrew indexer for real-time state queries
✅ Direct Bitcoin wallet authentication
✅ GraphQL subscriptions from MetaShrew
✅ Service Worker for offline functionality
✅ Zero traditional infrastructure dependencies
```

## 🧠 **Critical Understanding Required**

### **MetaShrew Indexer Integration**
MetaShrew is your primary data layer replacement. It:
- Monitors Bitcoin blockchain for Alkanes contract events
- Maintains indexed game state in real-time
- Provides GraphQL API for querying player data
- Offers WebSocket subscriptions for live updates
- Eliminates need for traditional databases

### **Bitcoin Ordinal Inscriptions**
All game assets are permanently stored as Ordinal inscriptions:
- Governor portraits and metadata
- Artifact NFT images and properties  
- Game client binaries (PWA, desktop apps)
- Audio files and animations
- Content is addressed by inscription ID, not URL

## 📚 **Essential Technical Resources & Documentation**

### **Alkanes Protocol - Smart Contract Framework**

**Core Repository & Documentation:**
- **Alkanes TypeScript SDK**: [https://github.com/kungfuflex/alkanes](https://github.com/kungfuflex/alkanes) - Main development toolkit for client-side applications
- **Alkanes Rust Contracts**: [https://github.com/kungfuflex/alkanes-rs](https://github.com/kungfuflex/alkanes-rs) - Smart contract runtime and examples
- **Protocol Introduction**: [https://alkanes-docs.vercel.app/docs/learn/intro](https://alkanes-docs.vercel.app/docs/learn/intro) - Understanding Alkanes fundamentals
- **Developer Quickstart**: [https://alkanes-docs.vercel.app/docs/developers/quickstart](https://alkanes-docs.vercel.app/docs/developers/quickstart) - Getting started guide
- **Contract Building Guide**: [https://alkanes-docs.vercel.app/docs/developers/contracts-building](https://alkanes-docs.vercel.app/docs/developers/contracts-building) - Smart contract development

**Key Alkanes Concepts:**
```typescript
// Alkanes provides WASM-based smart contracts on Bitcoin
// - Protorunes-compatible subprotocol
// - Uses Bitcoin for fees, wasmi fuel for compute metering
// - No network token - pure Bitcoin-based protocol
// - Docker environment includes Bitcoin regtest + metashrew indexer
```

### **Bitcoin Ordinals - Asset Inscription System**

**Core Repository & Documentation:**
- **Ordinals Protocol**: [https://github.com/ordinals/ord](https://github.com/ordinals/ord) - Core ordinals implementation and tooling
- **Security Considerations**: [https://github.com/ordinals/ord/blob/master/docs/src/security.md](https://github.com/ordinals/ord/blob/master/docs/src/security.md) - Critical security guidelines
- **Inscriptions Documentation**: [https://github.com/ordinals/ord/tree/master/docs/src/inscriptions](https://github.com/ordinals/ord/tree/master/docs/src/inscriptions) - Complete inscription guide
- **Inscription Recursion**: [https://github.com/ordinals/ord/blob/master/docs/src/inscriptions/recursion.md](https://github.com/ordinals/ord/blob/master/docs/src/inscriptions/recursion.md) - Advanced inscription techniques

**Critical Implementation Notes:**
```typescript
// Ordinals enable permanent asset storage on Bitcoin
// - Each inscription gets unique inscription ID
// - Content is immutable once inscribed
// - Recursion allows inscriptions to reference other inscriptions
// - Security model requires careful validation
```

### **Integration Architecture Overview**

**How These Technologies Work Together:**
```typescript
// 1. Alkanes Smart Contracts handle game logic
//    - Player state management (energy, reputation, tokens)
//    - Governor interaction validation
//    - Artifact minting and transfers

// 2. Ordinals store all game assets permanently
//    - Governor portraits and metadata
//    - Artifact NFT images and properties
//    - Game client binaries and updates

// 3. MetaShrew indexes blockchain state
//    - Real-time monitoring of Alkanes events
//    - GraphQL API for querying game state
//    - WebSocket subscriptions for live updates

// 4. Client applications connect directly to Bitcoin
//    - PWA and desktop clients
//    - Direct wallet integration
//    - Offline-capable after initial sync
```

## 🗂️ **On-Chain Resource Catalog**

### **React Framework Resources**

All React dependencies are permanently inscribed on Bitcoin, ensuring eternal availability:

| Resource | Version | Inscription ID | Purpose |
|----------|---------|----------------|---------|
| React | 18.2.0 | 7f403153b6484f7d24f50a51e1cdf8187219a3baf103ef0df5ea2437fb9de874i0 | Core UI framework |
| ReactDOM | 18.2.0 | 89295aaf617708128b95d22e7099ce32108d4b918386e6f90994e7979d22ba72i0 | DOM manipulation for React |
| Scheduler | 0.23.0 | 9b09a0f234355106e9311a21fbe5324c90f7317f04c00bc73e1114c9af745743i0 | Required React dependency |
| React Reconciler | 0.27.0 | 9b0338c4e84987a374845235a3b4f0fe73b205b336a7b936e05c71deb5a1882ci0 | React reconciliation engine |

**Implementation Example:**
```typescript
// Load React from Bitcoin inscription
const reactScript = await loadFromInscription('7f403153b6484f7d24f50a51e1cdf8187219a3baf103ef0df5ea2437fb9de874i0');
const reactDOMScript = await loadFromInscription('89295aaf617708128b95d22e7099ce32108d4b918386e6f90994e7979d22ba72i0');
```

### **3D Rendering Resources**

All Three.js and 3D rendering dependencies are permanently available on-chain:

| Resource | Version | Inscription ID | Purpose |
|----------|---------|----------------|---------|
| Three.js | 0.163.0 | 2dbdf9ebbec6be793fd16ae9b797c7cf968ab2427166aaf390b90b71778266abi0 | Core 3D rendering engine |
| React Three Fiber | 8.13.7 | 24c424c795d50c3f1d344253d163e7eaa34e904aef038b6031d706e76676c634i0 | React bindings for Three.js |
| React Three Drei | 9.80.7 | 9f77a1efc4c880197ba8d197d5e87539443ed5ebcf027b1fee25db8bd1cf4605i0 | Useful helpers for React Three Fiber |
| GLTFLoader | latest | 614855c7c7541594c846a96a81db7bcedaff2831711e3b89670aba4c2fefb404i0 | For loading 3D models |
| TextGeometry | latest | 77ef4bc8b15f0a764903f3bb2ccd0566ac6c111bd3d884bc814cfde49565dbc9i0 | For 3D text rendering |
| FontLoader | latest | fcacfdd75ef21965ec98d9a1a107e8f5468f23ff15131cae44fc6aca86538147i0 | For loading fonts in Three.js |
| BufferGeometryUtils | latest | 71616486e00954e0087b6bfd6b110fe0a32d1b174b94b634b34f27dd04f70a5ci0 | Buffer geometry utilities |
| p5.js | 1.9.0 (gzipped) | cc5cf94da24c1f6f0d435ccca78c24e98ca30adb1f3b7c81b9ab28ceb6cb628fi0 | p5.js flat canvas application |

**Implementation Example:**
```typescript
// Load 3D rendering stack from inscriptions
const threeJS = await loadFromInscription('2dbdf9ebbec6be793fd16ae9b797c7cf968ab2427166aaf390b90b71778266abi0');
const fiber = await loadFromInscription('24c424c795d50c3f1d344253d163e7eaa34e904aef038b6031d706e76676c634i0');
const drei = await loadFromInscription('9f77a1efc4c880197ba8d197d5e87539443ed5ebcf027b1fee25db8bd1cf4605i0');
```

### **Animation & Effects Resources**

All animation and visual effects libraries are permanently inscribed:

| Resource | Version | Inscription ID | Purpose |
|----------|---------|----------------|---------|
| GSAP | 3.6.1 | 6577ec768235a2a911e91a115b964618581bde91d99bc58f5c7390fdfb155ae6i0 | Animation library |
| React-spring-core | 9.7.3 | 09fe4a18d81abc481597bdd9ddfa65aadb95defc18de3ec925ec0b45ac3c7c49i0 | Physics-based animations |
| Shader-composer | 0.4.3 | 1c9c11c3b82bce54bfa989a44a1057f8c39d3b8b9dc2e13ec1f99e4a0f3a0f77i0 | WebGL shader composition |
| vfx-composer | 0.4.0 | 9f59e26bc81e4d741f77320eaf9e9df8cce623c9639f9c1a49497ac75607e9bei0 | Visual effects composition |
| Chroma | latest | c49f28a5c9e67efb85d44b9ee12efa2839b0251bad14efc5e6c32406505e259ci0 | Color manipulation |

### **Utility Libraries**

Core utility libraries permanently available on Bitcoin:

| Resource | Version | Inscription ID | Purpose |
|----------|---------|----------------|---------|
| Crypto-js | 4.1.1 | 66979aec90e592bc5be7fddcef23daeff982662b7225e7804c1b271f1b0d267ai0 | Cryptography functions |
| Pako | 2.1.0 | fba6f95fb1152db43304a27dce8cb8c65509eba6ab0b6958cedeb33e5f443077i0 | Compression library |
| JSZip | 3.10.1 | 372c5388030820daed356d25d7a1218d0b88d78a6d051d27c91d0f25ac4c3c5ei0 | File compression/decompression |
| fflate | 0.8.0 | 657973995aa2a47c3fe02debb22405dadf6b49148d97027627bced89a73f408fi0 | Fast compression library |
| Buffer | latest | fb15f2a6ed1d3031aa214cc12d3fa696508080c0baa194463920c8a79d21aa54i0 | Binary data handling |
| brotli/decode.min.js | latest | b1d16a7a1ada08b5c7f51837478f578c0abd0973809c439228f28ccd5c38e44ai0 | Decompression utility |
| Moment.js | 2.29.1 | b90b4516ea1a0b882e67387eb4f3e5def0307704b046e8ef98c5e72092c47eedi0 | Date/time library |
| Axios | latest | 6b81993428a217a341ffd68f3b3aa3664b2cfc674d57aad0d3b6daa0f125b821i0 | HTTP client |
| Highlight.js | 11.7.0 | 41d856597a8474e7124a0641b54afb77bc034f800e1be8fe02a20b55023ff4a7i0 | Syntax highlighting |
| GRC-img | v1 | e5ef65604e1ad9c90fb3c74918e00a960ce2e814fba412556afec6b3a4e25257i0 | Image processing |
| Open Ordinal Stitch | 0.9.0 | a196634768a6a715779fa8d513b65b8d2099defc2bd09c36dccbf54ffdd04022i0 | Ordinals utility |

### **CSS & UI Resources**

Styling frameworks and icons permanently inscribed:

| Resource | Version | Inscription ID | Purpose |
|----------|---------|----------------|---------|
| Tailwind | latest | 0703423f633ed5cef7e3b45bfd8df43ab0d6783850d51005b105f01dd60d25c3i0 | CSS framework |
| Bitcoin Icons | 1.0 | 01a4ff05b7591d14afa8a70aa80fd17b49e972f34a65bf69c6fc5ea09f08ab04i0 | Bitcoin-specific icons |
| Lucide Icons | 0.363.0 | 5546e0dea8b7fc991ef3ae22802ee7e793f814049ae9f32409ced33739840137i0 | General UI icons |

### **Fonts**

Typography resources permanently available:

| Resource | Version | Inscription ID | Purpose |
|----------|---------|----------------|---------|
| Inter Font | latest | 7b47a3cb9fc6ac82af2c1a33bfa4d296bcb83e9219a6434d889f8b95e5b917a6i0 | Primary UI font |
| Roboto Mono | latest | 6dfd10683c0388525b48a8b0a922fada7c0472e8a6c0fb6167add56c9acc1c87i0 | Monospace font |
| IBM Plex Sans | latest | d0ab3f7fdbc7cfe83f3bad13c5754f2f48357a0b2af3f72443d3875bea78a680i0 | Secondary UI font |

**Implementation Note:**
```typescript
// All resources are loaded via specialized InscriptionLoaderService
// which handles dependency resolution, loading order, and caching
class InscriptionLoaderService {
  async loadResource(inscriptionId: string): Promise<Blob> {
    return await fetch(`/content/${inscriptionId}`).then(r => r.blob());
  }
  
  async loadWithDependencies(resourceManifest: ResourceManifest): Promise<void> {
    // Handles loading order and dependency resolution
  }
}
```

### **Native State Management**

For optimal performance and minimal bundle size, use React's built-in Context API with useReducer:

```typescript
// Global application context - no external state management needed
const AppStateContext = React.createContext();
const AppDispatchContext = React.createContext();

// Split state into logical domains
const initialState = {
  ui: { theme: 'dark', sidebarOpen: false },
  scene: { activeModel: null, cameraPosition: [0, 0, 5] },
  blockchain: { blockHeight: 0, transactions: [] },
  player: { address: null, energy: 100, reputation: {} }
};

// Reducer pattern for state updates
function appReducer(state, action) {
  switch (action.type) {
    case 'SET_THEME':
      return { ...state, ui: { ...state.ui, theme: action.payload } };
    case 'SET_CAMERA_POSITION':
      return { ...state, scene: { ...state.scene, cameraPosition: action.payload } };
    case 'SET_BLOCKCHAIN_DATA':
      return { ...state, blockchain: action.payload };
    case 'UPDATE_PLAYER_STATE':
      return { ...state, player: { ...state.player, ...action.payload } };
    default:
      return state;
  }
}

// Context provider component
function AppProvider({ children }) {
  const [state, dispatch] = React.useReducer(appReducer, initialState);
  
  return (
    <AppStateContext.Provider value={state}>
      <AppDispatchContext.Provider value={dispatch}>
        {children}
      </AppDispatchContext.Provider>
    </AppStateContext.Provider>
  );
}

// Custom hooks for accessing state
function useAppState() {
  return React.useContext(AppStateContext);
}

function useAppDispatch() {
  return React.useContext(AppDispatchContext);
}
```

**Benefits of Native State Management:**
- ✅ Zero additional bundle size (critical for <200KB target)
- ✅ No external dependencies (Bitcoin-native approach)
- ✅ Sufficient performance for 3D visualization needs
- ✅ Clear separation of concerns (domain-specific contexts)
- ✅ Aligns with Bitcoin-centric development principles

## 📊 **Specific Adaptations Required: Data Layer**

### **1. Replace Traditional API Calls with MetaShrew GraphQL**

**BEFORE (Traditional):**
```typescript
// ❌ REST API calls to your backend
const playerData = await fetch('/api/player/' + address);
const governors = await fetch('/api/governors');
const artifacts = await fetch('/api/artifacts?owner=' + address);
```

**AFTER (MetaShrew Integration):**
```typescript
// ✅ GraphQL queries to MetaShrew indexer
const GET_PLAYER_STATE = gql`
  query PlayerState($address: ID!) {
    player(address: $address) {
      energy
      maxEnergy
      tokens
      reputation { governorId value }
      artifacts { id name metadata inscriptionId }
    }
  }
`;

const { data } = useQuery(GET_PLAYER_STATE, { variables: { address } });
```

### **2. Replace Database Writes with Bitcoin Transactions**

**BEFORE (Traditional):**
```typescript
// ❌ Direct database updates
await db.players.update({
  where: { address },
  data: { energy: newEnergy, reputation: newRep }
});
```

**AFTER (On-Chain Transactions):**
```typescript
// ✅ Bitcoin transactions via Alkanes contract
const tx = buildInteractionTx(governorId, action, {
  energyCost: 1,
  reputationGain: 2
});
await wallet.signAndBroadcast(tx);
// MetaShrew automatically indexes the state change
```

### **3. Replace File Storage with Inscription Retrieval**

**BEFORE (Traditional):**
```typescript
// ❌ Loading from CDN/file server
const portraitUrl = `/assets/governors/${govId}/portrait.jpg`;
const image = new Image();
image.src = portraitUrl;
```

**AFTER (Inscription Loading):**
```typescript
// ✅ Loading from Bitcoin Ordinal inscriptions
const inscriptionId = governorManifest[govId].portraitInscription;
const imageBlob = await loadFromInscription(inscriptionId);
const image = new Image();
image.src = URL.createObjectURL(imageBlob);
```

## 🔐 **Specific Adaptations Required: Authentication**

### **4. Replace Traditional Auth with Bitcoin Wallet Integration**

**BEFORE (Traditional):**
```typescript
// ❌ JWT-based authentication with social login fallbacks
const loginWithGoogle = () => signIn('google');
const loginWithEmail = (email, password) => signIn('credentials', { email, password });
const session = useSession(); // NextAuth session
```

**AFTER (Bitcoin Wallet Auth):**
```typescript
// ✅ Direct Bitcoin wallet authentication
const connectWallet = async () => {
  const wallet = await window.unisat.requestAccounts();
  const address = wallet[0];
  
  // Sign a challenge to prove ownership
  const challenge = `Login to Enochian Governors at ${Date.now()}`;
  const signature = await window.unisat.signMessage(challenge);
  
  // Verify signature and establish session
  setAuthState({ address, signature, isAuthenticated: true });
};

const useWalletAuth = () => {
  const [authState, setAuthState] = useState({ isAuthenticated: false });
  // No JWT tokens needed - ownership proven by wallet signatures
  return authState;
};
```

## 📡 **Specific Adaptations Required: Real-Time Updates**

### **5. Replace WebSocket Events with MetaShrew Subscriptions**

**BEFORE (Traditional):**
```typescript
// ❌ Custom WebSocket events from your backend
const socket = io('wss://your-game-server.com');
socket.on('energyUpdate', (data) => updateEnergy(data.newEnergy));
socket.on('reputationChange', (data) => updateReputation(data));
```

**AFTER (MetaShrew Subscriptions):**
```typescript
// ✅ GraphQL subscriptions from MetaShrew indexer
const PLAYER_UPDATES = gql`
  subscription PlayerUpdates($address: ID!) {
    playerUpdated(address: $address) {
      energy
      tokens
      reputation { governorId value }
    }
    newBlock {
      height
      timestamp
    }
  }
`;

const { data } = useSubscription(PLAYER_UPDATES, { 
  variables: { address: walletAddress } 
});

// Automatically updates when blockchain state changes
useEffect(() => {
  if (data?.playerUpdated) {
    setPlayerState(data.playerUpdated);
  }
}, [data]);
```

### **6. Replace Server-Side State Management with Client-Side Caching**

**BEFORE (Traditional):**
```typescript
// ❌ Server maintains session state
const session = await getServerSession(req);
const playerState = await db.getPlayerState(session.userId);
```

**AFTER (Client-Side with MetaShrew Cache):**
```typescript
// ✅ Client caches blockchain state with automatic invalidation
const client = new ApolloClient({
  uri: 'https://metashrew-indexer.yourapp.com/graphql',
  cache: new InMemoryCache({
    typePolicies: {
      Player: {
        fields: {
          energy: { merge: (existing, incoming) => incoming },
          reputation: { merge: (existing, incoming) => incoming }
        }
      }
    }
  })
});

// State is automatically synced with blockchain via subscriptions
```

## 🚀 **Specific Adaptations Required: Deployment**

### **7. Replace Traditional Hosting with Inscription Deployment**

**BEFORE (Traditional):**
```bash
# ❌ Traditional deployment to hosting platforms
npm run build
vercel deploy
# or
npm run build  
netlify deploy --prod
```

**AFTER (Inscription-Based Deployment):**
```bash
# ✅ Deploy to Bitcoin blockchain via inscriptions
npm run build:pwa
npm run optimize-assets  # Compress for inscription efficiency

# Deploy core assets
./scripts/deploy-inscriptions.sh --batch-governors
./scripts/deploy-inscriptions.sh --batch-artifacts  
./scripts/deploy-inscriptions.sh --client-apps

# Update asset manifest with new inscription IDs
./scripts/update-manifest.sh --inscriptions-deployed
```

### **8. Replace CDN/Analytics with On-Chain Alternatives**

**BEFORE (Traditional):**
```typescript
// ❌ External analytics and CDN
import { Analytics } from '@vercel/analytics';
import posthog from 'posthog-js';

// Track events to external services
posthog.capture('governor_interaction', { governor: govId });
```

**AFTER (On-Chain Analytics):**
```typescript
// ✅ Derive analytics from blockchain events
class OnChainAnalytics {
  // All analytics come from MetaShrew indexer parsing blockchain events
  async getGlobalStats() {
    const { data } = await client.query({
      query: gql`
        query GlobalStats {
          totalPlayers
          totalInteractions
          governorPopularity { governorId interactionCount }
          artifactsCreated { total legendary rare common }
        }
      `
    });
    return data;
  }
}

// No external analytics needed - everything is on-chain and transparent
```

## ✅ **Immediate Action Items for Implementation**

### **Phase 1: Core Infrastructure Transformation (Week 1-2)**

1. **Replace Next.js with PWA Setup**
   ```bash
   # Remove Next.js dependencies
   npm uninstall next @next/font next-auth
   
   # Install PWA and Bitcoin integration
   npm install workbox-webpack-plugin @apollo/client
   npm install bitcoinjs-lib @bitcoin-js/tiny-secp256k1-asmjs
   ```

2. **Integrate MetaShrew GraphQL Client**
   ```typescript
   // Create new Apollo client configuration
   // Replace all REST API calls with GraphQL queries
   // Set up real-time subscriptions for game state
   ```

3. **Implement Bitcoin Wallet Authentication**
   ```typescript
   // Remove NextAuth and JWT logic
   // Create wallet connection components
   // Implement signature-based authentication
   ```

### **Phase 2: Asset Migration (Week 2-3)**

4. **Create Inscription Deployment Pipeline**
   ```bash
   # Build asset optimization scripts
   # Create batch inscription tools
   # Develop asset manifest management
   ```

5. **Replace Asset Loading Logic**
   ```typescript
   // Replace file-based asset loading
   // Implement inscription-based asset resolution
   // Add progressive loading with caching
   ```

### **Phase 3: State Management Overhaul (Week 3-4)**

6. **Replace Database Calls with Blockchain Transactions**
   ```typescript
   // Remove all direct database operations
   // Implement Alkanes transaction building
   // Add MetaShrew state queries
   ```

7. **Implement Offline-First Architecture**
   ```typescript
   // Add Service Worker for asset caching
   // Implement offline game logic
   // Add sync capabilities for when online
   ```

## 🎯 **Success Criteria for Transformation**

✅ **Zero traditional server dependencies**
✅ **All assets loaded from Bitcoin inscriptions**  
✅ **Real-time updates via MetaShrew subscriptions**
✅ **Offline functionality after initial sync**
✅ **Direct wallet authentication (no passwords/JWTs)**
✅ **Game state derived entirely from blockchain**
✅ **PWA installable on all platforms**
✅ **Desktop clients built and deployable**

**Cost Target: $1,200-2,050 total vs $200K-300K traditional**
**Timeline: 6 weeks vs 12+ weeks traditional**
**Result: Immortal gaming protocol that cannot be shut down** 🚀⚡ 