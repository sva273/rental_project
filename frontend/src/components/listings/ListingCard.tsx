import { Link } from 'react-router-dom'
import { Listing } from '../../types/listing'
import { motion } from 'framer-motion'

interface ListingCardProps {
  listing: Listing
}

const ListingCard = ({ listing }: ListingCardProps) => {
  const defaultImage = 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop'

  return (
    <Link to={`/listings/${listing.id}`} className="block h-full group">
      <motion.div 
        className="glass rounded-2xl premium-shadow overflow-hidden card-hover h-full flex flex-col luxury-border relative"
        whileHover={{ 
          scale: 1.02,
          transition: { duration: 0.4 }
        }}
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="relative h-64 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-amber-900/20 to-black/40"></div>
          <img
            src={listing.main_image || defaultImage}
            alt={listing.title}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
            onError={(e) => {
              e.currentTarget.src = defaultImage
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent"></div>
          
          {/* Premium badge */}
          <div className="absolute top-4 left-4">
            <div className="glass-dark px-4 py-1.5 rounded-full luxury-border">
              <span className="text-amber-400 text-xs font-semibold tracking-wider uppercase">Premium</span>
            </div>
          </div>
          
          {!listing.is_active && (
            <div className="absolute top-4 right-4 glass-dark px-3 py-1.5 rounded-full luxury-border">
              <span className="text-red-400 text-xs font-semibold">Unavailable</span>
            </div>
          )}
          
          {listing.average_rating > 0 && (
            <div className="absolute bottom-4 right-4 glass-dark px-3 py-2 rounded-lg luxury-border">
              <div className="flex items-center gap-1.5">
                <svg className="w-4 h-4 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <span className="text-white text-sm font-bold">{listing.average_rating.toFixed(1)}</span>
              </div>
            </div>
          )}
          
          {/* Decorative corner elements */}
          <div className="absolute top-0 left-0 w-12 h-12 border-t-2 border-l-2 border-amber-400/30"></div>
          <div className="absolute top-0 right-0 w-12 h-12 border-t-2 border-r-2 border-amber-400/30"></div>
        </div>
        <div className="p-8 flex-grow flex flex-col bg-gradient-to-b from-white/10 to-white/5 backdrop-blur-xl">
          <h3 className="text-2xl font-bold mb-3 text-white line-clamp-2 group-hover:text-amber-400 transition-colors elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
            {listing.title}
          </h3>
          <p className="text-gray-300 text-sm mb-6 flex items-center font-light">
            <svg className="w-4 h-4 mr-2 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {listing.city}, {listing.country}
          </p>
          <div className="mt-auto">
            <div className="flex items-center gap-6 mb-6 text-gray-400">
              {listing.rooms && (
                <div className="flex items-center text-sm font-light">
                  <span className="elegant-text text-gray-300">{listing.rooms} {listing.rooms === 1 ? 'bedroom' : 'bedrooms'}</span>
                </div>
              )}
              {listing.reviews_count > 0 && (
                <div className="flex items-center text-sm font-light">
                  <svg className="w-4 h-4 mr-2 text-amber-400/60" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span className="elegant-text">{listing.reviews_count} {listing.reviews_count === 1 ? 'review' : 'reviews'}</span>
                </div>
              )}
            </div>
            <div className="flex items-center justify-between pt-6 border-t border-amber-400/20">
              <div>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-black gradient-text" style={{ fontFamily: "'Playfair Display', serif" }}>
                    ${listing.price_per_day}
                  </span>
                  <span className="text-gray-400 text-sm font-light elegant-text">per night</span>
                </div>
              </div>
              <motion.div 
                className="px-6 py-2.5 glass-dark text-amber-400 rounded-lg text-sm font-semibold opacity-0 group-hover:opacity-100 luxury-border"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                View →
              </motion.div>
            </div>
          </div>
        </div>
      </motion.div>
    </Link>
  )
}

export default ListingCard

