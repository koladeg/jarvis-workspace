import Link from "next/link";

export default function Hero() {
  return (
    <section className="bg-gradient-to-br from-primary-50 via-white to-secondary-50 py-16 sm:py-24">
      <div className="section-container">
        <div className="grid md:grid-cols-2 gap-8 items-center">
          {/* Left Column */}
          <div>
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-neutral-900 leading-tight mb-6">
              Health Insurance{" "}
              <span className="text-primary-600">Made Simple</span>
            </h1>
            <p className="text-lg sm:text-xl text-neutral-600 mb-8">
              Affordable community health coverage starting at just{" "}
              <span className="font-bold text-secondary-600">₦15,000/year</span>.
              No hidden fees. No bureaucracy. Just care.
            </p>

            {/* Key Benefits */}
            <div className="space-y-4 mb-8">
              <div className="flex gap-3">
                <div className="text-2xl">✓</div>
                <div>
                  <p className="font-semibold text-neutral-900">
                    Complete Coverage
                  </p>
                  <p className="text-neutral-600">
                    Outpatient, maternity, surgeries, lab tests & more
                  </p>
                </div>
              </div>
              <div className="flex gap-3">
                <div className="text-2xl">✓</div>
                <div>
                  <p className="font-semibold text-neutral-900">
                    Community-Based
                  </p>
                  <p className="text-neutral-600">
                    Trusted by thousands of Nigerians
                  </p>
                </div>
              </div>
              <div className="flex gap-3">
                <div className="text-2xl">✓</div>
                <div>
                  <p className="font-semibold text-neutral-900">
                    Quick Enrollment
                  </p>
                  <p className="text-neutral-600">
                    Sign up in minutes, covered immediately
                  </p>
                </div>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Link href="/enrollment" className="btn-primary text-center">
                Start Enrollment Now
              </Link>
              <Link href="/coverage" className="btn-outline text-center">
                View Coverage Plans
              </Link>
            </div>
          </div>

          {/* Right Column - Visual */}
          <div className="flex justify-center items-center">
            <div className="relative w-64 h-64 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-3xl flex items-center justify-center shadow-lg">
              <div className="text-8xl">💚</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
