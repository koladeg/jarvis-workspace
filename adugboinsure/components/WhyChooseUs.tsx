export default function WhyChooseUs() {
  return (
    <section className="py-16 sm:py-24 bg-neutral-50">
      <div className="section-container">
        <div className="grid md:grid-cols-2 gap-8 sm:gap-12 items-center">
          {/* Left - Image/Visual */}
          <div className="flex justify-center order-2 md:order-1">
            <div className="space-y-4 w-full">
              <div className="bg-gradient-to-r from-secondary-100 to-primary-100 rounded-2xl p-8 text-center">
                <p className="text-4xl font-bold text-secondary-600 mb-2">
                  50K+
                </p>
                <p className="text-neutral-700">Happy Members</p>
              </div>
              <div className="bg-gradient-to-r from-primary-100 to-accent-50 rounded-2xl p-8 text-center">
                <p className="text-4xl font-bold text-primary-600 mb-2">
                  99%
                </p>
                <p className="text-neutral-700">Claim Approval Rate</p>
              </div>
              <div className="bg-gradient-to-r from-accent-50 to-secondary-100 rounded-2xl p-8 text-center">
                <p className="text-4xl font-bold text-accent-600 mb-2">
                  24/7
                </p>
                <p className="text-neutral-700">Customer Support</p>
              </div>
            </div>
          </div>

          {/* Right - Content */}
          <div className="order-1 md:order-2">
            <h2 className="section-title">Why Choose AdugboInsure?</h2>
            <p className="text-lg text-neutral-600 mb-8">
              We&apos;re not just another insurance company. We&apos;re part of your
              community, dedicated to making healthcare affordable for everyone.
            </p>

            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-bold text-neutral-900 mb-2">
                  ✓ Transparent & Fair
                </h3>
                <p className="text-neutral-600">
                  No hidden charges. You know exactly what you&apos;re paying for and
                  what you get.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-bold text-neutral-900 mb-2">
                  ✓ Fast Claims
                </h3>
                <p className="text-neutral-600">
                  Get your claims processed in days, not months. We understand
                  you need help quickly.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-bold text-neutral-900 mb-2">
                  ✓ Community Support
                </h3>
                <p className="text-neutral-600">
                  Your money stays in your community. We invest back in local
                  healthcare infrastructure.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-bold text-neutral-900 mb-2">
                  ✓ Simple Language
                </h3>
                <p className="text-neutral-600">
                  No confusing jargon. We explain everything in plain, simple
                  terms.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
