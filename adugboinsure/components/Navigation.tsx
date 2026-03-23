"use client";

import Link from "next/link";
import { useState } from "react";

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  const navLinks = [
    { href: "/", label: "Home" },
    { href: "/coverage", label: "Coverage" },
    { href: "/faq", label: "FAQ" },
    { href: "/about", label: "About" },
    { href: "/contact", label: "Contact" },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-white shadow-md">
      <div className="section-container">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link
            href="/"
            className="flex items-center gap-2 font-bold text-xl text-primary-600 hover:text-primary-700"
          >
            <span className="text-2xl">💚</span>
            <span>AdugboInsure</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="px-4 py-2 text-neutral-700 hover:text-primary-600 transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Desktop CTA */}
          <div className="hidden md:block">
            <Link
              href="/enrollment"
              className="btn-primary text-sm"
            >
              Enroll Now
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 text-neutral-700 hover:bg-neutral-100 rounded"
            aria-label="Toggle menu"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden pb-4 border-t border-neutral-200">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className="block px-4 py-2 text-neutral-700 hover:bg-neutral-100 rounded"
              >
                {link.label}
              </Link>
            ))}
            <Link
              href="/enrollment"
              onClick={() => setIsOpen(false)}
              className="block px-4 py-2 mt-2 btn-primary text-sm text-center"
            >
              Enroll Now
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
