export default function AboutSection() {
  return (
    <section className="py-16 sm:py-24 bg-neutral-50">
      <div className="section-container">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="section-title">About AdugboInsure</h1>
          <p className="section-subtitle">
            Bringing affordable, quality health insurance to Nigerian communities
          </p>
        </div>

        {/* Mission */}
        <div className="grid md:grid-cols-2 gap-8 sm:gap-12 items-center mb-16">
          <div>
            <h2 className="text-3xl font-bold text-neutral-900 mb-6">
              Our Mission
            </h2>
            <p className="text-lg text-neutral-700 mb-4 leading-relaxed">
              At AdugboInsure, we believe healthcare should be affordable,
              accessible, and stress-free. We&apos;re on a mission to ensure every
              Nigerian family has reliable health protection without breaking
              the bank.
            </p>
            <p className="text-lg text-neutral-700 leading-relaxed">
              Founded on the principle of community care, we leverage
              collective strength to deliver personalized, responsive health
              insurance that actually listens to your needs.
            </p>
          </div>
          <div className="bg-gradient-to-br from-primary-100 to-secondary-100 rounded-2xl p-12 text-center">
            <div className="text-7xl mb-4">🤝</div>
            <p className="text-xl font-semibold text-neutral-900">
              Built by the community, for the community
            </p>
          </div>
        </div>

        {/* Values */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-neutral-900 text-center mb-12">
            Our Values
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-2xl p-8 border-2 border-primary-200">
              <div className="text-5xl mb-4">💚</div>
              <h3 className="text-xl font-bold text-neutral-900 mb-3">
                Compassion
              </h3>
              <p className="text-neutral-700">
                We genuinely care about your health and wellbeing. Every
                decision we make is guided by how it affects real people.
              </p>
            </div>
            <div className="bg-white rounded-2xl p-8 border-2 border-secondary-200">
              <div className="text-5xl mb-4">🎯</div>
              <h3 className="text-xl font-bold text-neutral-900 mb-3">
                Integrity
              </h3>
              <p className="text-neutral-700">
                No hidden fees, no tricks. We&apos;re transparent about what we
                offer and honest about what we can&apos;t cover.
              </p>
            </div>
            <div className="bg-white rounded-2xl p-8 border-2 border-accent-200">
              <div className="text-5xl mb-4">🚀</div>
              <h3 className="text-xl font-bold text-neutral-900 mb-3">
                Innovation
              </h3>
              <p className="text-neutral-700">
                We continuously improve our services and embrace technology to
                make health insurance simpler for you.
              </p>
            </div>
          </div>
        </div>

        {/* Impact Stats */}
        <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-2xl p-8 sm:p-12 text-white mb-16">
          <h2 className="text-3xl font-bold text-center mb-12">
            Our Impact So Far
          </h2>
          <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { number: "50K+", label: "Members Protected" },
              { number: "₦2B+", label: "Claims Paid" },
              { number: "99%", label: "Satisfaction Rate" },
              { number: "24/7", label: "Customer Support" },
            ].map((stat, idx) => (
              <div key={idx}>
                <div className="text-4xl font-bold mb-2">{stat.number}</div>
                <p className="text-primary-100">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Team Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-neutral-900 text-center mb-12">
            Leadership
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                name: "Dr. Kunle Adeyemi",
                role: "Founder & CEO",
                bio: "Healthcare innovator with 15+ years in community health",
              },
              {
                name: "Chioma Okonkwo",
                role: "Chief Operations Officer",
                bio: "Insurance veteran focused on customer-first operations",
              },
              {
                name: "Tunde Bello",
                role: "Head of Claims",
                bio: "Fast claims processing specialist and member advocate",
              },
            ].map((member, idx) => (
              <div
                key={idx}
                className="bg-white rounded-2xl p-8 border-2 border-neutral-200 text-center hover:border-primary-300 transition-colors"
              >
                <div className="w-24 h-24 mx-auto mb-4 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full flex items-center justify-center text-5xl">
                  👤
                </div>
                <h3 className="text-xl font-bold text-neutral-900 mb-1">
                  {member.name}
                </h3>
                <p className="text-primary-600 font-semibold mb-3">
                  {member.role}
                </p>
                <p className="text-neutral-600">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Community Commitment */}
        <div className="bg-gradient-to-r from-secondary-50 to-accent-50 rounded-2xl p-8 sm:p-12 border-2 border-secondary-200">
          <h2 className="text-3xl font-bold text-neutral-900 mb-6">
            Our Community Commitment
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-bold text-neutral-900 mb-3">
                ✓ Local Healthcare Support
              </h3>
              <p className="text-neutral-700 mb-4">
                We invest 10% of profits back into improving healthcare
                infrastructure in the communities we&apos;re serving.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-neutral-900 mb-3">
                ✓ Free Health Education
              </h3>
              <p className="text-neutral-700 mb-4">
                Regular wellness talks, health screenings, and prevention
                programs for all community members.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-neutral-900 mb-3">
                ✓ Accessible Employment
              </h3>
              <p className="text-neutral-700 mb-4">
                We create jobs in our communities, prioritizing local hiring at
                all levels.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-neutral-900 mb-3">
                ✓ Transparent Operations
              </h3>
              <p className="text-neutral-700 mb-4">
                Open books policy. Members can see how their money is used and
                they influence company decisions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
