/**
 * Parallel Workflow Template
 *
 * Use this template when sub-skills have NO dependencies.
 * Both agents run simultaneously, then results are synthesized.
 *
 * Replace placeholders:
 * - {{SKILL_NAME}}: Your skill name
 * - {{AGENT_1_NAME}}: First agent/sub-skill name
 * - {{AGENT_2_NAME}}: Second agent/sub-skill name
 * - {{INPUT_VAR}}: Input variable name
 */

async function parallelWorkflow(args) {
  // Fan-out: Spawn multiple agents in parallel
  const [agent1Result, agent2Result] = await Promise.all([
    runAgent({
      name: "{{AGENT_1_NAME}}",
      prompt: `Read ${args.{{INPUT_VAR}}}, execute {{AGENT_1_NAME}}`,
      tools: ["Read"],
      model: "sonnet",
      worktree: true   // IMPORTANT: Use worktree for parallel execution
    }),
    runAgent({
      name: "{{AGENT_2_NAME}}",
      prompt: `Read ${args.{{INPUT_VAR}}}, execute {{AGENT_2_NAME}}`,
      tools: ["Read"],
      model: "haiku",  // Can use cheaper model for simpler tasks
      worktree: true
    })
  ]);

  // Barrier: Wait for all agents, then synthesize
  return synthesizeParallelResults([agent1Result, agent2Result]);
}

/**
 * Helper: Synthesize results from parallel agents
 */
function synthesizeParallelResults(results) {
  // Check if all agents passed
  const allPassed = results.every(r => r.status === "PASS");

  // Combine outputs
  return {
    agents: results.map(r => ({
      name: r.name,
      status: r.status,
      output: r.output
    })),
    combinedStatus: allPassed ? "PASS" : "FAIL",
    summary: `Parallel execution: ${results.length} agents, ${results.filter(r => r.status === "PASS").length} passed`
  };
}

// Export: Claude Code runtime calls this with args
module.exports = parallelWorkflow(args);