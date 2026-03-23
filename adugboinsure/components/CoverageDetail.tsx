"use client";

import { useState } from "react";

interface Plan {
  name: string;
  price: string;
  description: string;
  coverage: string[];
  popular?: boolean;
}

const plans: Plan[] = [
  {
    name: "Individual Plan",
    price: "₦15,000",
    description: "Perfect for one person",
    coverage: [
      "Outpatient care (up to ₦500,000/year)",
      "Maternity (delivery & antenatal care)",
      "Emergency treatment (₦1,000,000 limit)",
      "Prescribed medications",
      "Lab tests & diagnostics",
      "Minor surgeries",
    ],
  },
  {
    name: "Family Plan",
    price: "₦35,000",
    description: "Cover up to 4 family members",
    coverage: [
      "All Individual Plan benefits",
      "Spouse coverage (same benefits)",
      "Children under 18 (2 kids included)",
      "Higher surgery limit (₦2,000,000)",
      "Preventive health checks",
      "Free wellness programs",
    ],
    popular: true,
  },
  {
    name: "Premium Family Plan",
    price: "₦55,000",
    description: "Complete family protection",
    coverage: [
      "All Family Plan benefits",
      "Extended surgery coverage (₦5,000,000)",
      "Up to 6 family members",
      "Maternity coverage for spouse",
      "Annual health screening",
      "Priority claim processing",
      "24/7 dedicated hotline",
    ],
  },
];

export default function CoverageDetail() {
  const [selectedPlan, setSelectedPlan] = useState(1);

  return (
    <section className="py-16 sm:py-24 bg-neutral-50">
      <div className="section-container">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="section-title">Our Coverage Plans</h1>
          <p className="section-subtitle">
            Choose the plan that works best for you and your family
          </p>
        </div>

        {/* Plans Grid */}
        <div className="grid md:grid-cols-3 gap-6 sm:gap-8 mb-16">
          {plans.map((plan, idx) => (
            <div
              key={idx}
              className={`rounded-2xl overflow-hidden transition-all duration-300 cursor-pointer ${
                selectedPlan === idx
                  ? "ring-2 ring-primary-600 shadow-xl scale-105 md:scale-100"
                  : "shadow-md hover:shadow-lg"
              } ${plan.popular ? "bg-gradient-to-br from-primary-50 to-primary-100" : "bg-white"}`}
              onClick={() => setSelectedPlan(idx)}
            >
              {plan.popular && (
                <div className="bg-secondary-500 text-white text-center py-2 font-bold">
                  MOST POPULAR
                </div>
              )}

              <div className="p-8">
                <h3 className="text-2xl font-bold text-neutral-900 mb-2">
                  {plan.name}
                </h3>
                <p className="text-neutral-600 mb-6">{plan.description}</p>

                <div className="mb-8">
                  <div className="text-5xl font-bold text-primary-600">
                    {plan.price}
                  </div>
                  <p className="text-neutral-600 text-sm">per year</p>
                </div>

                <button
                  className={`w-full py-3 rounded-lg font-bold transition-all duration-200 mb-8 ${
                    plan.popular
                      ? "bg-primary-600 text-white hover:bg-primary-700"
                      : "border-2 border-primary-600 text-primary-600 hover:bg-primary-50"
                  }`}
                >
                  Choose Plan
                </button>

                {/* Coverage List */}
                <div className="space-y-3">
                  {plan.coverage.map((item, i) => (
                    <div key={i} className="flex gap-3">
                      <span className="text-primary-600 font-bold flex-shrink-0">
                        ✓
                      </span>
                      <span className="text-neutral-700 text-sm">{item}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Detailed Coverage Table */}
        <div className="bg-white rounded-2xl overflow-hidden shadow-lg">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-primary-600 text-white">
                <tr>
                  <th className="px-6 py-4 text-left">Coverage Item</th>
                  <th className="px-6 py-4 text-center">Individual</th>
                  <th className="px-6 py-4 text-center">Family</th>
                  <th className="px-6 py-4 text-center">Premium Family</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-200">
                {[
                  {
                    item: "Outpatient Care",
                    individual: "Up to ₦500k",
                    family: "Up to ₦750k",
                    premium: "Unlimited",
                  },
                  {
                    item: "Maternity Coverage",
                    individual: "Yes",
                    family: "Spouse + children",
                    premium: "Full family",
                  },
                  {
                    item: "Emergency Care",
                    individual: "₦1,000,000",
                    family: "₦2,000,000",
                    premium: "₦5,000,000",
                  },
                  {
                    item: "Medications",
                    individual: "Covered",
                    family: "Covered",
                    premium: "100% covered",
                  },
                  {
                    item: "Lab & Diagnostics",
                    individual: "Basic",
                    family: "Comprehensive",
                    premium: "Full coverage",
                  },
                  {
                    item: "Surgeries",
                    individual: "Minor only",
                    family: "Minor & major",
                    premium: "All types",
                  },
                  {
                    item: "Annual Health Check",
                    individual: "No",
                    family: "Yes",
                    premium: "Yes",
                  },
                  {
                    item: "Priority Support",
                    individual: "No",
                    family: "Standard",
                    premium: "24/7 Dedicated",
                  },
                ].map((row, idx) => (
                  <tr key={idx} className="hover:bg-neutral-50">
                    <td className="px-6 py-4 font-semibold text-neutral-900">
                      {row.item}
                    </td>
                    <td className="px-6 py-4 text-center text-neutral-700">
                      {row.individual}
                    </td>
                    <td className="px-6 py-4 text-center text-neutral-700">
                      {row.family}
                    </td>
                    <td className="px-6 py-4 text-center text-neutral-700">
                      {row.premium}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="mt-12 text-center">
          <p className="text-lg text-neutral-600 mb-6">
            Ready to get covered? Choose your plan and enroll in minutes.
          </p>
          <a
            href="/enrollment"
            className="btn-primary inline-block"
          >
            Start Enrollment Now
          </a>
        </div>
      </div>
    </section>
  );
}
