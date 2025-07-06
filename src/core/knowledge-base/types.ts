import { BlockchainMetadata } from '../blockchain/types';

export type TraditionType = 
  | 'enochian'
  | 'kabbalah'
  | 'hermeticism'
  | 'alchemy'
  | 'tarot'
  | 'astrology'
  | 'numerology'
  | 'gematria'
  | 'sacred_geometry'
  | 'egyptian'
  | 'greek'
  | 'celtic'
  | 'norse'
  | 'vedic'
  | 'buddhist'
  | 'taoism'
  | 'sufism'
  | 'shamanic';

export interface Reference {
  source: string;
  type: 'academic' | 'primary' | 'historical';
  citation: string;
  url?: string;
}

export interface KnowledgeEntry {
  id: string;
  tradition: TraditionType;
  title: string;
  content: string;
  tags: string[];
  references: Reference[];
  crossReferences: string[];
  lastModified: number;
  version: number;
  blockchainMetadata?: BlockchainMetadata;
}

export interface KnowledgeIndex {
  byTradition: Map<TraditionType, string[]>;
  byTag: Map<string, string[]>;
  byReference: Map<string, string[]>;
  crossRefGraph: Map<string, string[]>;
}

export interface SearchOptions {
  tradition?: TraditionType;
  tags?: string[];
  offset?: number;
  limit?: number;
  includeContent?: boolean;
}

export interface SearchResult {
  entries: KnowledgeEntry[];
  total: number;
  hasMore: boolean;
}

export enum ValidationErrorCode {
  CONTENT_LENGTH = 'CONTENT_LENGTH',
  INSUFFICIENT_TAGS = 'INSUFFICIENT_TAGS',
  INVALID_REFERENCE = 'INVALID_REFERENCE',
  INVALID_CROSS_REF = 'INVALID_CROSS_REF',
  CULTURAL_SENSITIVITY = 'CULTURAL_SENSITIVITY'
}

export interface ValidationError {
  field: string;
  message: string;
  code: ValidationErrorCode;
}

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
}

export interface KnowledgeStats {
  totalEntries: number;
  entriesByTradition: Map<TraditionType, number>;
  totalTags: number;
  popularTags: Array<{
    tag: string;
    count: number;
  }>;
} 