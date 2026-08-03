Claude, we are executing a strategic CMS migration for the Manooch platform on the wp-to-strapi branch. We are abandoning the previous CMS/hardcoded structure in favor of Strapi to maximize our customization capabilities for the public-facing website.

Please review the following structural problems and execute the migration plan without generating raw coding logic or database schemas in your acknowledgement. I just need you to understand the architectural intent and set up the structural plan.

1. The Core Issue (Mocks & Rigidity):
Currently, the public website relies heavily on "mock fallback" data, making content updates rigid and requiring developer intervention.

Requirement: All website mock fallbacks must be completely removed from the frontend 
repository. Every piece of static or fallback content must be structurally defined inside Strapi and consumed dynamically via API.

2. The Problem (Coupled Data Models):
Previously, the concepts of "Plans" and "Plugins" on the marketing website were too closely tied to the Portal's internal operational logic. This limits how we can display, market, and describe them to public users.

Requirement: You must create entirely separate, independent definitions for "Plans" and "Plugins" inside Strapi. These Strapi definitions are strictly for marketing and content presentation on the public website. They must NOT share a data structure with or be dependent on the Portal/Super Admin's internal definitions of plans and plugins.

3. The API Mandate:
The public website should act as a pure, headless consumer. All data driving the website's pages must originate from the Strapi structure and be connected exclusively via API.

/human: Ensure that the Strapi content types are designed with the Content Manager in mind. The fields for Plans and Plugins should be intuitive, allowing a non-technical marketing user to easily update pricing display text, feature bullet points, and plugin marketing descriptions without breaking the frontend layout.

/blindspot: Watch out for data-sync illusions. Since we are decoupling the marketing Plans/Plugins (in Strapi) from the operational Plans/Plugins (in the backend Portal), ensure the website frontend fails gracefully if a Strapi API endpoint is temporarily down, rather than crashing the whole page. Also, ensure CORS and API permissions in Strapi are properly restricted for public read-only access.