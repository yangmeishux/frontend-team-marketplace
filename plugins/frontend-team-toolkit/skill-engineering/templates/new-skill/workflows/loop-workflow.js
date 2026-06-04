/**
 * Loop Until Done Workflow Template
 *
 * Use this template for tasks with unknown amount of work.
 * Loops until stop condition is met or max iterations reached.
 *
 * Replace placeholders:
 * - {{SKILL_NAME}}: Your skill name
 * - {{STOP_CONDITION}}: Stop condition description
 * - {{MAX_ITERATIONS}}: Maximum iterations (default 10)
 */

async function loopWorkflow(args) {
  const maxIterations = args.maxIterations || {{MAX_ITERATIONS}};
  let iteration = 0;
  let stopConditionMet = false;
  let results = [];

  // Loop until stop condition or max iterations
  while (iteration < maxIterations && !stopConditionMet) {
    // Phase 1: Run agent for this iteration
    const iterationResult = await runAgent({
      name: "{{SKILL_NAME}}-worker",
      prompt: `Iteration ${iteration}: Execute task, check {{STOP_CONDITION}}`,
      tools: ["Read", "Bash"],
      model: "sonnet",
      worktree: true
    });

    // Phase 2: Check stop condition
    stopConditionMet = checkStopCondition(iterationResult);

    // Phase 3: Record result
    results.push({
      iteration,
      result: iterationResult,
      stopConditionMet,
      timestamp: new Date().toISOString()
    });

    iteration++;

    // Optional: Wait between iterations
    if (!stopConditionMet && iteration < maxIterations) {
      await sleep(60000);  // Wait 1 minute
    }
  }

  // Phase 4: Return loop summary
  return {
    totalIterations: iteration,
    stopConditionMet,
    results,
    finalStatus: stopConditionMet ? "CONDITION_MET" : "MAX_ITERATIONS_REACHED"
  };
}

/**
 * Helper: Check if stop condition is met
 */
function checkStopCondition(result) {
  // Replace with your actual stop condition logic
  // Example: Check if all evals pass
  return result.status === "PASS" && result.errors === 0;
}

/**
 * Helper: Sleep between iterations
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Export: Claude Code runtime calls this with args
module.exports = loopWorkflow(args);