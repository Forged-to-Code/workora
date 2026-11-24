# Workora — Local work. Smarter connections.

A hyperlocal employment MVP for India's informal and semi-skilled workforce. The supplied logo is used with its original navy/orange colors on white; the interface follows #0A0A0A and #15A82E. The four design references informed the dark hero, search bar, job cards, filters, and bento layouts. Original vector illustrations replace stock photography; they are embedded and work offline.

## 1. Try it immediately (no installation)
Open `Workora_Demo.html` in Chrome or Edge. The standalone file includes the application, styles, logo, illustrations and sample data. No API credentials are needed. It uses an offline React 16 compatibility adapter, not the production dependency bundle. For voice recognition or location, the browser may require HTTPS or localhost and an internet connection. If a file URL is restricted, serve the folder with `python3 -m http.server 8000` and open `http://localhost:8000/Workora_Demo.html`.

Suggested hackathon walkthrough:
1. Search `Electrician within 5 km, ₹800 per day` (default area: Vajarahalli, Bengaluru).
2. View the result, save it and apply. Switch to map view.
3. Log in using **Continue as demo worker**, view saved jobs and applications.
4. Open document verification, choose **Use synthetic sample**, check consent and submit.
5. Open Admin review, enter demo reviewer mode and approve or reject.
6. Log in as demo employer, post a listing, review applicants and update an application status.

All sample jobs, accounts, businesses, reports and verification actions are fictional. Demo mode does not contact employers or perform identity verification. Do not upload real documents or enter real personal information. Clear your browser's site data to reset the demo.

## 2. Run the actual React / TypeScript / Tailwind project
Install Node.js 22 LTS and a code editor such as VS Code. Extract the ZIP and open the `workora` folder. In a terminal:

```sh
npm install
npm run dev
```

Open the localhost URL Vite prints (usually http://localhost:5173). No `.env` is required for local demo mode. The normal project uses React 18, React Router, Tailwind CSS and Lucide icons; the custom stylesheet defines the main visual system. Run `npm run typecheck` and `npm run build` before deployment. These commands require installed dependencies; dependency installation was blocked by the authoring environment's network restrictions, so the Vite build and full typecheck have not been executed.

## 3. Connect Supabase (optional, for real data)
Create a fresh sandbox Supabase project. Do not apply this initial migration to an existing database because it defines a complete new schema and grants. In Supabase SQL Editor, run `supabase/migrations/001_initial.sql`. Review the RLS and column permissions before deploying. In the project root, copy `.env.example` to `.env.local` and enter the project URL and public anon key, available from your project settings. Never place a service-role key or Gemini API key in a `VITE_` variable. Restart Vite. The app switches to connected mode when both public Supabase values exist. Register worker and employer accounts. Configure email confirmation and auth redirect URLs in Supabase. Create a separate administrator account, then assign its role from a trusted SQL editor:

```sql
update public.profiles set role='admin' where id='YOUR_ADMIN_AUTH_USER_UUID';
```

Never let users assign themselves admin. The schema includes role-restricted access, duplicate application prevention, private documents, an authorised review policy and a status-only employer RPC. For optional sample listings, edit the UUID placeholders in `supabase/seed.sql` to an employer account's ID and run it in the sandbox only. Remove seed data before real launch.

## 4. Connect Gemini and contact submissions
Install the Supabase CLI using its supported installation method. Log in and link the project. From the project folder:

```sh
supabase login
supabase link --project-ref YOUR_PROJECT_REF
supabase secrets set GEMINI_API_KEY=YOUR_PRIVATE_KEY
supabase secrets set GEMINI_MODEL=gemini-2.5-flash
supabase functions deploy parse-query --no-verify-jwt
supabase functions deploy contact --no-verify-jwt
```

Use a supported Gemini model available in your account; model name and structured output support must be verified. These functions are deliberately public for pre-login search/contact; they validate input and use a basic per-IP database rate limit. Before public release add gateway-level abuse prevention, stronger trusted IP handling, CAPTCHA or authenticated quota as appropriate, and restrict CORS. Search sends text only (not GPS or audio) to Gemini. Gemini extracts structured requirements; the app filters actual database records. Local keyword parsing is the fallback. Contact submissions are stored in the database, not emailed. Configure administrator monitoring and a support process before launch.

## 5. Voice and location
Use the microphone icon and choose English, Hindi, Kannada, Tamil, Telugu, Bengali or Marathi. Actual language support and recognition quality depend on your browser and speech provider; the interface itself is English. Grant microphone permission. Use text if recognition fails. The local parser recognizes a limited multilingual vocabulary; Gemini is needed for broader regional-language interpretation. Choose a Bengaluru area or grant GPS access. Distances are Haversine straight-line estimates, not driving distances. Leaflet uses OpenStreetMap tiles in the regular app; the offline preview uses a schematic map. Review OSM tile usage terms before scaling.

## 6. Deploy to Vercel
Create a Git repository, commit the source files (not `.env.local`), and import the repository into Vercel. Select Vite, build command `npm run build`, output `dist`. Add `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` if you want connected mode. Keep Gemini in Supabase secrets. Deploy, then add the HTTPS domain to Supabase authentication redirect settings. Check all links, authentication, password recovery, permissions, map and voice access on the actual deployed URL. Deployment has not been performed.

## 7. Project layout
- `src/App.tsx`: routes, pages and interactions
- `src/data.ts`: sample listings, local query parsing, geodistance, job types
- `src/Illustration.tsx`: reusable local vector artwork
- `src/Map.tsx`: Leaflet and offline schematic map
- `src/content.ts`: 24 FAQs and draft legal pages
- `src/styles.css`: responsive design system and Tailwind entry
- `src/main.tsx`: React Router, Supabase and Leaflet initialization
- `supabase/migrations`: PostgreSQL schema, constraints, RLS and private bucket
- `supabase/functions`: Gemini structured query parser and contact handler
- `tests/browser_smoke.py`: offline Chromium smoke test
- `tools/build-offline.cjs`: environment-specific offline packaging tool; not needed for normal development. It uses locally available TypeScript and React vendor builds.

## 8. Testing and readiness
Passed in the standalone preview (Chromium): homepage rendering, twelve categories, text search with wage/radius, bookmarking, applying, map display, details, worker saved jobs/application status, synthetic document submission and simulated approval, employer job posting and closing, applicant status changes, 16 page routes, searchable FAQs and 390px responsive menu. No uncaught browser errors in the smoke test. The browser environment blocked normal URL navigation, so testing injected the HTML into a blank page with a storage shim; persistence across real browser restarts was not independently tested. Actual microphone/GPS, connected Supabase, Gemini, OSM tiles, email confirmation/recovery, storage upload and RLS enforcement have not been tested end-to-end.

Production gaps: complete language translations and cross-browser voice QA; actual photos (local original illustrations are supplied instead); direct messaging or phone handoff; wider geocoding and employer-selected exact job locations; richer availability/schedule matching and worker recommendations; document content preview and detailed upload progress; admin moderation actions beyond report resolution; account deletion and privacy retention processes; independent RLS/security review, spam prevention and full accessibility testing. The current demo uses a simple deterministic matching score internally and does not show fabricated percentages. The supplied 450M+ estimate is not published because it has not been verified. Privacy/terms/cookie pages are draft copy, not legal advice or final launch documents. Do not use real identity documents until connected storage, reviewer permissions and retention are verified.
