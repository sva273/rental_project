import { Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { motion } from 'framer-motion'

const Header = () => {
  const { isAuthenticated, logout, user } = useAuthStore()
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <motion.header 
      className="glass-dark sticky top-0 z-50 border-b border-amber-400/20 shadow-2xl backdrop-blur-xl"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center group">
            <div className="flex flex-col">
              <span className="text-2xl font-black gradient-text leading-tight" style={{ fontFamily: "'Playfair Display', serif" }}>
                ÉLÉGANCE
              </span>
              <span className="text-xs text-gray-400 font-light tracking-widest uppercase">Premium Residences</span>
            </div>
          </Link>
          <nav className="flex gap-2 items-center">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link 
                to="/" 
                className={`px-6 py-2.5 rounded-xl font-semibold transition-all ${
                  isActive('/') 
                    ? 'luxury-gradient text-black shadow-lg glow-effect' 
                    : 'text-gray-300 hover:text-amber-400 glass-dark luxury-border'
                }`}
              >
                Explore
              </Link>
            </motion.div>
            {isAuthenticated ? (
              <>
                <Link 
                  to="/bookings" 
                  className={`px-5 py-2.5 rounded-xl font-medium transition-all ${
                    isActive('/bookings') 
                      ? 'luxury-gradient text-black shadow-lg glow-effect' 
                      : 'text-gray-300 hover:text-amber-400 glass-dark luxury-border'
                  }`}
                >
                  Bookings
                </Link>
                <Link 
                  to="/profile" 
                  className={`px-5 py-2.5 rounded-xl font-medium transition-all ${
                    isActive('/profile') 
                      ? 'luxury-gradient text-black shadow-lg glow-effect' 
                      : 'text-gray-300 hover:text-amber-400 glass-dark luxury-border'
                  }`}
                >
                  Profile
                </Link>
                <Link 
                  to="/reviews" 
                  className={`px-5 py-2.5 rounded-xl font-medium transition-all ${
                    isActive('/reviews') 
                      ? 'luxury-gradient text-black shadow-lg glow-effect' 
                      : 'text-gray-300 hover:text-amber-400 glass-dark luxury-border'
                  }`}
                >
                  Reviews
                </Link>
                <div className="flex items-center gap-4 pl-6 ml-6 border-l border-amber-400/20">
                  <motion.div 
                    className="hidden sm:flex items-center gap-3 px-4 py-2 glass-dark rounded-xl luxury-border"
                    whileHover={{ scale: 1.05 }}
                  >
                    <div className="w-10 h-10 luxury-gradient rounded-full flex items-center justify-center text-black text-sm font-black shadow-lg glow-effect">
                      {user?.email?.charAt(0).toUpperCase() || 'U'}
                    </div>
                    <span className="text-sm text-amber-400 font-semibold elegant-text">
                      {user?.email?.split('@')[0]}
                    </span>
                  </motion.div>
                  <motion.button
                    onClick={logout}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-6 py-2.5 glass-dark text-red-400 rounded-xl hover:bg-red-400/10 transition-all shadow-lg hover:shadow-xl font-semibold luxury-border border-red-400/30"
                  >
                    Logout
                  </motion.button>
                </div>
              </>
            ) : (
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link
                  to="/login"
                  className="px-8 py-3 luxury-gradient text-black rounded-xl transition-all shadow-lg glow-effect font-bold"
                >
                  Sign In
                </Link>
              </motion.div>
            )}
          </nav>
        </div>
      </div>
    </motion.header>
  )
}

export default Header

