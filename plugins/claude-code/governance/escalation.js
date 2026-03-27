'use strict';

/**
 * AEGIS Claude Code Plugin — escalation.js
 *
 * Handles ESCALATE and REQUIRE_CONFIRMATION decisions by prompting the
 * human operator directly via the TTY. The Tool Proxy owns the entire
 * escalation lifecycle — Claude Code never sees "ask".
 *
 * On Unix:    opens /dev/tty for direct terminal I/O
 * On Windows: opens CON (cmd) or /dev/tty (Git Bash / MSYS2)
 *
 * If the TTY is unavailable (non-interactive environment, piped session),
 * escalation defaults to DENY. Silent fail-open is not permitted.
 */

const fs       = require('fs');
const readline = require('readline');

/**
 * Attempt to open a readable+writable handle to the operator's terminal,
 * bypassing stdin/stdout which are piped to Claude Code.
 *
 * @returns {{ input: fs.ReadStream, output: fs.WriteStream }|null}
 */
function openTTY() {
  // Try platform-appropriate paths in order
  const candidates = process.platform === 'win32'
    ? ['CON', '\\\\.\\CON', 'CONIN$', '/dev/tty']
    : ['/dev/tty'];

  for (const candidate of candidates) {
    try {
      const fd = fs.openSync(candidate, 'r+');
      return {
        input:  new fs.ReadStream(null, { fd: fd, autoClose: false }),
        output: new fs.WriteStream(null, { fd: fd, autoClose: false }),
        fd:     fd,
      };
    } catch (_) {
      // Try next candidate
    }
  }

  return null;
}

/**
 * Prompt the operator for an escalation or confirmation decision.
 *
 * @param {string} decision       AGP-1 decision: "escalate" or "require_confirmation"
 * @param {string} toolName       The tool being governed
 * @param {string} inputSummary   Short description of the proposed action
 * @param {string} reason         Evaluator's reason string
 * @returns {Promise<string>}     Resolved decision: "allow" or "deny"
 */
function promptOperator(decision, toolName, inputSummary, reason) {
  return new Promise(function(resolve) {
    const tty = openTTY();

    if (!tty) {
      // No TTY available — default to deny (fail-closed)
      process.stderr.write(
        '[AEGIS] WARNING: Escalation required but no TTY available. Defaulting to DENY.\n'
      );
      resolve('deny');
      return;
    }

    const label = decision === 'require_confirmation'
      ? 'AEGIS CONFIRMATION REQUIRED'
      : 'AEGIS ESCALATION';

    const rl = readline.createInterface({
      input:  tty.input,
      output: tty.output,
    });

    tty.output.write('\n');
    tty.output.write('╔══════════════════════════════════════════════════════════╗\n');
    tty.output.write('║  ' + label.padEnd(55) + '║\n');
    tty.output.write('╠══════════════════════════════════════════════════════════╣\n');
    tty.output.write('║  Tool:   ' + toolName.padEnd(47) + '║\n');
    tty.output.write('║  Action: ' + inputSummary.slice(0, 47).padEnd(47) + '║\n');
    tty.output.write('║  Reason: ' + reason.slice(0, 47).padEnd(47) + '║\n');
    tty.output.write('╚══════════════════════════════════════════════════════════╝\n');

    rl.question('[AEGIS] Allow or deny? (a/d): ', function(answer) {
      rl.close();
      try { fs.closeSync(tty.fd); } catch (_) { /* ignore */ }

      const normalized = (answer || '').trim().toLowerCase();
      if (normalized === 'a' || normalized === 'allow') {
        resolve('allow');
      } else {
        // Anything other than explicit allow = deny (fail-closed)
        resolve('deny');
      }
    });
  });
}

module.exports = { promptOperator };
