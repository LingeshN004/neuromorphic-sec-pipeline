const mcServer = require('flying-squid');

mcServer.createMCServer({
  port: 25565,
  'max-players': 10,
  'online-mode': false,
  gameMode: 1, // Creative mode
  difficulty: 0, // Peaceful
  worldFolder: 'world',
  generation: {
    name: 'superflat',
    bottomY: 0,
    options: {
      layers: [
        { block: 'bedrock', count: 1 },
        { block: 'dirt', count: 2 },
        { block: 'grass_block', count: 1 }
      ]
    }
  },
  kickTimeout: 10000,
  logging: true
});

console.log('[*] Headless Minecraft Server listening on 127.0.0.1:25565');
