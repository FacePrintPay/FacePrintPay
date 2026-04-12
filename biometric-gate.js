// biometric-gate.js
// Sovereign auth gate — binds session to device fingerprint
// Usage: import { requireBiometric } from './lib/biometric-gate'

export const requireBiometric = async () => {
  // In real Termux: call termux-fingerprint API
  // For web demo: simulate with localStorage oath
  const oath = localStorage.getItem('sovereign_oath');
  if (!oath) {
    alert("🔒 Biometric authentication required");
    // In production: window.location.href = '/auth/fingerprint';
    localStorage.setItem('sovereign_oath', 'granted_' + Date.now());
  }
  return true;
};
