import Link from "next/link";

export default function CTASection() {
  return (
    <section className="py-16 sm:py-24 bg-gradient-to-r from-primary-600 to-primary-700">
      <div className="section-container text-center">
        <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
          Ready to Protect Your Health?
        </h2>
        <p className="text-lg text-primary-100 mb-8 max-w-2xl mx-auto">
          Join thousands of Nigerians who have chosen affordable, reliable
          health insurance. Enroll today and get covered immediately.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/enrollment"
            className="px-8 py-4 bg-white text-primary-600 font-bold rounded-lg hover:bg-neutral-50 transition-all duration-200 text-center"
          >
            Start Free Enrollment
          </Link>
          <Link
            href="/faq"
            className="px-8 py-4 border-2 border-white text-white font-bold rounded-lg hover:bg-primary-600 transition-all duration-200 text-center"
          >
            Have Questions?
          </Link>
        </div>

        <p className="text-primary-100 text-sm mt-8">
          ✓ No credit card required • ✓ Instant activation • ✓ Lifetime support
        </p>
      </div>
    </section>
  );
}
