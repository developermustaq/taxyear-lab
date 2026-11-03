// MCP server (stdio) with one tool: the official start and end dates of a UK tax year.
// stdout carries the MCP protocol, so diagnostics go to stderr only.

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "tax-calendar", version: "1.0.0" });

server.registerTool(
  "get_tax_year_dates",
  {
    title: "Get tax year dates",
    description: "Return the first and last day of a UK tax year, given its start year (for example 2025 for 2025/26).",
    inputSchema: { startYear: z.number().int().min(2000).max(2100) },
    annotations: { readOnlyHint: true },
  },
  async ({ startYear }) => {
    const end = String((startYear + 1) % 100).padStart(2, "0");
    const dates = {
      taxYear: `${startYear}/${end}`,
      firstDay: `${startYear}-04-06`,
      lastDay: `${startYear + 1}-04-05`,
    };
    return { content: [{ type: "text", text: JSON.stringify(dates, null, 2) }] };
  },
);

await server.connect(new StdioServerTransport());
console.error("tax-calendar MCP server running on stdio");
