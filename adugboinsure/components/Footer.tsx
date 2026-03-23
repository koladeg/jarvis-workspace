import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-neutral-900 text-neutral-100">
      <div className="section-container py-16 sm:py-20">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {/* About */}
          <div>
            <div className="flex items-center gap-2 font-bold text-xl text-secondary-400 mb-4">
              <span>💚</span>
              <span>AdugboInsure</span>
            </div>
            <p className="text-neutral-400 text-sm">
              Affordable, trustworthy health insurance for Nigerian communities.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-bold text-white mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              {[
                { href: "/", label: "Home" },
                { href: "/coverage", label: "Coverage" },
                { href: "/enrollment", label: "Enroll" },
                { href: "/faq", label: "FAQ" },
              ].map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-neutral-400 hover:text-secondary-400 transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-bold text-white mb-4">Company</h3>
            <ul className="space-y-2 text-sm">
              {[
                { href: "/about", label: "About Us" },
                { href: "/contact", label: "Contact" },
                { href: "#", label: "Careers" },
                { href: "#", label: "Blog" },
              ].map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-neutral-400 hover:text-secondary-400 transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-bold text-white mb-4">Contact</h3>
            <ul className="space-y-2 text-sm text-neutral-400">
              <li>
                <a href="tel:0800-INSURE-1" className="hover:text-secondary-400">
                  📞 0800-INSURE-1
                </a>
              </li>
              <li>
                <a href="mailto:support@adugboinsure.com" className="hover:text-secondary-400">
                  ✉️ support@adugboinsure.com
                </a>
              </li>
              <li>🏢 Lagos, Nigeria</li>
              <li className="pt-2">
                <a href="#" className="hover:text-secondary-400">
                  Download App →
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-neutral-800 my-8"></div>

        {/* Bottom */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-neutral-400">
          <p>
            &copy; {new Date().getFullYear()} AdugboInsure. All rights
            reserved.
          </p>
          <div className="flex gap-6">
            <a href="#" className="hover:text-secondary-400 transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-secondary-400 transition-colors">
              Terms of Service
            </a>
            <a href="#" className="hover:text-secondary-400 transition-colors">
              Security
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
