import { Logger, LogLevel } from '../src/core/utils/logger';
import { KnowledgeService } from '../src/core/knowledge-base/knowledge-service';
import { DialogService } from '../src/core/dialog-engine/dialog-service';
import { GameService } from '../src/core/game-loops/game-service';
import * as dotenv from 'dotenv';

async function main() {
  try {
    // Load environment variables
    dotenv.config();

    console.log('🌟 Starting Enochian Governor Generation System...');

    // Initialize logger
    const logger = new Logger('main', LogLevel.INFO);
    logger.info('Initializing services...');

    // Initialize services
    const knowledgeService = new KnowledgeService(
      new Logger('knowledge', LogLevel.INFO)
    );

    const dialogService = new DialogService(
      new Logger('dialog', LogLevel.INFO),
      knowledgeService
    );

    // Initialize game service - will be used by API server (TODO)
    const gameService = new GameService(
      new Logger('game', LogLevel.INFO),
      dialogService,
      knowledgeService
    );

    // Export services for API server
    global.services = {
      knowledgeService,
      dialogService,
      gameService
    };

    // Start services
    logger.info('Services initialized successfully');
    logger.info('System is ready to process requests');

    // Keep the process running
    process.on('SIGINT', () => {
      logger.info('Shutting down...');
      process.exit(0);
    });

    process.on('SIGTERM', () => {
      logger.info('Shutting down...');
      process.exit(0);
    });

    // TODO: Add API server initialization here
    // TODO: Add P2P network initialization here
    // TODO: Add blockchain connection here

  } catch (error) {
    console.error('❌ Failed to start system:', error);
    process.exit(1);
  }
}

main(); 