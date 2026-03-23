"use client";

import { useState } from "react";
import Link from "next/link";

interface FormData {
  fullName: string;
  email: string;
  phone: string;
  plan: string;
  familyMembers: string;
  acceptTerms: boolean;
}

export default function EnrollmentForm() {
  const [formData, setFormData] = useState<FormData>({
    fullName: "",
    email: "",
    phone: "",
    plan: "individual",
    familyMembers: "1",
    acceptTerms: false,
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would send data to your backend
    console.log("Form submitted:", formData);
    setSubmitted(true);
    setTimeout(() => {
      setFormData({
        fullName: "",
        email: "",
        phone: "",
        plan: "individual",
        familyMembers: "1",
        acceptTerms: false,
      });
      setSubmitted(false);
    }, 3000);
  };

  return (
    <section className="py-16 sm:py-24 bg-neutral-50">
      <div className="section-container">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="section-title">Start Your Coverage Today</h1>
            <p className="section-subtitle">
              Quick and simple enrollment. You&apos;ll be protected immediately after
              signup.
            </p>
          </div>

          {/* Form */}
          {!submitted ? (
            <div className="bg-white rounded-2xl shadow-lg p-8 sm:p-12">
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Full Name */}
                <div>
                  <label className="block text-sm font-semibold text-neutral-900 mb-2">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleChange}
                    required
                    placeholder="Enter your full name"
                    className="w-full px-4 py-3 border-2 border-neutral-200 rounded-lg focus:outline-none focus:border-primary-600 transition-colors"
                  />
                </div>

                {/* Email */}
                <div>
                  <label className="block text-sm font-semibold text-neutral-900 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="your.email@example.com"
                    className="w-full px-4 py-3 border-2 border-neutral-200 rounded-lg focus:outline-none focus:border-primary-600 transition-colors"
                  />
                </div>

                {/* Phone */}
                <div>
                  <label className="block text-sm font-semibold text-neutral-900 mb-2">
                    Phone Number *
                  </label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    required
                    placeholder="0801234567"
                    className="w-full px-4 py-3 border-2 border-neutral-200 rounded-lg focus:outline-none focus:border-primary-600 transition-colors"
                  />
                </div>

                {/* Plan Selection */}
                <div>
                  <label className="block text-sm font-semibold text-neutral-900 mb-2">
                    Select Your Plan *
                  </label>
                  <select
                    name="plan"
                    value={formData.plan}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-neutral-200 rounded-lg focus:outline-none focus:border-primary-600 transition-colors bg-white"
                  >
                    <option value="individual">
                      Individual Plan - ₦15,000/year
                    </option>
                    <option value="family">
                      Family Plan - ₦35,000/year
                    </option>
                    <option value="premium">
                      Premium Family Plan - ₦55,000/year
                    </option>
                  </select>
                </div>

                {/* Family Members */}
                {formData.plan !== "individual" && (
                  <div>
                    <label className="block text-sm font-semibold text-neutral-900 mb-2">
                      Number of Family Members *
                    </label>
                    <select
                      name="familyMembers"
                      value={formData.familyMembers}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border-2 border-neutral-200 rounded-lg focus:outline-none focus:border-primary-600 transition-colors bg-white"
                    >
                      {[1, 2, 3, 4, 5, 6].map((num) => (
                        <option key={num} value={num}>
                          {num} {num === 1 ? "person" : "people"}
                        </option>
                      ))}
                    </select>
                  </div>
                )}

                {/* Terms & Conditions */}
                <div className="flex gap-3">
                  <input
                    type="checkbox"
                    name="acceptTerms"
                    id="terms"
                    checked={formData.acceptTerms}
                    onChange={handleChange}
                    required
                    className="w-5 h-5 mt-1 cursor-pointer"
                  />
                  <label
                    htmlFor="terms"
                    className="text-sm text-neutral-600 cursor-pointer"
                  >
                    I agree to the terms and conditions, and privacy policy of
                    AdugboInsure. I understand that coverage begins immediately
                    upon enrollment confirmation.
                  </label>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={!formData.acceptTerms}
                  className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Complete Enrollment
                </button>

                <p className="text-center text-neutral-600 text-sm">
                  Need help? Call us at{" "}
                  <span className="font-bold">0800-INSURE-1</span> or email
                  support@adugboinsure.com
                </p>
              </form>
            </div>
          ) : (
            <div className="bg-white rounded-2xl shadow-lg p-8 sm:p-12 text-center">
              <div className="mb-6 text-6xl">✓</div>
              <h2 className="text-3xl font-bold text-secondary-600 mb-4">
                Welcome to AdugboInsure!
              </h2>
              <p className="text-lg text-neutral-700 mb-6">
                Your enrollment is confirmed. You&apos;re now covered and protected.
                A confirmation email has been sent to <strong>{formData.email}</strong>.
              </p>
              <div className="bg-primary-50 rounded-lg p-6 mb-6">
                <p className="text-neutral-700 mb-2">
                  <strong>Next Steps:</strong>
                </p>
                <ul className="text-left text-neutral-700 space-y-2">
                  <li>• Check your email for enrollment documents</li>
                  <li>• Download the AdugboInsure mobile app</li>
                  <li>• Save your membership number: ADG-{Math.random().toString(36).substr(2, 9).toUpperCase()}</li>
                  <li>• Visit our provider network to access services</li>
                </ul>
              </div>
              <Link href="/" className="btn-primary inline-block">
                Return to Home
              </Link>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
