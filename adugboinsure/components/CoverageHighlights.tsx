export default function CoverageHighlights() {
  const coverageItems = [
    {
      icon: "🏥",
      title: "Outpatient Care",
      description: "Doctor visits, consultations, and basic treatments",
    },
    {
      icon: "👶",
      title: "Maternity & Child",
      description: "Pregnancy care, delivery, and child health coverage",
    },
    {
      icon: "🚑",
      title: "Emergency Care",
      description: "Urgent medical attention when you need it most",
    },
    {
      icon: "💊",
      title: "Medications",
      description: "Essential medicines covered at partner pharmacies",
    },
    {
      icon: "🔬",
      title: "Lab Tests",
      description: "Blood work, imaging, and diagnostic tests",
    },
    {
      icon: "🏨",
      title: "Surgeries",
      description: "Major and minor surgical procedures covered",
    },
  ];

  return (
    <section className="py-16 sm:py-24 bg-white">
      <div className="section-container">
        <div className="text-center mb-16">
          <h2 className="section-title">What&apos;s Covered</h2>
          <p className="section-subtitle">
            Comprehensive health protection for you and your family
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {coverageItems.map((item, idx) => (
            <div
              key={idx}
              className="p-6 sm:p-8 rounded-xl border-2 border-neutral-100 hover:border-primary-300 hover:shadow-lg transition-all duration-300"
            >
              <div className="text-5xl mb-4">{item.icon}</div>
              <h3 className="text-xl font-bold text-neutral-900 mb-3">
                {item.title}
              </h3>
              <p className="text-neutral-600">{item.description}</p>
            </div>
          ))}
        </div>

        <div className="mt-12 sm:mt-16 bg-primary-50 rounded-2xl p-8 sm:p-12 border-2 border-primary-200">
          <p className="text-center text-lg text-neutral-700">
            <span className="font-bold text-primary-700">Plus:</span> Free
            preventive health talks, community wellness programs, and 24/7
            support hotline
          </p>
        </div>
      </div>
    </section>
  );
}
