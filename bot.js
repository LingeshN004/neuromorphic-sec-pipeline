const mineflayer = require('mineflayer');
const dgram = require('dgram');
const crypto = require('crypto');

// Configuration matching engine.py
const UDP_HOST = '127.0.0.1';
const UDP_PORT = 5005;
const SECRET_KEY = 'neurocraft_super_secret_capstone_key_2026';
const MAX_RAY_DIST = 16.0;

const udpClient = dgram.createSocket('udp4');

const bot = mineflayer.createBot({
  host: '172.21.112.1',
  port: 25565,
  username: 'FlyBrainBot'
});

// Canonical serializer for Python json.dumps(data, sort_keys=True)
function canonicalJson(data) {
  const sortedKeys = Object.keys(data).sort();
  const pairs = sortedKeys.map(k => `"${k}": ${Number(data[k])}`);
  return `{${pairs.join(', ')}}`;
}

function signPacket(data) {
  const serialized = canonicalJson(data);
  const hmac = crypto.createHmac('sha256', SECRET_KEY);
  hmac.update(serialized);
  return {
    data: data,
    signature: hmac.digest('hex')
  };
}

// Raycasting: Measures line-of-sight distance to solid blocks AND mobs
function getDistanceInDirection(angleOffsetRad) {
  if (!bot.entity) return MAX_RAY_DIST;

  const footPos = bot.entity.position.offset(0, 0.2, 0);
  const eyePos = bot.entity.position.offset(0, bot.entity.height, 0);
  const targetYaw = bot.entity.yaw + angleOffsetRad;
  const dx = -Math.sin(targetYaw);
  const dz = -Math.cos(targetYaw);

  for (let dist = 0.5; dist <= MAX_RAY_DIST; dist += 0.5) {
    const checkFoot = footPos.offset(dx * dist, 0, dz * dist);
    const checkEye = eyePos.offset(dx * dist, 0, dz * dist);

    const blockFoot = bot.blockAt(checkFoot);
    const blockEye = bot.blockAt(checkEye);

    const isSolid = (b) => b && b.boundingBox === 'block';

    if (isSolid(blockFoot) || isSolid(blockEye)) {
      return parseFloat(dist.toFixed(1));
    }

    // Entity collision checks along the ray
    for (const id of Object.keys(bot.entities)) {
      const e = bot.entities[id];
      if (!e || e === bot.entity) continue;
      if (e.type !== 'mob' && e.type !== 'player') continue;

      const mobMid = e.position.offset(0, (e.height || 1.8) * 0.5, 0);
      if (mobMid.distanceTo(checkEye) < 1.6 || mobMid.distanceTo(checkFoot) < 1.6) {
        return parseFloat(dist.toFixed(1));
      }
    }
  }
  return MAX_RAY_DIST;
}

// Check vertical height of obstacle directly ahead
function getObstacleAheadType() {
  if (!bot.entity) return 'CLEAR';

  const dx = -Math.sin(bot.entity.yaw);
  const dz = -Math.cos(bot.entity.yaw);

  const footCheck = bot.entity.position.offset(dx * 1.0, 0.2, dz * 1.0);
  const waistCheck = bot.entity.position.offset(dx * 1.0, 1.2, dz * 1.0);
  const headCheck = bot.entity.position.offset(dx * 1.0, 2.0, dz * 1.0);

  const isSolid = (pos) => {
    const b = bot.blockAt(pos);
    return b && b.boundingBox === 'block';
  };

  const footSolid = isSolid(footCheck);
  const waistSolid = isSolid(waistCheck);
  const headSolid = isSolid(headCheck);

  if (waistSolid || headSolid) return 'WALL'; // 2+ block tall wall (unjumpable)
  if (footSolid) return 'STEP';               // 1-block elevation (jumpable)
  return 'CLEAR';
}

let prevTelemetry = null;
const MAX_DELTA = 2.0;
let isEscaping = false;

bot.on('spawn', () => {
  console.log('[*] FlyBrainBot spawned. Starting autonomous control systems...');

  // Telemetry loop to Python connectome
  setInterval(() => {
    const rawLeft = getDistanceInDirection(Math.PI / 4);
    const rawFront = getDistanceInDirection(0);
    const rawRight = getDistanceInDirection(-Math.PI / 4);

    if (!prevTelemetry) {
      prevTelemetry = { front: rawFront, left: rawLeft, right: rawRight };
    }

    const smooth = (curr, prev) => {
      const diff = curr - prev;
      if (Math.abs(diff) > MAX_DELTA) {
        return parseFloat((prev + Math.sign(diff) * MAX_DELTA).toFixed(1));
      }
      return parseFloat(curr.toFixed(1));
    };

    const telemetry = {
      front: smooth(rawFront, prevTelemetry.front),
      left: smooth(rawLeft, prevTelemetry.left),
      right: smooth(rawRight, prevTelemetry.right)
    };

    prevTelemetry = telemetry;

    const signedPacket = signPacket(telemetry);
    const message = Buffer.from(JSON.stringify(signedPacket));

    udpClient.send(message, UDP_PORT, UDP_HOST, (err) => {
      if (err) console.error('[!] UDP error:', err);
    });
  }, 100);
});

// Proactive Combat: Attacks hostiles in range before taking damage
setInterval(() => {
  if (isEscaping || !bot.entity) return;

  const hostile = bot.nearestEntity((e) => {
    if (!e || e === bot.entity) return false;
    if (e.type !== 'mob') return false;
    const name = e.name ? e.name.toLowerCase() : '';
    return name.includes('zombie') || name.includes('skeleton') || 
           name.includes('spider') || name.includes('creeper') || 
           name.includes('pillager') || name.includes('vindicator');
  });

  if (hostile && bot.entity.position.distanceTo(hostile.position) <= 3.2) {
    bot.lookAt(hostile.position.offset(0, hostile.height * 0.8, 0), true);
    bot.attack(hostile);

    // If too close, step back while attacking to create spacing
    if (bot.entity.position.distanceTo(hostile.position) < 1.8) {
      bot.setControlState('forward', false);
      bot.setControlState('back', true);
      setTimeout(() => bot.setControlState('back', false), 250);
    }
  }
}, 250);

// Active Unstuck Routine: Detects movement stall and forces pivot
let lastPos = null;
let stallCount = 0;

setInterval(() => {
  if (!bot.entity || isEscaping) return;

  const currentPos = bot.entity.position;
  if (lastPos && currentPos.distanceTo(lastPos) < 0.15) {
    stallCount++;
  } else {
    stallCount = 0;
  }
  lastPos = currentPos.clone();

  // If stationary for > 1.2 seconds, trigger escape maneuver
  if (stallCount >= 3) {
    isEscaping = true;
    stallCount = 0;

    bot.clearControlStates();
    bot.setControlState('back', true);
    bot.setControlState('jump', true);

    // Turn toward whichever flank has more clearance
    const leftDist = getDistanceInDirection(Math.PI / 2);
    const rightDist = getDistanceInDirection(-Math.PI / 2);
    const escapeYaw = bot.entity.yaw + (leftDist >= rightDist ? 2.0 : -2.0);
    bot.look(escapeYaw, 0, true);

    setTimeout(() => {
      bot.clearControlStates();
      isEscaping = false;
    }, 700);
  }
}, 400);

// Process Neuromorphic Steering Commands
udpClient.on('message', (msg) => {
  if (isEscaping) return;

  try {
    const cmd = JSON.parse(msg.toString());

    if (cmd.status === 'ACCEPTED') {
      // 1. Apply angular steering from Python
      const yawDeltaRad = (cmd.yaw * Math.PI) / 180;
      const newYaw = bot.entity.yaw + yawDeltaRad;
      bot.look(newYaw, bot.entity.pitch, true);

      // 2. Evaluate obstacle height directly ahead
      const obstacle = getObstacleAheadType();

      if (obstacle === 'WALL') {
        // High wall: Halt forward thrust so the Python yaw can rotate the bot away
        bot.setControlState('forward', false);
        bot.setControlState('jump', false);
      } else if (obstacle === 'STEP') {
        // 1-block ledge: Jump and move forward
        bot.setControlState('forward', true);
        bot.setControlState('jump', true);
        bot.setControlState('sprint', false);
      } else {
        // Open terrain: Full forward drive
        bot.setControlState('forward', true);
        bot.setControlState('jump', false);
        bot.setControlState('sprint', cmd.thrust > 0.5);
      }
    } else {
      bot.clearControlStates();
    }
  } catch (err) {
    console.error('[!] Failed to parse command packet:', err);
  }
});

bot.on('kicked', console.log);
bot.on('error', console.log);