import type { Metadata } from "next";
import "./globals.css";
import Navigation from "@/components/Navigation";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "AdugboInsure - Community Health Insurance",
  description:
    "Affordable community-based health insurance. Just ₦15,000/year for comprehensive coverage.",
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='75' font-size='75' fill='%230284c7'>♥</text></svg>",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="bg-neutral-50 text-neutral-900">
        <Navigation />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
