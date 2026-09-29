import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "react-hot-toast";

export const metadata: Metadata = {
  title: "BIS SAKSHAM — Compliance Workspace",
  description: "A workspace for exploring product compliance requirements, standards, evidence and BIS services.",
  keywords: ["BIS", "Indian Standards", "IS", "compliance", "certification", "ISI Mark", "quality control"],
  openGraph: {
    title: "BIS SAKSHAM — Compliance Workspace",
    description: "Explore product compliance requirements, standards, evidence and BIS services.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased bg-[#F7F8FA] text-[#111827]">
        {children}
        <Toaster
          position="bottom-right"
          toastOptions={{
            style: {
              background: "#0B1F3A",
              color: "#fff",
              borderRadius: "8px",
              fontSize: "14px",
            },
            success: {
              iconTheme: { primary: "#16834B", secondary: "#fff" },
            },
            error: {
              iconTheme: { primary: "#C0392B", secondary: "#fff" },
            },
          }}
        />
      </body>
    </html>
  );
}
