# AI Usage Documentation

## Overview

AI tools were used as development assistants during the project, mainly to speed up scaffolding, debug route and template issues, and improve the consistency of the user interface. The final application was still reviewed and adjusted manually to match the MySQL schema, fix naming mismatches, and make sure the features worked inside the actual project structure.

## Tools Used

- Gemini:
  Used for early help with Flask route structure, HTML template setup, and general project scaffolding.
- ChatGPT:
  Used for debugging, reviewing route and template logic, and suggesting UI improvements and implementation adjustments.

## How AI Was Used

- Project setup:
  Outline the directory and file structure for the Flask project.
- Flask development:
  Suggestions were used when building or correcting route logic for the dashboard and CRUD pages.
- Frontend and templates:
  Generate or refine HTML page structure and improve visual consistency across the UI.
- Debugging:
  Spot naming mismatches between the Flask code, templates, and the MySQL database schema.
- Learning support:
  AI explanations were used to understand why a suggested change was needed instead of only copying code directly.

## Example Prompts

These are examples of the kinds of prompts that were used during development:

1. "Can you help create the directory and file structure for a Flask + MySQL project?"
2. "Show me what to adjust in this Flask route so it matches my database columns."
3. "Review this HTML template and tell me what needs to change for the route to work correctly."
4. "Suggest UI improvements so the pages look more consistent across forms and tables."
5. "Explain why this route or template is failing and what I should test after changing it."

## What AI Helped With Successfully

- Speeding up the initial structure of the project.
- Identifying route, template, and column-name mismatches.
- Suggesting clearer CRUD flow patterns for add, edit, and delete pages.
- Improving the overall consistency of the UI styling and layout.
- Providing explanations that made it easier to understand fixes before applying them.

## What I Changed Manually After Using AI

- Updated generated code so field names matched the actual MySQL schema.
- Adjusted SQL queries, route logic, and form handling to fit the tables used in the final app.
- Refined the UI so forms, tables, navigation, and action buttons looked more consistent.
- Reviewed AI suggestions before applying them and changed parts that did not fit the project exactly.
- Tested routes after making changes to confirm they worked with the local database and templates.

## Human Verification And Oversight

- I did not treat AI output as final code automatically.
- I manually checked whether route names, field names, and template variables matched the database and application logic.
- I used testing and manual review to confirm that CRUD operations still worked after changes.
- When AI suggestions were too generic or did not match the project schema, I revised them before keeping them.

## Limitations Of AI Assistance

- Some suggestions needed manual correction because generated field names did not always match the database exactly.
- AI could suggest structurally correct code that still needed project-specific fixes.
- UI suggestions were helpful, but they still needed human judgment to fit the final design of the application.

## Lessons Learned

- Always verify AI-generated code against the actual database schema and route names.
- Test all CRUD pages after making AI-assisted changes.
- Ask follow-up questions when a suggestion is unclear instead of copying it blindly.
- Request explanations along with code so the change becomes a learning opportunity.
- AI is most useful as a debugging and drafting assistant, not as a replacement for manual review.
