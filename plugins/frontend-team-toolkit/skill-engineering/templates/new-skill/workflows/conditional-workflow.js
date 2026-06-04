/**
 * Conditional Routing Workflow Template
 *
 * Use this template when you need to route to different sub-skills
 * based on input conditions (Classify-and-Act pattern).
 *
 * Replace placeholders:
 * - {{SKILL_NAME}}: Your skill name
 * - {{INPUT_VAR}}: Input variable name
 * - {{STATUS_VAR}}: Status/condition variable name
 * - {{ROUTE_CONDITION_1}}: First routing condition
 * - {{ROUTE_CONDITION_2}}: Second routing condition
 * - {{AGENT_1_NAME}}: Agent for condition 1
 * - {{AGENT_2_NAME}}: Agent for condition 2
 */

async function conditionalWorkflow(args) {
  // Phase 1: Classify input condition
  const status = args.{{STATUS_VAR}} || "default";  // Default fallback

  // Phase 2: Route to appropriate agent based on condition
  let agentConfig;

  // Route mapping
  if (status === "{{ROUTE_CONDITION_1}}") {
    agentConfig = {
      name: "{{AGENT_1_NAME}}",
      model: "sonnet",
      tools: ["Read"]
    };
  } else if (status === "{{ROUTE_CONDITION_2}}") {
    agentConfig = {
      name: "{{AGENT_2_NAME}}",
      model: "sonnet",
      tools: ["Read"]
    };
  } else {
    // Default route (fallback)
    agentConfig = {
      name: "{{AGENT_1_NAME}}",  // Default to first agent
      model: "haiku",
      tools: ["Read"]
    };
  }

  // Phase 3: Execute routed agent
  const result = await runAgent({
    ...agentConfig,
    prompt: `Read ${args.{{INPUT_VAR}}}, execute ${agentConfig.name}`,
    worktree: false
  });

  // Phase 4: Return result with routing info
  return {
    routedTo: agentConfig.name,
    condition: status,
    result: result,
    status: result.status
  };
}

/**
 * Helper: Validate routing conditions
 */
function validateRoutingConditions(status, validConditions) {
  if (!validConditions.includes(status)) {
    console.warn(`Unknown condition: ${status}, using default route`);
    return "default";
  }
  return status;
}

// Export: Claude Code runtime calls this with args
module.exports = conditionalWorkflow(args);