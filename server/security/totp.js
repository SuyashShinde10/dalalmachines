const crypto = require('crypto');

/**
 * Dalal Machine Tools Agency Pvt. Ltd. - Master Executive 2FA / TOTP Security Engine
 * Zero-dependency RFC 6238 Standard Implementation (HMAC-SHA1, 30s step, 6 digits)
 * Compatible with Google Authenticator, Microsoft Authenticator, Authy, Apple Keychain
 */

function base32Encode(buffer) {
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
  let bits = 0;
  let value = 0;
  let output = '';
  for (let i = 0; i < buffer.length; i++) {
    value = (value << 8) | buffer[i];
    bits += 8;
    while (bits >= 5) {
      output += alphabet[(value >>> (bits - 5)) & 31];
      bits -= 5;
    }
  }
  if (bits > 0) {
    output += alphabet[(value << (5 - bits)) & 31];
  }
  return output;
}

function base32Decode(str) {
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
  let bits = 0;
  let value = 0;
  let output = [];
  const cleanStr = (str || '').replace(/=+$/, '').toUpperCase().replace(/\s+/g, '');
  for (let i = 0; i < cleanStr.length; i++) {
    const idx = alphabet.indexOf(cleanStr[i]);
    if (idx === -1) continue;
    value = (value << 5) | idx;
    bits += 5;
    if (bits >= 8) {
      output.push((value >>> (bits - 8)) & 255);
      bits -= 8;
    }
  }
  return Buffer.from(output);
}

function generateSecret(username = 'superadmin', issuer = 'Dalal Machine Tools') {
  const secretBytes = crypto.randomBytes(20);
  const secret = base32Encode(secretBytes);
  const cleanIssuer = encodeURIComponent(issuer);
  const cleanUser = encodeURIComponent(username);
  const uri = `otpauth://totp/${cleanIssuer}:${cleanUser}?secret=${secret}&issuer=${cleanIssuer}&algorithm=SHA1&digits=6&period=30`;
  const recoveryCode = 'DMTA-REC-' + crypto.randomBytes(4).toString('hex').toUpperCase() + '-' + crypto.randomBytes(4).toString('hex').toUpperCase();

  // QR Code URL using Google Chart API for 1-click scanning in Authenticator apps
  const qrUrl = `https://chart.googleapis.com/chart?chs=220x220&chld=M|0&cht=qr&chl=${encodeURIComponent(uri)}`;

  return {
    secret,
    uri,
    qrUrl,
    recoveryCode
  };
}

function generateTotp(secret, timeStep = 30) {
  const key = base32Decode(secret);
  const epoch = Math.floor(Date.now() / 1000);
  const counter = Math.floor(epoch / timeStep);
  const buf = Buffer.alloc(8);
  buf.writeBigInt64BE(BigInt(counter));

  const hmac = crypto.createHmac('sha1', key).update(buf).digest();
  const offset = hmac[hmac.length - 1] & 0x0f;
  const binary = ((hmac[offset] & 0x7f) << 24) |
                 ((hmac[offset + 1] & 0xff) << 16) |
                 ((hmac[offset + 2] & 0xff) << 8) |
                 (hmac[offset + 3] & 0xff);
  return (binary % 1000000).toString().padStart(6, '0');
}

function verifyTotp(secret, token, window = 1, timeStep = 30) {
  if (!secret || !token) return false;
  const cleanToken = String(token).trim();
  if (cleanToken.length !== 6) return false;

  const key = base32Decode(secret);
  const epoch = Math.floor(Date.now() / 1000);
  const currentCounter = Math.floor(epoch / timeStep);

  for (let i = -window; i <= window; i++) {
    const counter = currentCounter + i;
    const buf = Buffer.alloc(8);
    buf.writeBigInt64BE(BigInt(counter));
    const hmac = crypto.createHmac('sha1', key).update(buf).digest();
    const offset = hmac[hmac.length - 1] & 0x0f;
    const binary = ((hmac[offset] & 0x7f) << 24) |
                   ((hmac[offset + 1] & 0xff) << 16) |
                   ((hmac[offset + 2] & 0xff) << 8) |
                   (hmac[offset + 3] & 0xff);
    const otp = (binary % 1000000).toString().padStart(6, '0');
    if (otp === cleanToken) return true;
  }
  return false;
}

module.exports = {
  generateSecret,
  generateTotp,
  verifyTotp,
  base32Encode,
  base32Decode
};
