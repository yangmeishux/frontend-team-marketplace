/**
 * Serial Workflow Template
 *
 * Use this template when sub-skills have sequential dependencies.
 * Phase 2 depends on Phase 1 output.
 *
 * Replace placeholders:
 * - {{SKILL_NAME}}: Your skill name
 * - {{PHASE_1_NAME}}: First sub-skill/phase name
 * - {{PHASE_2_NAME}}: Second sub-skill/phase name
 * - {{INPUT_VAR}}: Input variable name
 */

async function serialWorkflow(args) {
  // Phase 1: First sub-skill execution
  const phase1Result = await runAgent({
    name: "{{PHASE_1_NAME}}",
    prompt: `Read ${args.{{INPUT_VAR}}}, execute {{PHASE_1_NAME}}`,
    tools: ["Read", "Write"],  // Adjust tools as needed
    model: "sonnet",           // Adjust model as needed
    worktree: false            // false = shared context, true = isolated
  });

  // Phase 2: Second sub-skill (depends on Phase 1)
  const phase2Result = await runAgent({
    name: "{{PHASE_2_NAME}}",
    prompt: `Read ${phase1Result.outputPath}, execute {{PHASE_2_NAME}}`,
    tools: ["Read", "Write"],
    model: "sonnet",
    worktree: false
  });

  // Phase 3: Synthesize results
  return {
    phase1: phase1Result,
    phase2: phase2Result,
    summary: synthesizeResults([phase1Result, phase2Result]),
    status: "COMPLETE"
  };
}

/**
 * Helper: Synthesize results from multiple phases
 */
function synthesizeResults(results) {
  return {
    outputs: results.map(r => r.output),
    combined: results.every(r => r.status === "PASS") ? "PASS" : "FAIL"
  };
}

// Export: Claude Code runtime calls this with args
module.exports = serialWorkflow(args);