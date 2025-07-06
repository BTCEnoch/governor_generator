/**
 * TypeScript interface for the unified knowledge index
 */

import { TraditionType } from './types';

export interface IndexStats {
  totalTraditions: number;
  totalConcepts: number;
  totalTeachings: number;
  totalFrameworks: number;
  totalPersonalityTraits: number;
  totalInteractionPatterns: number;
  extractionTimestamp: string;
}

export interface TraditionIndex {
  traditionName: string;
  displayName: string;
  overview: string;
  conceptCount: number;
  qualityRating: number;
  sourceCount: number;
  personalityTraits: string[];
  interactionPatterns: string[];
  coreConcepts: string[];
  wisdomTeachings: string[];
  decisionFrameworks: string[];
}

export interface UnifiedIndex {
  extractionSummary: IndexStats;
  traditions: Record<string, TraditionIndex>;
  indices: {
    personalityTraits: Record<string, string[]>;
    interactionPatterns: Record<string, string[]>;
    concepts: Record<string, string[]>;
    teachings: Record<string, string[]>;
    frameworks: Record<string, string[]>;
  };
}

export class UnifiedIndexService {
  private index: UnifiedIndex;
  
  constructor(indexPath: string) {
    this.index = require(indexPath);
  }
  
  /**
   * Get a tradition by name
   */
  getTradition(name: string): TraditionIndex | undefined {
    return this.index.traditions[name];
  }
  
  /**
   * Get all traditions that contain a specific trait
   */
  getTraditionsByTrait(trait: string): string[] {
    return this.index.indices.personalityTraits[trait] || [];
  }
  
  /**
   * Get all traditions that use a specific interaction pattern
   */
  getTraditionsByPattern(pattern: string): string[] {
    return this.index.indices.interactionPatterns[pattern] || [];
  }
  
  /**
   * Get all traditions that share a concept
   */
  getTraditionsByConcept(concept: string): string[] {
    return this.index.indices.concepts[concept] || [];
  }
  
  /**
   * Get all traditions that share a teaching
   */
  getTraditionsByTeaching(teaching: string): string[] {
    return this.index.indices.teachings[teaching] || [];
  }
  
  /**
   * Get all traditions that use a specific framework
   */
  getTraditionsByFramework(framework: string): string[] {
    return this.index.indices.frameworks[framework] || [];
  }
  
  /**
   * Get all traits for a tradition
   */
  getTraitsForTradition(traditionName: string): string[] {
    return this.index.traditions[traditionName]?.personalityTraits || [];
  }
  
  /**
   * Get all patterns for a tradition
   */
  getPatternsForTradition(traditionName: string): string[] {
    return this.index.traditions[traditionName]?.interactionPatterns || [];
  }
  
  /**
   * Get all concepts for a tradition
   */
  getConceptsForTradition(traditionName: string): string[] {
    return this.index.traditions[traditionName]?.coreConcepts || [];
  }
  
  /**
   * Get all teachings for a tradition
   */
  getTeachingsForTradition(traditionName: string): string[] {
    return this.index.traditions[traditionName]?.wisdomTeachings || [];
  }
  
  /**
   * Get all frameworks for a tradition
   */
  getFrameworksForTradition(traditionName: string): string[] {
    return this.index.traditions[traditionName]?.decisionFrameworks || [];
  }
  
  /**
   * Find traditions that match multiple criteria
   */
  findTraditions(criteria: {
    traits?: string[];
    patterns?: string[];
    concepts?: string[];
    teachings?: string[];
    frameworks?: string[];
  }): string[] {
    const matchingSets: Set<string>[] = [];
    
    if (criteria.traits) {
      criteria.traits.forEach(trait => {
        matchingSets.push(new Set(this.getTraditionsByTrait(trait)));
      });
    }
    
    if (criteria.patterns) {
      criteria.patterns.forEach(pattern => {
        matchingSets.push(new Set(this.getTraditionsByPattern(pattern)));
      });
    }
    
    if (criteria.concepts) {
      criteria.concepts.forEach(concept => {
        matchingSets.push(new Set(this.getTraditionsByConcept(concept)));
      });
    }
    
    if (criteria.teachings) {
      criteria.teachings.forEach(teaching => {
        matchingSets.push(new Set(this.getTraditionsByTeaching(teaching)));
      });
    }
    
    if (criteria.frameworks) {
      criteria.frameworks.forEach(framework => {
        matchingSets.push(new Set(this.getTraditionsByFramework(framework)));
      });
    }
    
    if (matchingSets.length === 0) {
      return Object.keys(this.index.traditions);
    }
    
    // Find intersection of all matching sets
    const intersection = [...matchingSets[0]].filter(tradition =>
      matchingSets.every(set => set.has(tradition))
    );
    
    return intersection;
  }
  
  /**
   * Get index statistics
   */
  getStats(): IndexStats {
    return this.index.extractionSummary;
  }
} 