import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <footer className="glass-dark text-white py-12 mt-auto border-t border-white/10">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="mb-4">
              <span className="text-2xl font-black gradient-text" style={{ fontFamily: "'Playfair Display', serif" }}>ÉLÉGANCE</span>
              <p className="text-xs text-gray-400 font-light tracking-widest uppercase mt-1">Premium Residences</p>
            </div>
            <p className="text-gray-400 text-sm elegant-text leading-relaxed">
              Curated selection of the world's most prestigious properties. Where elegance meets excellence.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4 text-amber-400 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>Explore</h3>
            <ul className="space-y-3 text-sm">
              <li>
                <Link to="/" className="text-gray-300 hover:text-amber-400 transition elegant-text">
                  Browse Collection
                </Link>
              </li>
              <li>
                <Link to="/bookings" className="text-gray-300 hover:text-amber-400 transition elegant-text">
                  My Bookings
                </Link>
              </li>
              <li>
                <Link to="/profile" className="text-gray-300 hover:text-amber-400 transition elegant-text">
                  Profile
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4 text-amber-400 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>Support</h3>
            <ul className="space-y-3 text-sm">
              <li>
                <Link to="/help" className="text-gray-300 hover:text-amber-400 transition elegant-text">
                  Help Center
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-300 hover:text-amber-400 transition elegant-text">
                  Contact Us
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="text-gray-300 hover:text-amber-400 transition elegant-text">
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4 text-amber-400 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>Contact</h3>
            <p className="text-gray-300 text-sm mb-2 elegant-text">
              concierge@elegance.com
            </p>
            <p className="text-gray-400 text-xs mb-4 elegant-text">
              +1 (555) 123-4567
            </p>
            <div className="flex gap-3 mt-6">
              <a href="#" className="w-12 h-12 glass-dark rounded-xl flex items-center justify-center hover:bg-amber-400/10 transition luxury-border">
                <svg className="w-6 h-6 text-amber-400" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </a>
              <a href="#" className="w-12 h-12 glass-dark rounded-xl flex items-center justify-center hover:bg-amber-400/10 transition luxury-border">
                <svg className="w-6 h-6 text-amber-400" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
        <div className="border-t border-amber-400/20 pt-8 text-center">
          <p className="text-gray-400 text-sm elegant-text">&copy; 2024 ÉLÉGANCE. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer

