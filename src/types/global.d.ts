import { KnowledgeService } from '../core/knowledge-base/knowledge-service';
import { DialogService } from '../core/dialog-engine/dialog-service';
import { GameService } from '../core/game-loops/game-service';

declare global {
  var services: {
    knowledgeService: KnowledgeService;
    dialogService: DialogService;
    gameService: GameService;
  };
} 