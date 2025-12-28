import { motion } from 'framer-motion'
import AnimatedSection from '../components/common/AnimatedSection'

const HelpCenterPage = () => {
  const faqs = [
    {
      question: "How do I book a property?",
      answer: "Browse our exclusive collection, select your desired property, choose your dates, and complete the booking. Our concierge team will confirm your reservation within 24 hours."
    },
    {
      question: "What is included in the rental?",
      answer: "Each property includes premium amenities, high-speed internet, luxury linens, and full access to all listed facilities. Specific amenities are detailed on each property page."
    },
    {
      question: "Can I cancel my booking?",
      answer: "Yes, you can cancel your booking up to 7 days before check-in for a full refund. Cancellations within 7 days are subject to our cancellation policy."
    },
    {
      question: "How do I contact property owners?",
      answer: "Once your booking is confirmed, you'll receive contact information for the property manager. Our support team is also available 24/7 to assist you."
    },
    {
      question: "What payment methods do you accept?",
      answer: "We accept all major credit cards, bank transfers, and premium payment methods. All transactions are secured with bank-level encryption."
    },
    {
      question: "Are there any additional fees?",
      answer: "The price shown includes all standard fees. Optional services like parking, early check-in, or concierge services may incur additional charges."
    }
  ]

  return (
    <div className="max-w-4xl mx-auto">
      <AnimatedSection delay={0.1}>
        <div className="mb-12 text-center">
          <h1 className="text-6xl font-black text-white mb-4 text-shadow-luxury" style={{ fontFamily: "'Playfair Display', serif" }}>
            Help Center
          </h1>
          <p className="text-gray-400 text-lg elegant-text">Find answers to your questions</p>
        </div>
      </AnimatedSection>

      <div className="space-y-6">
        {faqs.map((faq, index) => (
          <AnimatedSection key={index} delay={0.1 * (index + 1)}>
            <motion.div
              className="glass-dark rounded-2xl p-8 luxury-border"
              whileHover={{ scale: 1.02 }}
              transition={{ duration: 0.2 }}
            >
              <h3 className="text-2xl font-bold text-amber-400 mb-4 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
                {faq.question}
              </h3>
              <p className="text-gray-300 leading-relaxed elegant-text">
                {faq.answer}
              </p>
            </motion.div>
          </AnimatedSection>
        ))}
      </div>

      <AnimatedSection delay={0.8}>
        <div className="mt-12 glass-dark rounded-2xl p-10 luxury-border text-center">
          <h2 className="text-3xl font-black text-white mb-4 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
            Still have questions?
          </h2>
          <p className="text-gray-400 mb-6 elegant-text">Our concierge team is here to help</p>
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

export default HelpCenterPage

