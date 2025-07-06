export interface BlockchainMetadata {
  inscriptionId: string;
  inscriptionNumber: number;
  blockHeight: number;
  timestamp: number;
  txid: string;
  vout: number;
  contentType: string;
  contentHash: string;
  size: number;
}

export interface TapscriptMetadata {
  tapLeafHash: string;
  controlBlock: string;
  scriptPubKey: string;
  internalKey: string;
}

export interface AssetMetadata extends BlockchainMetadata {
  tapMetadata: TapscriptMetadata;
  assetType: 'governor' | 'artifact' | 'knowledge' | 'questline';
  version: number;
  dependencies?: string[]; // Other inscription IDs this asset depends on
} 