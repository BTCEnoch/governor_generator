import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as dotenv from 'dotenv';

const execAsync = promisify(exec);

async function main() {
  try {
    // Load environment variables
    dotenv.config();

    console.log('🚀 Starting deployment...');

    // Check prerequisites
    console.log('📋 Checking prerequisites...');
    
    const nodeVersion = process.version;
    if (!nodeVersion.startsWith('v18')) {
      throw new Error('Node.js 18+ is required');
    }

    // Clean previous build
    console.log('🧹 Cleaning previous build...');
    await execAsync('npm run clean');

    // Install dependencies
    console.log('📦 Installing dependencies...');
    await execAsync('npm install');

    // Run tests
    console.log('🧪 Running tests...');
    await execAsync('npm run test');

    // Build project
    console.log('🔨 Building project...');
    await execAsync('npm run build');

    // Check Bitcoin node connection
    console.log('⛓️ Checking Bitcoin node connection...');
    if (!process.env.BITCOIN_NODE_URL) {
      throw new Error('BITCOIN_NODE_URL environment variable is required');
    }

    // Create required directories
    console.log('📁 Creating required directories...');
    const dirs = [
      'dist/knowledge-base',
      'dist/game-loops',
      'dist/dialog-engine',
      'dist/blockchain',
      'dist/utils'
    ];

    for (const dir of dirs) {
      await fs.mkdir(path.join(process.cwd(), dir), { recursive: true });
    }

    // Copy configuration files
    console.log('📝 Copying configuration files...');
    await fs.copyFile('.env', 'dist/.env');
    await fs.copyFile('package.json', 'dist/package.json');
    await fs.copyFile('README.md', 'dist/README.md');

    // Start services
    console.log('🌟 Starting services...');
    await execAsync('npm start');

    console.log('✨ Deployment complete!');
  } catch (error) {
    console.error('❌ Deployment failed:', error);
    process.exit(1);
  }
}

main(); 