import { ListingFilters as Filters } from '../../types/listing'
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import PropertyTypeSelector from './PropertyTypeSelector'

interface ListingFiltersProps {
  filters: Filters
  onFiltersChange: (filters: Filters) => void
}

const ListingFilters = ({ filters, onFiltersChange }: ListingFiltersProps) => {
  const [isExpanded, setIsExpanded] = useState(false)

  const handleChange = (key: keyof Filters, value: string | number | undefined) => {
    onFiltersChange({ ...filters, [key]: value || undefined })
  }

  const clearFilters = () => {
    onFiltersChange({})
  }

  const hasActiveFilters = Object.keys(filters).length > 0

  return (
    <div className="glass-dark rounded-2xl premium-shadow p-8 mb-10 luxury-border">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 luxury-gradient rounded-xl flex items-center justify-center glow-effect">
            <svg className="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
          </div>
          <div>
            <h3 className="text-2xl font-black text-white elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>Refine Selection</h3>
            <p className="text-gray-400 text-sm font-light">Discover your perfect residence</p>
          </div>
        </div>
        <div className="flex gap-2">
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="px-5 py-2.5 glass-dark text-red-400 rounded-xl hover:bg-red-400/10 font-medium transition-all text-sm luxury-border"
            >
              Clear all
            </button>
          )}
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="px-5 py-2.5 glass-dark text-amber-400 rounded-xl hover:bg-amber-400/10 font-medium transition-all text-sm luxury-border"
          >
            {isExpanded ? 'Less' : 'More'} filters
          </button>
        </div>
      </div>

      <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 ${isExpanded ? '' : 'hidden md:grid'}`}>
        <div>
          <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">City</label>
          <input
            type="text"
            value={filters.city || ''}
            onChange={(e) => handleChange('city', e.target.value)}
            className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
            placeholder="Enter city"
          />
        </div>
        <div>
          <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Min Price</label>
          <input
            type="number"
            value={filters.min_price || ''}
            onChange={(e) => handleChange('min_price', e.target.value ? Number(e.target.value) : undefined)}
            className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
            placeholder="Min price"
            min="0"
          />
        </div>
        <div>
          <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Max Price</label>
          <input
            type="number"
            value={filters.max_price || ''}
            onChange={(e) => handleChange('max_price', e.target.value ? Number(e.target.value) : undefined)}
            className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
            placeholder="Max price"
            min="0"
          />
        </div>
      </div>

      <div className="mt-6">
        <label className="block text-sm font-semibold text-amber-400 mb-4 elegant-text uppercase tracking-wider">Property Type</label>
        <PropertyTypeSelector
          value={filters.property_type || ''}
          onChange={(value) => handleChange('property_type', value)}
        />
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div 
            className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-6 border-t border-amber-400/20"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
          <div>
            <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Min Rooms</label>
            <input
              type="number"
              value={filters.min_rooms || ''}
              onChange={(e) => handleChange('min_rooms', e.target.value ? Number(e.target.value) : undefined)}
              className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
              placeholder="Min rooms"
              min="1"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Max Rooms</label>
            <input
              type="number"
              value={filters.max_rooms || ''}
              onChange={(e) => handleChange('max_rooms', e.target.value ? Number(e.target.value) : undefined)}
              className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
              placeholder="Max rooms"
              min="1"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Sort By</label>
            <select
              value={filters.ordering || ''}
              onChange={(e) => handleChange('ordering', e.target.value)}
              className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white luxury-border"
            >
              <option value="" className="bg-gray-900">Default</option>
              <option value="price_per_day" className="bg-gray-900">Price: Low to High</option>
              <option value="-price_per_day" className="bg-gray-900">Price: High to Low</option>
              <option value="-created_at" className="bg-gray-900">Newest First</option>
              <option value="average_rating" className="bg-gray-900">Highest Rated</option>
            </select>
          </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default ListingFilters

