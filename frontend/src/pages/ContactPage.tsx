import { useState } from 'react'
import { motion } from 'framer-motion'
import AnimatedSection from '../components/common/AnimatedSection'

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  })
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Simulate form submission
    setSubmitted(true)
    setTimeout(() => {
      setSubmitted(false)
      setFormData({ name: '', email: '', subject: '', message: '' })
    }, 3000)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <AnimatedSection delay={0.1}>
        <div className="mb-12 text-center">
          <h1 className="text-6xl font-black text-white mb-4 text-shadow-luxury" style={{ fontFamily: "'Playfair Display', serif" }}>
            Contact Us
          </h1>
          <p className="text-gray-400 text-lg elegant-text">Get in touch with our concierge team</p>
        </div>
      </AnimatedSection>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <AnimatedSection delay={0.2}>
          <div className="glass-dark rounded-2xl p-8 luxury-border">
            <h2 className="text-3xl font-black text-white mb-6 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
              Get in Touch
            </h2>
            <div className="space-y-6">
              <div>
                <div className="flex items-center gap-4 mb-2">
                  <div className="w-12 h-12 luxury-gradient rounded-xl flex items-center justify-center glow-effect">
                    <svg className="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-amber-400 font-semibold elegant-text">Email</p>
                    <p className="text-gray-300">concierge@elegance.com</p>
                  </div>
                </div>
              </div>
              <div>
                <div className="flex items-center gap-4 mb-2">
                  <div className="w-12 h-12 luxury-gradient rounded-xl flex items-center justify-center glow-effect">
                    <svg className="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-amber-400 font-semibold elegant-text">Phone</p>
                    <p className="text-gray-300">+1 (555) 123-4567</p>
                  </div>
                </div>
              </div>
              <div>
                <div className="flex items-center gap-4 mb-2">
                  <div className="w-12 h-12 luxury-gradient rounded-xl flex items-center justify-center glow-effect">
                    <svg className="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-amber-400 font-semibold elegant-text">Address</p>
                    <p className="text-gray-300">123 Luxury Avenue<br />New York, NY 10001</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </AnimatedSection>

        <AnimatedSection delay={0.3}>
          <div className="glass-dark rounded-2xl p-8 luxury-border">
            <h2 className="text-3xl font-black text-white mb-6 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
              Send Message
            </h2>
            {submitted ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center py-8"
              >
                <div className="w-20 h-20 luxury-gradient rounded-full flex items-center justify-center mx-auto mb-4 glow-effect">
                  <svg className="w-10 h-10 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <p className="text-amber-400 text-xl font-semibold elegant-text">Message sent successfully!</p>
                <p className="text-gray-400 mt-2">We'll get back to you within 24 hours.</p>
              </motion.div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                  <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">Name</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-5 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                    placeholder="Your name"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">Email</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-5 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                    placeholder="your@email.com"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">Subject</label>
                  <input
                    type="text"
                    value={formData.subject}
                    onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                    className="w-full px-5 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                    placeholder="Subject"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">Message</label>
                  <textarea
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    rows={5}
                    className="w-full px-5 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border resize-none"
                    placeholder="Your message"
                    required
                  />
                </div>
                <motion.button
                  type="submit"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full px-8 py-4 luxury-gradient text-black rounded-xl font-bold glow-effect"
                >
                  Send Message
                </motion.button>
              </form>
            )}
          </div>
        </AnimatedSection>
      </div>
    </div>
  )
}

export default ContactPage

