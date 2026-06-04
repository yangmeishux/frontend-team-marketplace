/**
 * Adversarial Verification Workflow Template
 *
 * Use this template for quality assurance: spawn an agent to execute,
 * then spawn another agent to adversarially verify its output.
 *
 * Replace placeholders:
 * - {{SKILL_NAME}}: Your skill name
 * - {{EXECUTOR_NAME}}: Executor agent name
 * - {{VERIFIER_NAME}}: Verifier agent name
 * - {{INPUT_VAR}}: Input variable name
 * - {{RUBRIC_PATH}}: Verification rubric path
 */

async function adversarialWorkflow(args) {
  // Phase 1: Executor agent performs task
  const executorResult = await runAgent({
    name: "{{EXECUTOR_NAME}}",
    prompt: `Read ${args.{{INPUT_VAR}}}, execute task`,
    tools: ["Read", "Write"],
    model: "sonnet",
    worktree: false
  });

  // Phase 2: Verifier agent adversarially checks output
  const verifierResult = await runAgent({
    name: "{{VERIFIER_NAME}}",
    prompt: `Read ${executorResult.outputPath}, adversarially verify against rubric at {{RUBRIC_PATH}}`,
    tools: ["Read"],
    model: "sonnet",
    worktree: true  // Isolated context for independent verification
  });

  // Phase 3: Judge result
  const passed = verifierResult.status === "PASS";

  // Phase 4: Return with verification status
  return {
    executorOutput: executorResult,
    verifierOutput: verifierResult,
    passed,
    status: passed ? "VERIFIED_PASS" : "VERIFIED_FAIL",
    // If failed, include issues for fixing
    issues: passed ? [] : verifierResult.issues
  };
}

/**
 * Helper: Extract issues from verifier output
 */
function extractIssues(verifierResult) {
  return verifierResult.issues || verifierResult.errors || [];
}

// Export: Claude Code runtime calls this with args
module.exports = adversarialWorkflow(args);