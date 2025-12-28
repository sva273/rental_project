import { motion } from 'framer-motion'
import AnimatedSection from '../components/common/AnimatedSection'

const PrivacyPolicyPage = () => {
  const sections = [
    {
      title: "Information We Collect",
      content: "We collect information that you provide directly to us, including your name, email address, phone number, payment information, and booking preferences. We also automatically collect certain information about your device and how you interact with our platform."
    },
    {
      title: "How We Use Your Information",
      content: "We use the information we collect to process your bookings, communicate with you about your reservations, provide customer support, improve our services, send you marketing communications (with your consent), and comply with legal obligations."
    },
    {
      title: "Information Sharing",
      content: "We may share your information with property owners/managers to facilitate bookings, with payment processors for transaction processing, and with service providers who assist us in operating our platform. We do not sell your personal information to third parties."
    },
    {
      title: "Data Security",
      content: "We implement industry-standard security measures to protect your personal information, including encryption, secure servers, and regular security audits. However, no method of transmission over the internet is 100% secure."
    },
    {
      title: "Your Rights",
      content: "You have the right to access, update, or delete your personal information at any time. You can also opt-out of marketing communications, request a copy of your data, or object to certain processing activities. Contact us to exercise these rights."
    },
    {
      title: "Cookies and Tracking",
      content: "We use cookies and similar tracking technologies to enhance your experience, analyze usage patterns, and personalize content. You can control cookies through your browser settings, though this may affect some functionality."
    },
    {
      title: "Third-Party Links",
      content: "Our platform may contain links to third-party websites. We are not responsible for the privacy practices of these external sites. We encourage you to review their privacy policies before providing any information."
    },
    {
      title: "Changes to This Policy",
      content: "We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the new policy on this page and updating the 'Last Updated' date. Your continued use of our services constitutes acceptance of the updated policy."
    }
  ]

  return (
    <div className="max-w-4xl mx-auto">
      <AnimatedSection delay={0.1}>
        <div className="mb-12 text-center">
          <h1 className="text-6xl font-black text-white mb-4 text-shadow-luxury" style={{ fontFamily: "'Playfair Display', serif" }}>
            Privacy Policy
          </h1>
          <p className="text-gray-400 text-lg elegant-text">Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
        </div>
      </AnimatedSection>

      <AnimatedSection delay={0.2}>
        <div className="glass-dark rounded-2xl p-8 mb-8 luxury-border">
          <p className="text-gray-300 leading-relaxed elegant-text text-lg">
            At ÉLÉGANCE, we are committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our premium rental platform.
          </p>
        </div>
      </AnimatedSection>

      <div className="space-y-6">
        {sections.map((section, index) => (
          <AnimatedSection key={index} delay={0.1 * (index + 2)}>
            <motion.div
              className="glass-dark rounded-2xl p-8 luxury-border"
              whileHover={{ scale: 1.01 }}
              transition={{ duration: 0.2 }}
            >
              <h2 className="text-3xl font-black text-amber-400 mb-4 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
                {section.title}
              </h2>
              <p className="text-gray-300 leading-relaxed elegant-text">
                {section.content}
              </p>
            </motion.div>
          </AnimatedSection>
        ))}
      </div>

      <AnimatedSection delay={1}>
        <div className="mt-12 glass-dark rounded-2xl p-10 luxury-border text-center">
          <h2 className="text-3xl font-black text-white mb-4 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
            Questions About Privacy?
          </h2>
          <p className="text-gray-400 mb-6 elegant-text">Contact our privacy team</p>
          <motion.a
            href="/contact"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="inline-block px-8 py-4 luxury-gradient text-black rounded-xl font-bold glow-effect"
          >
            Contact Us
          </motion.a>
        </div>
      </AnimatedSection>
    </div>
  )
}

export default PrivacyPolicyPage

