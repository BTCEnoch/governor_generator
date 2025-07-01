# Enochian Governors - Full Stack Architecture Map

## 📁 Project Overview
```
enochian-governors/
├── README.md
├── package.json
├── .env.example
├── .gitignore
├── docker-compose.yml
└── docs/
    ├── api-documentation.md
    ├── game-mechanics.md
    └── deployment-guide.md
```

## 🏗️ Root Directory Structure
```
enochian-governors/
├── frontend/                     # Next.js React Application
├── backend/                      # Alkanes Contracts & Indexer
├── shared/                       # Shared Types & Utils
├── assets/                       # Game Assets & Media
├── docs/                        # Documentation
├── scripts/                     # Build & Deployment Scripts
├── tests/                       # Cross-platform Tests
└── infrastructure/              # DevOps & Deployment
```

## 🖥️ Frontend Structure (PWA - Progressive Web App) ⚠️ **MAJOR ARCHITECTURAL CHANGE**
```
frontend/
├── package.json                  # ⚠️ **CRITICAL**: Remove Next.js dependencies
├── ~~next.config.js~~            # ❌ **REMOVED** - No Next.js SSR
├── ~~tailwind.config.js~~        # ⚠️ **MODIFIED** - PWA-specific Tailwind config  
├── tsconfig.json
├── .env.local
├── public/
│   ├── favicon.ico
│   ├── manifest.json             # ⚠️ **NEW** - PWA manifest for installability
│   ├── sw.js                     # ⚠️ **NEW** - Service Worker for offline functionality
│   ├── robots.txt
│   └── images/
│       ├── logos/
│       ├── icons/
│       └── placeholders/
├── src/
│   ├── ~~app/~~                  # ❌ **REMOVED** - Next.js 14 App Router (no SSR)
│   │   ├── ~~layout.tsx~~        # ❌ **DEPRECATED** - No server-side layout
│   │   ├── ~~page.tsx~~          # ❌ **DEPRECATED** - No server-rendered pages
│   │   ├── ~~loading.tsx~~       # ❌ **DEPRECATED** - Client-side loading only
│   │   ├── ~~error.tsx~~         # ❌ **DEPRECATED** - Client-side error boundaries
│   │   ├── ~~not-found.tsx~~     # ❌ **DEPRECATED** - Client-side 404 handling
│   │   ├── ~~globals.css~~       # ❌ **MOVED** - To src/styles/globals.css
│   │   ├── app-shell/                # ⚠️ **NEW** - PWA App Shell Architecture
│   │   │   ├── App.tsx               # Main PWA entry point (replaces Next.js _app)
│   │   │   ├── Router.tsx            # Client-side routing (React Router)
│   │   │   ├── Shell.tsx             # PWA shell layout
│   │   │   └── ServiceWorker.ts      # Service Worker management
│   │   ├── components/               # Reusable UI Components
│   │   │   ├── ui/                   # Base UI Components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── ProgressBar.tsx
│   │   │   │   └── LoadingSpinner.tsx
│   │   │   ├── layout/               # Layout Components
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── MainLayout.tsx
│   │   │   ├── game/                 # Game-specific Components
│   │   │   │   ├── EnergyMeter.tsx
│   │   │   │   ├── TokenBalance.tsx
│   │   │   │   ├── ReputationDisplay.tsx
│   │   │   │   └── InteractionCanvas.tsx
│   │   │   ├── governors/            # Governor Components
│   │   │   │   ├── GovernorCard.tsx
│   │   │   │   ├── GovernorList.tsx
│   │   │   │   ├── InteractionModal.tsx
│   │   │   │   └── DialogueSystem.tsx
│   │   │   ├── inventory/            # Inventory Components
│   │   │   │   ├── InventoryGrid.tsx
│   │   │   │   ├── ArtifactCard.tsx
│   │   │   │   └── ArtifactDetails.tsx
│   │   │   ├── wallet/               # Bitcoin Wallet Components ⚠️ **REPLACES**: Auth components
│   │   │   │   ├── WalletConnector.tsx
│   │   │   │   ├── TransactionBuilder.tsx
│   │   │   │   └── TransactionStatus.tsx
│   │   │   ├── ~~auth/~~             # ❌ **REMOVED** - Authentication Components
│   │   │   │   ├── ~~LoginModal.tsx~~     # ❌ **DEPRECATED** - Use WalletConnector instead
│   │   │   │   ├── ~~WalletAuth.tsx~~     # ❌ **DEPRECATED** - Merged into WalletConnector
│   │   │   │   ├── ~~SocialAuth.tsx~~     # ❌ **DEPRECATED** - No social auth needed
│   │   │   │   ├── ~~SessionManager.tsx~~ # ❌ **DEPRECATED** - No server sessions
│   │   │   │   └── ~~RecoveryFlow.tsx~~   # ❌ **DEPRECATED** - Wallet handles recovery
│   │   │   └── analytics/            # Analytics Components
│   │   │       ├── EventTracker.tsx
│   │   │       ├── ABTest.tsx
│   │   │       ├── UserBehavior.tsx
│   │   │       └── MetricsCollector.tsx
│   │   ├── hooks/                    # Custom React Hooks
│   │   │   ├── usePlayerState.ts
│   │   │   ├── useGovernor.ts
│   │   │   ├── useInventory.ts
│   │   │   ├── useTransactions.ts
│   │   │   ├── useWallet.ts          # ⚠️ **REPLACES**: useAuth.ts
│   │   │   ├── useRealTime.ts
│   │   │   ├── ~~useAuth.ts~~        # ❌ **REMOVED** - Replaced by useWallet.ts
│   │   │   ├── ~~useSession.ts~~     # ❌ **REMOVED** - No server sessions
│   │   │   ├── useAnalytics.ts
│   │   │   ├── useI18n.ts
│   │   │   └── useAccessibility.ts
│   │   ├── lib/                      # Utility Libraries
│   │   │   ├── apollo/               # GraphQL Setup
│   │   │   │   ├── client.ts
│   │   │   │   ├── queries.ts
│   │   │   │   ├── mutations.ts
│   │   │   │   └── subscriptions.ts
│   │   │   ├── bitcoin/              # Bitcoin Integration
│   │   │   │   ├── wallet.ts
│   │   │   │   ├── transactions.ts
│   │   │   │   └── ordinals.ts
│   │   │   ├── game/                 # Game Logic
│   │   │   │   ├── mechanics.ts
│   │   │   │   ├── validation.ts
│   │   │   │   └── constants.ts
│   │   │   ├── ~~auth/~~             # ❌ **REMOVED** - Authentication Logic
│   │   │   │   ├── ~~jwt.ts~~        # ❌ **DEPRECATED** - No JWT tokens
│   │   │   │   ├── ~~wallet-auth.ts~~ # ❌ **DEPRECATED** - Moved to bitcoin/wallet.ts
│   │   │   │   ├── ~~social-auth.ts~~ # ❌ **DEPRECATED** - No social auth
│   │   │   │   └── ~~session.ts~~    # ❌ **DEPRECATED** - No server sessions
│   │   │   ├── analytics/            # Analytics Integration
│   │   │   │   ├── posthog.ts
│   │   │   │   ├── mixpanel.ts
│   │   │   │   ├── events.ts
│   │   │   │   └── tracking.ts
│   │   │   ├── i18n/                 # Internationalization
│   │   │   │   ├── config.ts
│   │   │   │   ├── loader.ts
│   │   │   │   ├── translator.ts
│   │   │   │   └── formatter.ts
│   │   │   ├── accessibility/        # Accessibility Utilities
│   │   │   │   ├── keyboard-nav.ts
│   │   │   │   ├── screen-reader.ts
│   │   │   │   ├── focus-management.ts
│   │   │   │   └── aria-helpers.ts
│   │   │   ├── utils/                # General Utilities
│   │   │   │   ├── formatting.ts
│   │   │   │   ├── encryption.ts
│   │   │   │   └── helpers.ts
│   │   │   └── types/                # TypeScript Types
│   │   │       ├── game.ts
│   │   │       ├── api.ts
│   │   │       ├── wallet.ts         # ⚠️ **REPLACES**: auth.ts
│   │   │       ├── ~~auth.ts~~       # ❌ **REMOVED** - Wallet types cover identity
│   │   │       ├── analytics.ts
│   │   │       └── i18n.ts
│   │   ├── styles/                   # Styling
│   │   │   ├── globals.css
│   │   │   ├── components.css
│   │   │   ├── design-system/        # Design System Styles
│   │   │   │   ├── tokens.css
│   │   │   │   ├── foundations.css
│   │   │   │   ├── components.css
│   │   │   │   └── themes.css
│   │   │   ├── themes/
│   │   │   │   ├── dark.css
│   │   │   │   ├── occult.css
│   │   │   │   └── accessibility.css
│   │   │   └── responsive/           # Responsive Design
│   │   │       ├── mobile.css
│   │   │       ├── tablet.css
│   │   │       └── desktop.css
│   │   ├── providers/                # Context Providers
│   │   │   ├── WalletProvider.tsx    # ⚠️ **REPLACES**: AuthProvider.tsx
│   │   │   ├── GameStateProvider.tsx
│   │   │   ├── ThemeProvider.tsx
│   │   │   ├── ~~AuthProvider.tsx~~  # ❌ **REMOVED** - Replaced by WalletProvider
│   │   │   ├── I18nProvider.tsx
│   │   │   ├── AnalyticsProvider.tsx
│   │   │   └── AccessibilityProvider.tsx
│   │   ├── locales/                  # Internationalization Files
│   │   │   ├── en/
│   │   │   │   ├── common.json
│   │   │   │   ├── game.json
│   │   │   │   ├── governors.json
│   │   │   │   ├── artifacts.json
│   │   │   │   └── ui.json
│   │   │   ├── es/
│   │   │   │   ├── common.json
│   │   │   │   ├── game.json
│   │   │   │   ├── governors.json
│   │   │   │   ├── artifacts.json
│   │   │   │   └── ui.json
│   │   │   ├── fr/
│   │   │   │   ├── common.json
│   │   │   │   ├── game.json
│   │   │   │   ├── governors.json
│   │   │   │   ├── artifacts.json
│   │   │   │   └── ui.json
│   │   │   ├── de/
│   │   │   │   ├── common.json
│   │   │   │   ├── game.json
│   │   │   │   ├── governors.json
│   │   │   │   ├── artifacts.json
│   │   │   │   └── ui.json
│   │   │   └── zh/
│   │   │       ├── common.json
│   │   │       ├── game.json
│   │   │       ├── governors.json
│   │   │       ├── artifacts.json
│   │   │       └── ui.json
│   │   └── accessibility/            # Accessibility Configuration
│   │       ├── axe-config.js
│   │       ├── screen-reader-config.js
│   │       ├── keyboard-nav-config.js
│   │       └── wcag-compliance.json
├── .storybook/                   # Storybook Configuration
│   ├── main.js
│   ├── preview.js
│   ├── manager.js
│   ├── theme.js
│   └── addons.js
├── stories/                      # Storybook Stories
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.stories.tsx
│   │   │   ├── Modal.stories.tsx
│   │   │   ├── Input.stories.tsx
│   │   │   └── Card.stories.tsx
│   │   ├── game/
│   │   │   ├── EnergyMeter.stories.tsx
│   │   │   ├── TokenBalance.stories.tsx
│   │   │   └── ReputationDisplay.stories.tsx
│   │   └── governors/
│   │       ├── GovernorCard.stories.tsx
│   │       ├── GovernorList.stories.tsx
│   │       └── InteractionModal.stories.tsx
│   ├── foundations/
│   │   ├── Colors.stories.tsx
│   │   ├── Typography.stories.tsx
│   │   ├── Spacing.stories.tsx
│   │   └── Icons.stories.tsx
│   └── patterns/
│       ├── Navigation.stories.tsx
│       ├── Forms.stories.tsx
│       └── DataDisplay.stories.tsx
└── .next/                        # Next.js Build Output
```

## ⚙️ Backend Structure (Alkanes + MetaShrew)
```
backend/
├── package.json
├── Cargo.toml                    # Rust workspace config
├── .env.example
├── contracts/                    # Alkanes Smart Contracts
│   ├── Cargo.toml
│   ├── src/
│   │   ├── lib.rs
│   │   ├── constants.rs
│   │   ├── types.rs
│   │   ├── state/                # Game State Management
│   │   │   ├── mod.rs
│   │   │   ├── player.rs
│   │   │   ├── governors.rs
│   │   │   ├── artifacts.rs
│   │   │   └── watchtower.rs
│   │   ├── handlers/             # Transaction Handlers
│   │   │   ├── mod.rs
│   │   │   ├── init_player.rs
│   │   │   ├── interact_governor.rs
│   │   │   ├── craft_artifact.rs
│   │   │   ├── gamble.rs
│   │   │   └── energy_management.rs
│   │   ├── protocols/            # Protocol Implementations
│   │   │   ├── mod.rs
│   │   │   ├── enochian_keys.rs
│   │   │   ├── aethyr_system.rs
│   │   │   ├── reputation.rs
│   │   │   └── artifact_creation.rs
│   │   ├── utils/                # Contract Utilities
│   │   │   ├── mod.rs
│   │   │   ├── validation.rs
│   │   │   ├── encryption.rs
│   │   │   └── parsing.rs
│   │   └── tests/                # Contract Tests
│   │       ├── mod.rs
│   │       ├── player_tests.rs
│   │       ├── governor_tests.rs
│   │       └── artifact_tests.rs
│   └── deploy/                   # Deployment Scripts
│       ├── deploy.rs
│       ├── migrate.rs
│       └── setup.rs
├── indexer/                      # MetaShrew Indexer
│   ├── Cargo.toml
│   ├── src/
│   │   ├── main.rs
│   │   ├── lib.rs
│   │   ├── config.rs
│   │   ├── indexer/              # Core Indexing Logic
│   │   │   ├── mod.rs
│   │   │   ├── block_processor.rs
│   │   │   ├── transaction_parser.rs
│   │   │   └── state_updater.rs
│   │   ├── api/                  # GraphQL API Server
│   │   │   ├── mod.rs
│   │   │   ├── server.rs
│   │   │   ├── schema.rs
│   │   │   ├── resolvers/
│   │   │   │   ├── mod.rs
│   │   │   │   ├── player.rs
│   │   │   │   ├── governors.rs
│   │   │   │   ├── artifacts.rs
│   │   │   │   └── watchtower.rs
│   │   │   └── subscriptions/
│   │   │       ├── mod.rs
│   │   │       ├── blocks.rs
│   │   │       └── events.rs
│   │   ├── storage/              # Data Storage Layer
│   │   │   ├── mod.rs
│   │   │   ├── postgres.rs
│   │   │   ├── redis.rs
│   │   │   └── models/
│   │   │       ├── mod.rs
│   │   │       ├── player.rs
│   │   │       ├── governor.rs
│   │   │       ├── artifact.rs
│   │   │       └── transaction.rs
│   │   ├── bitcoin/              # Bitcoin Integration
│   │   │   ├── mod.rs
│   │   │   ├── rpc_client.rs
│   │   │   ├── block_parser.rs
│   │   │   └── ordinals.rs
│   │   └── utils/                # General Utilities
│   │       ├── mod.rs
│   │       ├── logging.rs
│   │       ├── metrics.rs
│   │       └── helpers.rs
│   └── migrations/               # Database Migrations
│       ├── 001_initial.sql
│       ├── 002_players.sql
│       ├── 003_governors.sql
│       └── 004_artifacts.sql
├── api/                          # Express.js API Gateway
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── app.ts
│   │   ├── server.ts
│   │   ├── config.ts
│   │   ├── middleware/           # Express Middleware
│   │   │   ├── cors.ts
│   │   │   └── validation.ts
│   │   ├── routes/               # API Routes
│   │   │   ├── index.ts
│   │   │   ├── players.ts
│   │   │   ├── governors.ts
│   │   │   ├── artifacts.ts
│   │   │   └── watchtower.ts
│   │   ├── services/             # Business Logic
│   │   │   ├── player-service.ts
│   │   │   ├── governor-service.ts
│   │   │   ├── artifact-service.ts
│   │   │   └── blockchain-service.ts
│   │   ├── utils/                # API Utilities
│   │   │   ├── logger.ts
│   │   │   └── validator.ts
│   │   └── types/                # Type Definitions
│   │       ├── api.ts
│   │       ├── blockchain.ts
│   │       └── game.ts
│   └── tests/                    # API Tests
│       ├── unit/
│       ├── integration/
│       └── e2e/
├── analytics/                    # Gameplay Analytics & Telemetry
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── app.ts
│   │   ├── config.ts
│   │   ├── collectors/
│   │   │   ├── gameplay-events.ts
│   │   │   ├── user-behavior.ts
│   │   │   ├── performance-metrics.ts
│   │   │   └── business-metrics.ts
│   │   ├── processors/
│   │   │   ├── event-processor.ts
│   │   │   ├── aggregator.ts
│   │   │   ├── real-time.ts
│   │   │   └── batch.ts
│   │   ├── exporters/
│   │   │   ├── posthog.ts
│   │   │   ├── mixpanel.ts
│   │   │   ├── amplitude.ts
│   │   │   └── custom-dashboard.ts
│   │   ├── models/
│   │   │   ├── events.ts
│   │   │   ├── metrics.ts
│   │   │   └── sessions.ts
│   │   └── utils/
│   │       ├── kafka-client.ts
│   │       ├── redis-client.ts
│   │       └── validators.ts
│   └── kafka/                    # Kafka configuration
│       ├── topics.yml
│       ├── producers.yml
│       └── consumers.yml
├── content/                      # Dynamic Content Management System
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── app.ts
│   │   ├── config.ts
│   │   ├── cms/
│   │   │   ├── git-backend.ts
│   │   │   ├── content-parser.ts
│   │   │   ├── validation.ts
│   │   │   └── deployment.ts
│   │   ├── api/
│   │   │   ├── content.ts
│   │   │   ├── preview.ts
│   │   │   ├── publish.ts
│   │   │   └── webhooks.ts
│   │   ├── models/
│   │   │   ├── content.ts
│   │   │   ├── version.ts
│   │   │   └── workflow.ts
│   │   ├── services/
│   │   │   ├── content-service.ts
│   │   │   ├── version-service.ts
│   │   │   ├── workflow-service.ts
│   │   │   └── sync-service.ts
│   │   └── utils/
│   │       ├── markdown.ts
│   │       ├── validators.ts
│   │       └── transformers.ts
│   ├── content/                  # Git-based content repository
│   │   ├── governors/
│   │   │   ├── lore/
│   │   │   ├── personalities/
│   │   │   └── dialog-updates/
│   │   ├── quests/
│   │   │   ├── seasonal/
│   │   │   ├── events/
│   │   │   └── storylines/
│   │   ├── artifacts/
│   │   │   ├── descriptions/
│   │   │   ├── lore/
│   │   │   └── mechanics/
│   │   └── system/
│   │       ├── announcements/
│   │       ├── help-content/
│   │       └── ui-text/
│   └── workflows/                # Editorial workflows
│       ├── content-review.yml
│       ├── translation.yml
│       └── publish.yml
├── secrets/                      # Enterprise Secrets Management
│   ├── vault/
│   │   ├── config.yml
│   │   ├── policies/
│   │   │   ├── api-access.hcl
│   │   │   ├── database-access.hcl
│   │   │   └── blockchain-access.hcl
│   │   └── scripts/
│   │       ├── init-vault.sh
│   │       ├── rotate-secrets.sh
│   │       └── backup-vault.sh
│   ├── k8s-secrets/
│   │   ├── secret-provider-class.yml
│   │   ├── vault-injector.yml
│   │   └── external-secrets.yml
│   └── aws-secrets/              # AWS Secrets Manager (alternative)
│       ├── secret-definitions.yml
│       ├── rotation-lambda/
│       └── access-policies.json
└── data/                         # Static Game Data
    ├── governors/                # Governor Profiles & Data
    │   ├── profiles.json
    │   ├── personalities/
    │   │   ├── governor_01.json
    │   │   ├── governor_02.json
    │   │   └── ...
    │   └── templates/
    ├── artifacts/                # Artifact Definitions
    │   ├── blueprints.json
    │   ├── materials.json
    │   └── recipes.json
    ├── enochian/                 # Enochian System Data
    │   ├── keys.json
    │   ├── aethyrs.json
    │   ├── elements.json
    │   └── correspondences.json
    └── game/                     # Game Configuration
        ├── mechanics.json
        ├── constants.json
        └── balancing.json
```

## 🔗 Shared Types & Utilities
```
shared/
├── package.json
├── tsconfig.json
├── src/
│   ├── types/                    # Cross-platform Type Definitions
│   │   ├── index.ts
│   │   ├── game/                 # Game-specific Types
│   │   │   ├── player.ts
│   │   │   ├── governor.ts
│   │   │   ├── artifact.ts
│   │   │   ├── watchtower.ts
│   │   │   └── mechanics.ts
│   │   ├── blockchain/           # Blockchain Types
│   │   │   ├── transaction.ts
│   │   │   ├── ordinals.ts
│   │   │   ├── alkanes.ts
│   │   │   └── bitcoin.ts
│   │   ├── api/                  # API Interface Types
│   │   │   ├── requests.ts
│   │   │   ├── responses.ts
│   │   │   ├── graphql.ts
│   │   │   └── websocket.ts
│   │   └── enochian/            # Enochian System Types
│   │       ├── governors.ts
│   │       ├── aethyrs.ts
│   │       ├── keys.ts
│   │       └── elements.ts
│   ├── utils/                    # Shared Utility Functions
│   │   ├── index.ts
│   │   ├── validation/           # Data Validation
│   │   │   ├── player.ts
│   │   │   ├── governor.ts
│   │   │   ├── transaction.ts
│   │   │   └── enochian.ts
│   │   ├── formatting/           # Data Formatting
│   │   │   ├── bitcoin.ts
│   │   │   ├── currency.ts
│   │   │   ├── time.ts
│   │   │   └── text.ts
│   │   ├── crypto/               # Cryptographic Functions
│   │   │   ├── hash.ts
│   │   │   ├── sign.ts
│   │   │   └── encrypt.ts
│   │   └── game/                 # Game Logic Helpers
│   │       ├── mechanics.ts
│   │       ├── calculations.ts
│   │       ├── randomness.ts
│   │       └── state.ts
│   ├── constants/                # Shared Constants
│   │   ├── index.ts
│   │   ├── game.ts
│   │   ├── blockchain.ts
│   │   ├── api.ts
│   │   └── enochian.ts
│   └── schemas/                  # Data Schemas & Validation
│       ├── index.ts
│       ├── game/
│       │   ├── player.schema.ts
│       │   ├── governor.schema.ts
│       │   └── artifact.schema.ts
│       ├── api/
│       │   ├── request.schema.ts
│       │   └── response.schema.ts
│       └── blockchain/
│           ├── transaction.schema.ts
│           └── alkanes.schema.ts
└── dist/                         # Compiled Output
```

## 🎨 Assets Directory Structure
```
assets/
├── README.md                     # Asset guidelines & specs
├── raw/                          # Source files (PSD, AI, etc.)
│   ├── governors/
│   │   ├── portraits/
│   │   ├── sigils/
│   │   └── backgrounds/
│   ├── artifacts/
│   │   ├── weapons/
│   │   ├── talismans/
│   │   └── scrolls/
│   ├── ui/
│   │   ├── components/
│   │   ├── icons/
│   │   └── backgrounds/
│   └── animations/
│       ├── governors/
│       ├── effects/
│       └── transitions/
├── processed/                    # Optimized game-ready assets
│   ├── governors/                # 91 Governor Assets
│   │   ├── portraits/            # High-res governor portraits
│   │   │   ├── 01_occodon.webp
│   │   │   ├── 02_pascomb.webp
│   │   │   └── ...               # All 91 governors
│   │   ├── thumbnails/           # Smaller versions for lists
│   │   │   ├── 01_occodon_thumb.webp
│   │   │   ├── 02_pascomb_thumb.webp
│   │   │   └── ...
│   │   ├── sigils/               # Governor sigils/seals
│   │   │   ├── 01_occodon_sigil.svg
│   │   │   ├── 02_pascomb_sigil.svg
│   │   │   └── ...
│   │   ├── backgrounds/          # Governor-specific backgrounds
│   │   │   ├── 01_occodon_bg.webp
│   │   │   ├── 02_pascomb_bg.webp
│   │   │   └── ...
│   │   └── animations/           # Governor interaction animations
│   │       ├── idle/
│   │       ├── speaking/
│   │       └── blessing/
│   ├── artifacts/                # Artifact Assets
│   │   ├── weapons/              # Weapon artifacts
│   │   │   ├── swords/
│   │   │   ├── staves/
│   │   │   └── daggers/
│   │   ├── talismans/            # Talisman artifacts
│   │   │   ├── rings/
│   │   │   ├── amulets/
│   │   │   └── pendants/
│   │   ├── scrolls/              # Scroll artifacts
│   │   │   ├── invocations/
│   │   │   ├── banishments/
│   │   │   └── transmutations/
│   │   └── materials/            # Crafting materials
│   │       ├── metals/
│   │       ├── gems/
│   │       └── essences/
│   ├── ui/                       # User Interface Assets
│   │   ├── components/           # UI Component graphics
│   │   │   ├── buttons/
│   │   │   ├── panels/
│   │   │   ├── modals/
│   │   │   └── forms/
│   │   ├── icons/                # System icons
│   │   │   ├── energy.svg
│   │   │   ├── reputation.svg
│   │   │   ├── bitcoin.svg
│   │   │   └── watchtower.svg
│   │   ├── backgrounds/          # UI backgrounds
│   │   │   ├── main_bg.webp
│   │   │   ├── modal_bg.webp
│   │   │   └── card_bg.webp
│   │   ├── borders/              # Decorative borders
│   │   │   ├── panels/
│   │   │   ├── cards/
│   │   │   └── modals/
│   │   └── cursors/              # Custom cursors
│   │       ├── default.png
│   │       ├── interact.png
│   │       └── loading.png
│   ├── enochian/                 # Enochian System Assets
│   │   ├── alphabet/             # Enochian letters
│   │   │   ├── un.svg
│   │   │   ├── pa.svg
│   │   │   └── ...               # All 21 letters
│   │   ├── aethyrs/              # 30 Aethyr symbols
│   │   │   ├── lil.svg
│   │   │   ├── arn.svg
│   │   │   └── ...
│   │   ├── elements/             # Elemental symbols
│   │   │   ├── fire.svg
│   │   │   ├── water.svg
│   │   │   ├── air.svg
│   │   │   └── earth.svg
│   │   └── keys/                 # 19 Enochian Keys
│   │       ├── key_01.webp
│   │       ├── key_02.webp
│   │       └── ...
│   ├── effects/                  # Visual Effects
│   │   ├── particles/            # Particle system assets
│   │   │   ├── fire/
│   │   │   ├── water/
│   │   │   ├── air/
│   │   │   └── earth/
│   │   ├── lighting/             # Lighting effects
│   │   │   ├── glow.png
│   │   │   ├── beam.png
│   │   │   └── aura.png
│   │   └── transitions/          # Page/state transitions
│   │       ├── fade.webm
│   │       ├── portal.webm
│   │       └── shimmer.webm
│   └── audio/                    # Game Audio Assets
│       ├── music/                # Background music
│       │   ├── main_theme.ogg
│       │   ├── governor_themes/
│       │   │   ├── occodon.ogg
│       │   │   ├── pascomb.ogg
│       │   │   └── ...
│       │   └── ambient/
│       │       ├── watchtower.ogg
│       │       ├── aethyrs.ogg
│       │       └── crafting.ogg
│       ├── sfx/                  # Sound effects
│       │   ├── ui/
│       │   │   ├── click.ogg
│       │   │   ├── hover.ogg
│       │   │   └── error.ogg
│       │   ├── game/
│       │   │   ├── energy_gain.ogg
│       │   │   ├── artifact_craft.ogg
│       │   │   └── governor_speak.ogg
│       │   └── ambient/
│       │       ├── wind.ogg
│       │       ├── energy_hum.ogg
│       │       └── portal_open.ogg
│       └── voice/                # Voice lines (if any)
│           ├── governors/
│           └── narrator/
└── sprites/                      # Sprite sheets & animations
    ├── governors/                # Governor animation sprites
    ├── artifacts/                # Artifact sprites
    ├── ui/                       # UI element sprites
    └── effects/                  # Effect sprites
```

## 🔧 Scripts & Automation
```
scripts/
├── README.md                     # Script documentation
├── setup/                        # Environment setup
│   ├── install.sh
│   ├── configure.sh
│   └── verify.sh
├── build/                        # Build automation
│   ├── frontend.sh
│   ├── backend.sh
│   ├── contracts.sh
│   ├── assets.sh
│   ├── storybook.sh
│   ├── i18n-extract.sh
│   ├── security-scan.sh
│   └── cdn-deploy.sh
├── deploy/                       # Deployment scripts
│   ├── staging.sh
│   ├── production.sh
│   ├── rollback.sh
│   ├── migrate.sh
│   ├── cdn-invalidate.sh
│   ├── secrets-rotate.sh
│   └── content-deploy.sh
├── development/                  # Development utilities
│   ├── start-dev.sh
│   ├── seed-data.sh
│   ├── reset-db.sh
│   ├── generate-types.sh
│   ├── start-storybook.sh
│   ├── analytics-debug.sh
│   └── i18n-sync.sh
├── testing/                      # Testing automation
│   ├── run-tests.sh
│   ├── e2e-tests.sh
│   ├── load-tests.sh
│   ├── security-scan.sh
│   ├── accessibility-tests.sh
│   ├── visual-regression.sh
│   ├── smart-contract-audit.sh
│   └── performance-tests.sh
├── maintenance/                  # Maintenance scripts
│   ├── backup.sh
│   ├── cleanup.sh
│   ├── health-check.sh
│   ├── update-deps.sh
│   ├── cache-clear.sh
│   ├── analytics-export.sh
│   └── content-sync.sh
├── security/                     # Security Scripts
│   ├── vulnerability-scan.sh
│   ├── dependency-check.sh
│   ├── secrets-audit.sh
│   ├── compliance-check.sh
│   ├── penetration-test.sh
│   └── incident-response.sh
└── data/                        # Data management
    ├── export-governors.sh
    ├── import-assets.sh
    ├── validate-data.sh
    ├── sync-blockchain.sh
    ├── analytics-migrate.sh
    ├── i18n-import.sh
    └── content-backup.sh
```

## 🧪 Testing Structure
```
tests/
├── README.md                     # Testing documentation
├── jest.config.js               # Jest configuration
├── playwright.config.ts        # E2E test configuration
├── setup/                       # Test setup files
│   ├── global-setup.ts
│   ├── test-env.ts
│   └── mocks/
│       ├── bitcoin-wallet.ts
│       ├── alkanes-api.ts
│       └── metashrew.ts
├── unit/                        # Unit tests
│   ├── frontend/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── lib/
│   ├── backend/
│   │   ├── contracts/
│   │   ├── indexer/
│   │   ├── api/
│   │   └── services/
│   └── shared/
│       ├── types/
│       ├── utils/
│       └── schemas/
├── integration/                 # Integration tests
│   ├── api/
│   │   ├── player-flows.test.ts
│   │   ├── governor-interactions.test.ts
│   │   └── artifact-crafting.test.ts
│   ├── blockchain/
│   │   ├── alkanes-integration.test.ts
│   │   ├── metashrew-indexing.test.ts
│   │   └── bitcoin-transactions.test.ts
│   └── database/
│       ├── postgres-operations.test.ts
│       └── redis-caching.test.ts
├── e2e/                         # End-to-end tests
│   ├── user-journeys/
│   │   ├── new-player-onboarding.spec.ts
│   │   ├── governor-interaction.spec.ts
│   │   ├── artifact-crafting.spec.ts
│   │   └── gambling-mechanics.spec.ts
│   ├── game-mechanics/
│   │   ├── energy-system.spec.ts
│   │   ├── reputation-tracking.spec.ts
│   │   └── watchtower-progression.spec.ts
│   └── cross-browser/
│       ├── chrome.spec.ts
│       ├── firefox.spec.ts
│       └── safari.spec.ts
├── performance/                 # Performance tests
│   ├── load-testing/
│   │   ├── api-load.test.ts
│   │   ├── frontend-perf.test.ts
│   │   └── blockchain-sync.test.ts
│   └── stress-testing/
│       ├── concurrent-users.test.ts
│       └── high-volume-tx.test.ts
├── security/                    # Security tests
│   ├── authentication.test.ts
│   ├── wallet-security.test.ts
│   ├── input-validation.test.ts
│   └── smart-contract-audit.test.ts
└── fixtures/                    # Test data fixtures
    ├── players/
    ├── governors/
    ├── artifacts/
    └── transactions/
```

## 🚀 Infrastructure & DevOps
```
infrastructure/
├── README.md                    # Infrastructure documentation
├── docker/                      # Docker configurations
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   ├── Dockerfile.indexer
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── docker-compose.prod.yml
├── kubernetes/                  # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmaps/
│   │   ├── frontend-config.yaml
│   │   ├── backend-config.yaml
│   │   └── indexer-config.yaml
│   ├── deployments/
│   │   ├── frontend-deployment.yaml
│   │   ├── backend-deployment.yaml
│   │   ├── indexer-deployment.yaml
│   │   └── postgres-deployment.yaml
│   ├── services/
│   │   ├── frontend-service.yaml
│   │   ├── backend-service.yaml
│   │   └── postgres-service.yaml
│   ├── ingress/
│   │   ├── frontend-ingress.yaml
│   │   └── api-ingress.yaml
│   └── secrets/
│       ├── api-keys.yaml
│       └── database-secrets.yaml
├── terraform/                   # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/
│   │   ├── networking/
│   │   ├── compute/
│   │   ├── storage/
│   │   ├── monitoring/
│   │   ├── cdn/                  # CDN & Asset Distribution
│   │   │   ├── cloudflare.tf
│   │   │   ├── aws-cloudfront.tf
│   │   │   ├── cache-rules.tf
│   │   │   └── ssl-certificates.tf
│   │   ├── secrets/              # Secrets Management
│   │   │   ├── vault.tf
│   │   │   ├── aws-secrets.tf
│   │   │   ├── k8s-secrets.tf
│   │   │   └── rotation.tf
│   │   └── security/             # Security Infrastructure
│   │       ├── waf.tf
│   │       ├── ddos-protection.tf
│   │       ├── security-groups.tf
│   │       └── audit-logging.tf
│   └── environments/
│       ├── development/
│       ├── staging/
│       └── production/
├── monitoring/                  # Monitoring & observability
│   ├── prometheus/
│   │   ├── config.yml
│   │   └── rules/
│   ├── grafana/
│   │   ├── dashboards/
│   │   │   ├── system-metrics.json
│   │   │   ├── api-performance.json
│   │   │   └── game-analytics.json
│   │   └── provisioning/
│   ├── alertmanager/
│   │   ├── config.yml
│   │   └── templates/
│   └── jaeger/
│       └── config.yml
├── nginx/                       # Reverse proxy configuration
│   ├── nginx.conf
│   ├── sites-available/
│   │   ├── frontend.conf
│   │   ├── api.conf
│   │   └── indexer.conf
│   └── ssl/
│       ├── certificates/
│       └── configs/
├── backup/                      # Backup strategies
│   ├── database/
│   │   ├── backup-script.sh
│   │   └── restore-script.sh
│   ├── assets/
│   │   └── sync-assets.sh
│   └── blockchain/
│       └── sync-state.sh
└── ci-cd/                      # CI/CD configurations
    ├── github-actions/
    │   ├── test.yml
    │   ├── build.yml
    │   ├── deploy.yml
    │   ├── security-scan.yml
    │   ├── smart-contract-audit.yml
    │   ├── accessibility-test.yml
    │   ├── visual-regression.yml
    │   ├── storybook-deploy.yml
    │   ├── i18n-validation.yml
    │   ├── dependency-update.yml
    │   ├── performance-test.yml
    │   ├── cdn-deploy.yml
    │   └── secrets-rotation.yml
    ├── gitlab-ci/
    │   ├── .gitlab-ci.yml
    │   ├── security-pipeline.yml
    │   ├── accessibility-pipeline.yml
    │   ├── storybook-pipeline.yml
    │   └── i18n-pipeline.yml
    ├── jenkins/
    │   ├── Jenkinsfile
    │   ├── security-pipeline.groovy
    │   ├── accessibility-pipeline.groovy
    │   └── deployment-pipeline.groovy
    └── workflows/
        ├── security/
        │   ├── smart-contract-audit.yml
        │   ├── dependency-scan.yml
        │   ├── code-security-scan.yml
        │   ├── container-scan.yml
        │   └── penetration-test.yml
        ├── quality/
        │   ├── accessibility-audit.yml
        │   ├── performance-audit.yml
        │   ├── visual-regression.yml
        │   └── code-quality.yml
        ├── deployment/
        │   ├── staging-deploy.yml
        │   ├── production-deploy.yml
        │   ├── rollback.yml
        │   ├── cdn-deploy.yml
        │   └── content-deploy.yml
        └── maintenance/
            ├── dependency-update.yml
            ├── security-patches.yml
            ├── cache-warming.yml
            └── health-checks.yml
```

## 📚 Documentation Structure
```
docs/
├── README.md                    # Main documentation index
├── game-design/                 # Game design documents
│   ├── mechanics.md
│   ├── governors.md
│   ├── artifacts.md
│   ├── enochian-system.md
│   └── progression.md
├── technical/                   # Technical documentation
│   ├── architecture.md
│   ├── api-reference.md
│   ├── smart-contracts.md
│   ├── blockchain-integration.md
│   └── security.md
├── user-guides/                 # User documentation
│   ├── getting-started.md
│   ├── wallet-setup.md
│   ├── gameplay.md
│   └── troubleshooting.md
├── developer/                   # Developer documentation
│   ├── setup.md
│   ├── contribution-guide.md
│   ├── coding-standards.md
│   ├── testing-guide.md
│   └── deployment.md
├── assets/                      # Documentation assets
│   ├── images/
│   ├── diagrams/
│   └── videos/
└── legal/                       # Legal documentation
    ├── terms-of-service.md
    ├── privacy-policy.md
    └── licenses/
```

## ⚠️ **REALISTIC INFRASTRUCTURE CLARIFICATION**

### **"Minimal Off-Chain Core" (Not Zero Infrastructure)**

**CRITICAL CORRECTION**: The "zero-infrastructure" claim is misleading. While we eliminate traditional web servers, databases, and CDNs, **these services still require hosting:**

```
minimal-infrastructure/
├── metashrew-indexer/            # ⚠️ **REQUIRED** - Always-on indexer node
│   ├── bitcoin-node/             # Full Bitcoin node (500GB+ storage)
│   ├── indexer-service/          # MetaShrew GraphQL server
│   ├── postgres/                 # Indexer database (for query performance)
│   └── redis/                    # Caching layer
├── monitoring/                   # ⚠️ **REQUIRED** - Health monitoring
│   ├── prometheus/               # Metrics collection
│   ├── grafana/                  # Dashboards
│   └── alertmanager/             # Alert notifications
├── backup/                       # ⚠️ **REQUIRED** - Data backup
│   ├── bitcoin-snapshots/        # Blockchain state backups
│   ├── indexer-snapshots/        # Index database backups
│   └── s3-storage/               # Off-site backup storage
└── security/                     # ⚠️ **REQUIRED** - Security services
    ├── vault/                    # Secrets management (optional)
    └── audit-logging/            # Security audit logs
```

### **Realistic Monthly Operating Costs**

| Service Category | Monthly Cost (USD) | Annual Cost (USD) | Notes |
|------------------|-------------------|-------------------|--------|
| **MetaShrew Indexer Node** | $75-150 | $900-1,800 | Bitcoin node + indexer (4-8 vCPU, 16-32GB RAM, 1TB SSD) |
| **Monitoring & Alerts** | $25-50 | $300-600 | Prometheus, Grafana, AlertManager |
| **Backup & Storage** | $20-40 | $240-480 | S3 snapshots, off-site backup |
| **Security & Compliance** | $10-30 | $120-360 | Vault, audit logging, security scanning |
| **Network & DNS** | $10-20 | $120-240 | Domain, DNS, load balancer |
| **TOTAL ONGOING COSTS** | **$140-290** | **$1,680-3,480** | ⚠️ **NOT ZERO** but 95% less than traditional |

### **High Availability & Failover Plan**

```
redundancy-strategy/
├── primary-indexer/              # Primary MetaShrew node (US-East)
├── backup-indexer/               # Secondary MetaShrew node (EU-West)  
├── bitcoin-node-cluster/         # 2-3 Bitcoin nodes for redundancy
├── load-balancer/                # Route GraphQL queries to healthy nodes
└── automatic-failover/           # Health checks with 30s failover time
```

**Key Risk Mitigation:**
- If primary indexer fails, backup takes over within 30 seconds
- Community can run their own indexer nodes (open source)
- In worst case, clients can query Bitcoin network directly (slower but works)
- All critical data lives on Bitcoin blockchain (truly unstoppable)

---

## 🎨 Assets Directory Structure
```
assets/
├── README.md                     # Asset guidelines & specs
├── raw/                          # Source files (PSD, AI, etc.)
│   ├── governors/
│   │   ├── portraits/
│   │   ├── sigils/
│   │   └── backgrounds/
│   ├── artifacts/
│   │   ├── weapons/
│   │   ├── talismans/
│   │   └── scrolls/
│   ├── ui/
│   │   ├── components/
│   │   ├── icons/
│   │   └── backgrounds/
│   └── animations/
│       ├── governors/
│       ├── effects/
│       └── transitions/
├── processed/                    # Optimized game-ready assets
│   ├── governors/                # 91 Governor Assets
│   │   ├── portraits/            # High-res governor portraits
│   │   │   ├── 01_occodon.webp
│   │   │   ├── 02_pascomb.webp
│   │   │   └── ...               # All 91 governors
│   │   ├── thumbnails/           # Smaller versions for lists
│   │   │   ├── 01_occodon_thumb.webp
│   │   │   ├── 02_pascomb_thumb.webp
│   │   │   └── ...
│   │   ├── sigils/               # Governor sigils/seals
│   │   │   ├── 01_occodon_sigil.svg
│   │   │   ├── 02_pascomb_sigil.svg
│   │   │   └── ...
│   │   ├── backgrounds/          # Governor-specific backgrounds
│   │   │   ├── 01_occodon_bg.webp
│   │   │   ├── 02_pascomb_bg.webp
│   │   │   └── ...
│   │   └── animations/           # Governor interaction animations
│   │       ├── idle/
│   │       ├── speaking/
│   │       └── blessing/
│   ├── artifacts/                # Artifact Assets
│   │   ├── weapons/              # Weapon artifacts
│   │   │   ├── swords/
│   │   │   ├── staves/
│   │   │   └── daggers/
│   │   ├── talismans/            # Talisman artifacts
│   │   │   ├── rings/
│   │   │   ├── amulets/
│   │   │   └── pendants/
│   │   ├── scrolls/              # Scroll artifacts
│   │   │   ├── invocations/
│   │   │   ├── banishments/
│   │   │   └── transmutations/
│   │   └── materials/            # Crafting materials
│   │       ├── metals/
│   │       ├── gems/
│   │       └── essences/
│   ├── ui/                       # User Interface Assets
│   │   ├── components/           # UI Component graphics
│   │   │   ├── buttons/
│   │   │   ├── panels/
│   │   │   ├── modals/
│   │   │   └── forms/
│   │   ├── icons/                # System icons
│   │   │   ├── energy.svg
│   │   │   ├── reputation.svg
│   │   │   ├── bitcoin.svg
│   │   │   └── watchtower.svg
│   │   ├── backgrounds/          # UI backgrounds
│   │   │   ├── main_bg.webp
│   │   │   ├── modal_bg.webp
│   │   │   └── card_bg.webp
│   │   ├── borders/              # Decorative borders
│   │   │   ├── panels/
│   │   │   ├── cards/
│   │   │   └── modals/
│   │   └── cursors/              # Custom cursors
│   │       ├── default.png
│   │       ├── interact.png
│   │       └── loading.png
│   ├── enochian/                 # Enochian System Assets
│   │   ├── alphabet/             # Enochian letters
│   │   │   ├── un.svg
│   │   │   ├── pa.svg
│   │   │   └── ...               # All 21 letters
│   │   ├── aethyrs/              # 30 Aethyr symbols
│   │   │   ├── lil.svg
│   │   │   ├── arn.svg
│   │   │   └── ...
│   │   ├── elements/             # Elemental symbols
│   │   │   ├── fire.svg
│   │   │   ├── water.svg
│   │   │   ├── air.svg
│   │   │   └── earth.svg
│   │   └── keys/                 # 19 Enochian Keys
│   │       ├── key_01.webp
│   │       ├── key_02.webp
│   │       └── ...
│   ├── effects/                  # Visual Effects
│   │   ├── particles/            # Particle system assets
│   │   │   ├── fire/
│   │   │   ├── water/
│   │   │   ├── air/
│   │   │   └── earth/
│   │   ├── lighting/             # Lighting effects
│   │   │   ├── glow.png
│   │   │   ├── beam.png
│   │   │   └── aura.png
│   │   └── transitions/          # Page/state transitions
│   │       ├── fade.webm
│   │       ├── portal.webm
│   │       └── shimmer.webm
│   └── audio/                    # Game Audio Assets
│       ├── music/                # Background music
│       │   ├── main_theme.ogg
│       │   ├── governor_themes/
│       │   │   ├── occodon.ogg
│       │   │   ├── pascomb.ogg
│       │   │   └── ...
│       │   └── ambient/
│       │       ├── watchtower.ogg
│       │       ├── aethyrs.ogg
│       │       └── crafting.ogg
│       ├── sfx/                  # Sound effects
│       │   ├── ui/
│       │   │   ├── click.ogg
│       │   │   ├── hover.ogg
│       │   │   └── error.ogg
│       │   ├── game/
│       │   │   ├── energy_gain.ogg
│       │   │   ├── artifact_craft.ogg
│       │   │   └── governor_speak.ogg
│       │   └── ambient/
│       │       ├── wind.ogg
│       │       ├── energy_hum.ogg
│       │       └── portal_open.ogg
│       └── voice/                # Voice lines (if any)
│           ├── governors/
│           └── narrator/
└── sprites/                      # Sprite sheets & animations
    ├── governors/                # Governor animation sprites
    ├── artifacts/                # Artifact sprites
    ├── ui/                       # UI element sprites
    └── effects/                  # Effect sprites
```

## 🔧 Scripts & Automation
```
scripts/
├── README.md                     # Script documentation
├── setup/                        # Environment setup
│   ├── install.sh
│   ├── configure.sh
│   └── verify.sh
├── build/                        # Build automation
│   ├── frontend.sh
│   ├── backend.sh
│   ├── contracts.sh
│   ├── assets.sh
│   ├── storybook.sh
│   ├── i18n-extract.sh
│   ├── security-scan.sh
│   └── cdn-deploy.sh
├── deploy/                       # Deployment scripts
│   ├── staging.sh
│   ├── production.sh
│   ├── rollback.sh
│   ├── migrate.sh
│   ├── cdn-invalidate.sh
│   ├── secrets-rotate.sh
│   └── content-deploy.sh
├── development/                  # Development utilities
│   ├── start-dev.sh
│   ├── seed-data.sh
│   ├── reset-db.sh
│   ├── generate-types.sh
│   ├── start-storybook.sh
│   ├── analytics-debug.sh
│   └── i18n-sync.sh
├── testing/                      # Testing automation
│   ├── run-tests.sh
│   ├── e2e-tests.sh
│   ├── load-tests.sh
│   ├── security-scan.sh
│   ├── accessibility-tests.sh
│   ├── visual-regression.sh
│   ├── smart-contract-audit.sh
│   └── performance-tests.sh
├── maintenance/                  # Maintenance scripts
│   ├── backup.sh
│   ├── cleanup.sh
│   ├── health-check.sh
│   ├── update-deps.sh
│   ├── cache-clear.sh
│   ├── analytics-export.sh
│   └── content-sync.sh
├── security/                     # Security Scripts
│   ├── vulnerability-scan.sh
│   ├── dependency-check.sh
│   ├── secrets-audit.sh
│   ├── compliance-check.sh
│   ├── penetration-test.sh
│   └── incident-response.sh
└── data/                        # Data management
    ├── export-governors.sh
    ├── import-assets.sh
    ├── validate-data.sh
    ├── sync-blockchain.sh
    ├── analytics-migrate.sh
    ├── i18n-import.sh
    └── content-backup.sh
```

## 🧪 Testing Structure
```
tests/
├── README.md                     # Testing documentation
├── jest.config.js               # Jest configuration
├── playwright.config.ts        # E2E test configuration
├── setup/                       # Test setup files
│   ├── global-setup.ts
│   ├── test-env.ts
│   └── mocks/
│       ├── bitcoin-wallet.ts
│       ├── alkanes-api.ts
│       └── metashrew.ts
├── unit/                        # Unit tests
│   ├── frontend/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── lib/
│   ├── backend/
│   │   ├── contracts/
│   │   ├── indexer/
│   │   ├── api/
│   │   └── services/
│   └── shared/
│       ├── types/
│       ├── utils/
│       └── schemas/
├── integration/                 # Integration tests
│   ├── api/
│   │   ├── player-flows.test.ts
│   │   ├── governor-interactions.test.ts
│   │   └── artifact-crafting.test.ts
│   ├── blockchain/
│   │   ├── alkanes-integration.test.ts
│   │   ├── metashrew-indexing.test.ts
│   │   └── bitcoin-transactions.test.ts
│   └── database/
│       ├── postgres-operations.test.ts
│       └── redis-caching.test.ts
├── e2e/                         # End-to-end tests
│   ├── user-journeys/
│   │   ├── new-player-onboarding.spec.ts
│   │   ├── governor-interaction.spec.ts
│   │   ├── artifact-crafting.spec.ts
│   │   └── gambling-mechanics.spec.ts
│   ├── game-mechanics/
│   │   ├── energy-system.spec.ts
│   │   ├── reputation-tracking.spec.ts
│   │   └── watchtower-progression.spec.ts
│   └── cross-browser/
│       ├── chrome.spec.ts
│       ├── firefox.spec.ts
│       └── safari.spec.ts
├── performance/                 # Performance tests
│   ├── load-testing/
│   │   ├── api-load.test.ts
│   │   ├── frontend-perf.test.ts
│   │   └── blockchain-sync.test.ts
│   └── stress-testing/
│       ├── concurrent-users.test.ts
│       └── high-volume-tx.test.ts
├── security/                    # Security tests
│   ├── authentication.test.ts
│   ├── wallet-security.test.ts
│   ├── input-validation.test.ts
│   └── smart-contract-audit.test.ts
└── fixtures/                    # Test data fixtures
    ├── players/
    ├── governors/
    ├── artifacts/
    └── transactions/
```

## 🚀 Infrastructure & DevOps
```
infrastructure/
├── README.md                    # Infrastructure documentation
├── docker/                      # Docker configurations
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   ├── Dockerfile.indexer
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── docker-compose.prod.yml
├── kubernetes/                  # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmaps/
│   │   ├── frontend-config.yaml
│   │   ├── backend-config.yaml
│   │   └── indexer-config.yaml
│   ├── deployments/
│   │   ├── frontend-deployment.yaml
│   │   ├── backend-deployment.yaml
│   │   ├── indexer-deployment.yaml
│   │   └── postgres-deployment.yaml
│   ├── services/
│   │   ├── frontend-service.yaml
│   │   ├── backend-service.yaml
│   │   └── postgres-service.yaml
│   ├── ingress/
│   │   ├── frontend-ingress.yaml
│   │   └── api-ingress.yaml
│   └── secrets/
│       ├── api-keys.yaml
│       └── database-secrets.yaml
├── terraform/                   # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/
│   │   ├── networking/
│   │   ├── compute/
│   │   ├── storage/
│   │   ├── monitoring/
│   │   ├── cdn/                  # CDN & Asset Distribution
│   │   │   ├── cloudflare.tf
│   │   │   ├── aws-cloudfront.tf
│   │   │   ├── cache-rules.tf
│   │   │   └── ssl-certificates.tf
│   │   ├── secrets/              # Secrets Management
│   │   │   ├── vault.tf
│   │   │   ├── aws-secrets.tf
│   │   │   ├── k8s-secrets.tf
│   │   │   └── rotation.tf
│   │   └── security/             # Security Infrastructure
│   │       ├── waf.tf
│   │       ├── ddos-protection.tf
│   │       ├── security-groups.tf
│   │       └── audit-logging.tf
│   └── environments/
│       ├── development/
│       ├── staging/
│       └── production/
├── monitoring/                  # Monitoring & observability
│   ├── prometheus/
│   │   ├── config.yml
│   │   └── rules/
│   ├── grafana/
│   │   ├── dashboards/
│   │   │   ├── system-metrics.json
│   │   │   ├── api-performance.json
│   │   │   └── game-analytics.json
│   │   └── provisioning/
│   ├── alertmanager/
│   │   ├── config.yml
│   │   └── templates/
│   └── jaeger/
│       └── config.yml
├── nginx/                       # Reverse proxy configuration
│   ├── nginx.conf
│   ├── sites-available/
│   │   ├── frontend.conf
│   │   ├── api.conf
│   │   └── indexer.conf
│   └── ssl/
│       ├── certificates/
│       └── configs/
├── backup/                      # Backup strategies
│   ├── database/
│   │   ├── backup-script.sh
│   │   └── restore-script.sh
│   ├── assets/
│   │   └── sync-assets.sh
│   └── blockchain/
│       └── sync-state.sh
└── ci-cd/                      # CI/CD configurations
    ├── github-actions/
    │   ├── test.yml
    │   ├── build.yml
    │   ├── deploy.yml
    │   ├── security-scan.yml
    │   ├── smart-contract-audit.yml
    │   ├── accessibility-test.yml
    │   ├── visual-regression.yml
    │   ├── storybook-deploy.yml
    │   ├── i18n-validation.yml
    │   ├── dependency-update.yml
    │   ├── performance-test.yml
    │   ├── cdn-deploy.yml
    │   └── secrets-rotation.yml
    ├── gitlab-ci/
    │   ├── .gitlab-ci.yml
    │   ├── security-pipeline.yml
    │   ├── accessibility-pipeline.yml
    │   ├── storybook-pipeline.yml
    │   └── i18n-pipeline.yml
    ├── jenkins/
    │   ├── Jenkinsfile
    │   ├── security-pipeline.groovy
    │   ├── accessibility-pipeline.groovy
    │   └── deployment-pipeline.groovy
    └── workflows/
        ├── security/
        │   ├── smart-contract-audit.yml
        │   ├── dependency-scan.yml
        │   ├── code-security-scan.yml
        │   ├── container-scan.yml
        │   └── penetration-test.yml
        ├── quality/
        │   ├── accessibility-audit.yml
        │   ├── performance-audit.yml
        │   ├── visual-regression.yml
        │   └── code-quality.yml
        ├── deployment/
        │   ├── staging-deploy.yml
        │   ├── production-deploy.yml
        │   ├── rollback.yml
        │   ├── cdn-deploy.yml
        │   └── content-deploy.yml
        └── maintenance/
            ├── dependency-update.yml
            ├── security-patches.yml
            ├── cache-warming.yml
            └── health-checks.yml
```

## 📚 Documentation Structure
```
docs/
├── README.md                    # Main documentation index
├── game-design/                 # Game design documents
│   ├── mechanics.md
│   ├── governors.md
│   ├── artifacts.md
│   ├── enochian-system.md
│   └── progression.md
├── technical/                   # Technical documentation
│   ├── architecture.md
│   ├── api-reference.md
│   ├── smart-contracts.md
│   ├── blockchain-integration.md
│   └── security.md
├── user-guides/                 # User documentation
│   ├── getting-started.md
│   ├── wallet-setup.md
│   ├── gameplay.md
│   └── troubleshooting.md
├── developer/                   # Developer documentation
│   ├── setup.md
│   ├── contribution-guide.md
│   ├── coding-standards.md
│   ├── testing-guide.md
│   └── deployment.md
├── assets/                      # Documentation assets
│   ├── images/
│   ├── diagrams/
│   └── videos/
└── legal/                       # Legal documentation
    ├── terms-of-service.md
    ├── privacy-policy.md
    └── licenses/
``` 