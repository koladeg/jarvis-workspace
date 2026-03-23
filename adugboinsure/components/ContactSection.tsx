"use client";

import { useState } from "react";

interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export default function ContactSection() {
  const [formData, setFormData] = useState<ContactFormData>({
    name: "",
    email: "",
    subject: "",
    message: "",
  });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Contact form submitted:", formData);
    setSubmitted(true);
    setTimeout(() => {
      setFormData({
        name: "",
        email: "",
        subject: "",
        message: "",
      });
      setSubmitted(false);
    }, 3000);
  };

  return (
    <section className="py-16 sm:py-24 bg-neutral-50">
      <div className="section-container">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="section-title">Get In Touch</h1>
          <p className="section-subtitle">
            Have a question or feedback? We&apos;re here to help. Reach out anytime.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {/* Contact Methods */}
          <div className="md:col-span-1 space-y-6">
            {/* Phone */}
            <div className="bg-white rounded-2xl p-8 border-2 border-primary-200 text-center">
              <div className="text-5xl mb-4">📞</div>
              <h3 className="text-xl font-bold text-neutral-900 mb-2">Call Us</h3>
              <p className="text-neutral-600 mb-2">
                Available 24/7 for support
              </p>
              <a
                href="tel:0800-INSURE-1"
                className="font-bold text-primary-600 hover:text-primary-700"
              >
                0800-INSURE-1
              </a>
            </div>

            {/* Email */}
            <div className="bg-white rounded-2xl p-8 border-2 border-secondary-200 text-center">
              <div className="text-5xl mb-4">✉️</div>
              <h3 className="text-xl font-bold text-neutral-900 mb-2">
                Email Us
              </h3>
              <p className="text-neutral-600 mb-2">
                Response within 24 hours
              </p>
              <a
                href="mailto:support@adugboinsure.com"
                className="font-bold text-secondary-600 hover:text-secondary-700 break-all"
              >
                support@adugboinsure.com
              </a>
            </div>

            {/* Visit */}
            <div className="bg-white rounded-2xl p-8 border-2 border-accent-200 text-center">
              <div className="text-5xl mb-4">🏢</div>
              <h3 className="text-xl font-bold text-neutral-900 mb-2">
                Visit Us
              </h3>
              <p className="text-neutral-600">
                Lagos, Nigeria
                <br />
                <span className="text-sm">(By appointment)</span>
              </p>
            </div>
          </div>

          {/* Contact Form */}
          <div className="md:col-span-2">
            {!submitted ? (
              <div className="bg-white rounded-2xl shadow-lg p-8 sm:p-12">
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Name */}
                  <div>
                    <label className="block text-sm font-semibold text-neutral-900 mb-2">
                      Your Name *
                    </label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      placeholder="Enter your name"
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

                  {/* Subject */}
                  <div>
                    <label className="block text-sm font-semibold text-neutral-900 mb-2">
                      Subject *
                    </label>
                    <input
                      type="text"
                      name="subject"
                      value={formData.subject}
                      onChange={handleChange}
                      required
                      placeholder="How can we help?"
                      className="w-full px-4 py-3 border-2 border-neutral-200 rounded-lg focus:outline-none focus:border-primary-600 transition-colors"
                    />
                  </div>

                  {/* Message */}
                  <div>
                    <label className="block text-sm font-semibold text-neutral-900 mb-2">
                      Message *
                    </label>
                    <textarea
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      required
                      placeholder="Tell us more..."
                      rows={5}
                      className="w-full px-4 py-3 border-2 border-neutral-200 rounded-lg focus:outline-none focus:border-primary-600 transition-colors resize-none"
                    />
                  </div>

                  {/* Submit Button */}
                  <button type="submit" className="w-full btn-primary">
                    Send Message
                  </button>
                </form>
              </div>
            ) : (
              <div className="bg-white rounded-2xl shadow-lg p-8 sm:p-12 text-center">
                <div className="text-6xl mb-6">✓</div>
                <h2 className="text-2xl font-bold text-secondary-600 mb-4">
                  Message Sent!
                </h2>
                <p className="text-neutral-700">
                  Thank you for reaching out. We&apos;ll get back to you as soon as
                  possible.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Social & Additional Info */}
        <div className="bg-primary-50 rounded-2xl p-8 sm:p-12 border-2 border-primary-200">
          <h2 className="text-2xl font-bold text-neutral-900 mb-6 text-center">
            Connect With Us
          </h2>
          <div className="grid sm:grid-cols-3 gap-6 text-center mb-8">
            <div>
              <p className="text-sm text-neutral-600 mb-2">
                Response Time on Email
              </p>
              <p className="font-bold text-neutral-900">Within 24 hours</p>
            </div>
            <div>
              <p className="text-sm text-neutral-600 mb-2">
                Phone Support Hours
              </p>
              <p className="font-bold text-neutral-900">24/7 Available</p>
            </div>
            <div>
              <p className="text-sm text-neutral-600 mb-2">
                Average Call Wait Time
              </p>
              <p className="font-bold text-neutral-900">Less than 2 minutes</p>
            </div>
          </div>

          <p className="text-center text-neutral-700">
            Whether you&apos;re an existing member or considering joining AdugboInsure,
            we&apos;re here to answer your questions and support your health journey.
          </p>
        </div>
      </div>
    </section>
  );
}
