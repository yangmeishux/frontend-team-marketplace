// weekly-regression.js
// Workflows script for weekly automated regression using Claude Code `/loop`

/**
 * Weekly Regression Workflow
 *
 * Purpose: Run weekly regression for a skill, report issues if found.
 * Trigger: Claude Code `/loop weekly` command
 *
 * Usage:
 *   /loop weekly 用 workflows/weekly-regression.js 回归 wechat-article-review Skill
 */

async function weeklyRegression(args) {
  const skillName = args.skill || "wechat-article-review";
  const riskFilter = args.risk || "high,medium";

  console.log(`Starting weekly regression for ${skillName}...`);
  console.log(`Risk filter: ${riskFilter}`);

  // Phase 1: Run Eval with risk=high + medium
  const evalResults = await runAgent({
    name: "eval-runner",
    prompt: `跑 ${skillName} 的 risk=${riskFilter} Eval，输出 results.tsv 格式结果`,
    tools: ["Read", "Bash", "Write"],
    model: "sonnet",
    context: {
      skill_path: `plugins/frontend-team-toolkit/skills/${skillName}`,
      evals_path: `plugins/frontend-team-toolkit/skills/${skillName}/evals/evals.json`
    }
  });

  // Phase 2: Parse results and check regression
  const regressionFailed = evalResults.filter(
    result => result.type === "regression" &&
              result.risk === "high" &&
              result.pass === false
  );

  // Phase 3: Report or record
  if (regressionFailed.length > 0) {
    console.log(`❌ Found ${regressionFailed.length} regression failures`);

    // Log each failure
    regressionFailed.forEach(failure => {
      console.log(`  - ${failure.eval_id}: ${failure.reason}`);
    });

    // Return issue report for Claude Code to notify
    return {
      status: "REGRESSION_FOUND",
      skill: skillName,
      issues: regressionFailed,
      timestamp: new Date().toISOString(),
      action: "报警",
      message: `发现 ${regressionFailed.length} 个 regression 失败，请检查并修复`
    };
  } else {
    console.log("✅ All regression Evals passed");

    return {
      status: "ALL_PASS",
      skill: skillName,
      timestamp: new Date().toISOString(),
      action: "记录",
      message: "全量回归通过"
    };
  }
}

// Export for Claude Code workflows runtime
module.exports = weeklyRegression;

/**
 * Expected args:
 * {
 *   skill: "wechat-article-review",  // Skill name
 *   risk: "high,medium",             // Risk filter (optional)
 *   maxIterations: 10                // Max iterations for loop (optional)
 * }
 *
 * Expected return:
 * {
 *   status: "REGRESSION_FOUND" | "ALL_PASS",
 *   skill: string,
 *   issues: Array,      // If REGRESSION_FOUND
 *   timestamp: string,
 *   action: "报警" | "记录",
 *   message: string
 * }
 */