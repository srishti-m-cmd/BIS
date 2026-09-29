# BIS SAKSHAM

BIS SAKSHAM is a compliance workspace prototype for exploring product requirements, related Indian Standards, evidence, testing laboratories, and BIS services.

## Run locally

```sh
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Use the left navigation to explore the overview, products, standards, laboratory directory, updates, and BIS services. Expand a product requirement to view its description and sample evidence.

## Build

```sh
npm run build
npm run start
```

## Demo data

The interface is a front-end prototype backed by the sample records in `src/lib/demo-data.ts`. It does not connect to a BIS system, upload evidence, verify licenses, or provide authoritative compliance determinations. Sample standards, requirements, laboratory details, contacts, dates, and updates must be independently checked against current official sources before use.

## Stack

Next.js App Router, React, TypeScript, Tailwind CSS, and Lucide icons.
