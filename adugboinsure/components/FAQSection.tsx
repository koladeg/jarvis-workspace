"use client";

import { useState } from "react";

interface FAQItem {
  question: string;
  answer: string;
}

const faqs: FAQItem[] = [
  {
    question: "What does AdugboInsure cover?",
    answer:
      "Our plans cover outpatient care, maternity services, emergency treatment, medications, lab tests, minor and major surgeries, and preventive health checks depending on your chosen plan.",
  },
  {
    question: "How much does AdugboInsure cost?",
    answer:
      "Plans start at just ₦15,000 per year for individual coverage, ₦35,000 for family coverage (up to 4 members), and ₦55,000 for premium family coverage. No hidden fees.",
  },
  {
    question: "Who can enroll in AdugboInsure?",
    answer:
      "Any Nigerian resident aged 18 and above can enroll. Family plans include spouse and children under 18. We have no age limits for enrollment.",
  },
  {
    question: "When does my coverage start?",
    answer:
      "Coverage begins immediately after you complete enrollment and receive confirmation. You don't have to wait for a policy document.",
  },
  {
    question: "How do I make a claim?",
    answer:
      "Call our claims hotline at 0800-INSURE-1, visit our website portal, or use the mobile app. Submit your hospital receipt and membership card. Most claims are processed within 5 business days.",
  },
  {
    question: "Can I add family members after enrolling?",
    answer:
      "Yes. You can upgrade your plan or add family members anytime. Just contact our support team and we'll process it within 24 hours.",
  },
  {
    question: "What if I need emergency care outside my location?",
    answer:
      "Our network extends across Nigeria. Emergency care at any registered facility is covered. Just present your membership card.",
  },
  {
    question: "Is there a waiting period before I can claim?",
    answer:
      "No waiting period for emergency care. For other services, coverage is immediate upon enrollment. Pre-existing conditions may have a 3-month period for some specific treatments.",
  },
  {
    question: "Can I cancel my membership?",
    answer:
      "Yes, you can cancel anytime with 14 days notice. However, we offer flexible payment options and plan upgrades if you need adjustments.",
  },
  {
    question: "How is AdugboInsure different from other insurance?",
    answer:
      "We're community-based, transparent, and responsive. We process claims faster, use simple language, keep your money in the community, and genuinely care about your wellbeing—not just profits.",
  },
];

export default function FAQSection() {
  const [openIdx, setOpenIdx] = useState<number | null>(null);

  return (
    <section className="py-16 sm:py-24 bg-neutral-50">
      <div className="section-container">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="section-title">Frequently Asked Questions</h1>
          <p className="section-subtitle">
            Got questions? We&apos;ve got answers. If you don&apos;t find what you&apos;re looking for, contact us!
          </p>
        </div>

        {/* FAQ Items */}
        <div className="max-w-3xl mx-auto space-y-4">
          {faqs.map((faq, idx) => (
            <div
              key={idx}
              className="bg-white rounded-lg border-2 border-neutral-200 overflow-hidden hover:border-primary-300 transition-colors"
            >
              <button
                onClick={() => setOpenIdx(openIdx === idx ? null : idx)}
                className="w-full px-6 py-4 sm:px-8 sm:py-6 text-left flex justify-between items-start gap-4 hover:bg-neutral-50 transition-colors"
              >
                <span className="font-semibold text-neutral-900 text-lg">
                  {faq.question}
                </span>
                <span
                  className={`text-2xl text-primary-600 flex-shrink-0 transition-transform duration-300 ${
                    openIdx === idx ? "rotate-180" : ""
                  }`}
                >
                  ↓
                </span>
              </button>

              {openIdx === idx && (
                <div className="px-6 py-4 sm:px-8 sm:py-6 bg-neutral-50 border-t-2 border-neutral-200">
                  <p className="text-neutral-700 leading-relaxed">
                    {faq.answer}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Contact CTA */}
        <div className="mt-16 bg-gradient-to-r from-primary-50 to-secondary-50 rounded-2xl p-8 sm:p-12 border-2 border-primary-200 text-center">
          <h2 className="text-2xl font-bold text-neutral-900 mb-4">
            Still Have Questions?
          </h2>
          <p className="text-neutral-700 mb-6">
            Our friendly support team is ready to help you
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a
              href="tel:0800-INSURE-1"
              className="text-lg font-bold text-primary-600 hover:text-primary-700"
            >
              📞 Call: 0800-INSURE-1
            </a>
            <span className="text-neutral-400 hidden sm:block">•</span>
            <a
              href="/contact"
              className="text-lg font-bold text-secondary-600 hover:text-secondary-700"
            >
              ✉️ Email us
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
