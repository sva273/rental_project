import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { listingsApi } from '../../services/listings'
import { motion, AnimatePresence } from 'framer-motion'
import ErrorMessage from '../common/ErrorMessage'

interface AddListingFormProps {
  onClose: () => void
  onSuccess?: () => void
}

const AddListingForm = ({ onClose, onSuccess }: AddListingFormProps) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    country: '',
    city: '',
    street: '',
    house_number: '',
    latitude: '',
    longitude: '',
    price_per_day: '',
    rooms: '',
    floor: '',
    property_type: 'apartment' as 'apartment' | 'house' | 'studio',
    bathroom_type: 'shower' as 'shower' | 'bathtub',
    has_elevator: false,
    has_terrace: false,
    has_balcony: false,
    has_internet: false,
    has_parking: false,
    daily_enabled: true,
    parking_price_per_day: '',
    main_image: null as File | null,
  })
  const [error, setError] = useState('')
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (data: any) => listingsApi.createListing(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['listings'] })
      onSuccess?.()
      onClose()
    },
    onError: (err: any) => {
      const errorMessage = err.response?.data?.detail || 
                          Object.values(err.response?.data || {}).flat()[0] ||
                          'Failed to create listing'
      setError(errorMessage)
    },
  })

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setFormData({ ...formData, main_image: file })
      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    // Create FormData for file upload
    const submitData = new FormData()
    submitData.append('title', formData.title.trim())
    submitData.append('description', formData.description.trim())
    submitData.append('country', formData.country.trim())
    submitData.append('city', formData.city.trim())
    submitData.append('street', formData.street.trim())
    submitData.append('house_number', formData.house_number.trim())
    submitData.append('price_per_day', formData.price_per_day)
    submitData.append('property_type', formData.property_type)
    submitData.append('bathroom_type', formData.bathroom_type)
    submitData.append('daily_enabled', formData.daily_enabled.toString())
    submitData.append('has_elevator', formData.has_elevator.toString())
    submitData.append('has_terrace', formData.has_terrace.toString())
    submitData.append('has_balcony', formData.has_balcony.toString())
    submitData.append('has_internet', formData.has_internet.toString())
    submitData.append('has_parking', formData.has_parking.toString())

    if (formData.rooms) {
      submitData.append('rooms', formData.rooms)
    }
    if (formData.floor) {
      submitData.append('floor', formData.floor)
    }
    if (formData.latitude && formData.longitude) {
      submitData.append('latitude', formData.latitude)
      submitData.append('longitude', formData.longitude)
    }
    if (formData.parking_price_per_day) {
      submitData.append('parking_price_per_day', formData.parking_price_per_day)
    }
    if (formData.main_image) {
      submitData.append('main_image', formData.main_image)
    }

    mutation.mutate(submitData)
  }

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          className="glass-dark rounded-3xl premium-shadow p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto luxury-border"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-black gradient-text" style={{ fontFamily: "'Playfair Display', serif" }}>
              Add New Listing
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {error && <ErrorMessage message={error} />}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                Title *
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                placeholder="Luxury Apartment in City Center"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                Description *
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={4}
                className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                placeholder="Describe your property..."
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  Country *
                </label>
                <input
                  type="text"
                  value={formData.country}
                  onChange={(e) => setFormData({ ...formData, country: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="Country"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  City *
                </label>
                <input
                  type="text"
                  value={formData.city}
                  onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="City"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  Street *
                </label>
                <input
                  type="text"
                  value={formData.street}
                  onChange={(e) => setFormData({ ...formData, street: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="Street"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  House Number *
                </label>
                <input
                  type="text"
                  value={formData.house_number}
                  onChange={(e) => setFormData({ ...formData, house_number: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="123"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  Price per Day *
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.price_per_day}
                  onChange={(e) => setFormData({ ...formData, price_per_day: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="100"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  Rooms
                </label>
                <input
                  type="number"
                  min="1"
                  value={formData.rooms}
                  onChange={(e) => setFormData({ ...formData, rooms: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="2"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  Floor
                </label>
                <input
                  type="number"
                  min="0"
                  value={formData.floor}
                  onChange={(e) => setFormData({ ...formData, floor: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="5"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">
                Property Type *
              </label>
              <div className="flex flex-wrap gap-3">
                {[
                  { value: 'apartment', label: 'Apartment' },
                  { value: 'house', label: 'House' },
                  { value: 'studio', label: 'Studio' },
                ].map((type) => (
                  <motion.button
                    key={type.value}
                    type="button"
                    onClick={() => setFormData({ ...formData, property_type: type.value as any })}
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className={`px-6 py-3 rounded-xl font-semibold transition-all luxury-border ${
                      formData.property_type === type.value
                        ? 'luxury-gradient text-black shadow-lg glow-effect'
                        : 'glass-dark text-amber-400 hover:bg-amber-400/10'
                    }`}
                  >
                    {type.label}
                  </motion.button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">
                Bathroom Type
              </label>
              <div className="flex flex-wrap gap-3">
                {[
                  { value: 'shower', label: 'Shower' },
                  { value: 'bathtub', label: 'Bathtub' },
                ].map((type) => (
                  <motion.button
                    key={type.value}
                    type="button"
                    onClick={() => setFormData({ ...formData, bathroom_type: type.value as any })}
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className={`px-6 py-3 rounded-xl font-semibold transition-all luxury-border ${
                      formData.bathroom_type === type.value
                        ? 'luxury-gradient text-black shadow-lg glow-effect'
                        : 'glass-dark text-amber-400 hover:bg-amber-400/10'
                    }`}
                  >
                    {type.label}
                  </motion.button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  Latitude (optional)
                </label>
                <input
                  type="number"
                  step="0.000001"
                  value={formData.latitude}
                  onChange={(e) => setFormData({ ...formData, latitude: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="40.7128"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  Longitude (optional)
                </label>
                <input
                  type="number"
                  step="0.000001"
                  value={formData.longitude}
                  onChange={(e) => setFormData({ ...formData, longitude: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="-74.0060"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">
                Amenities
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div className="flex items-center gap-3 p-3 glass-dark rounded-xl luxury-border">
                  <input
                    type="checkbox"
                    id="has_elevator"
                    checked={formData.has_elevator}
                    onChange={(e) => setFormData({ ...formData, has_elevator: e.target.checked })}
                    className="w-5 h-5 luxury-gradient rounded focus:ring-amber-400 cursor-pointer"
                  />
                  <label htmlFor="has_elevator" className="text-white font-semibold elegant-text cursor-pointer text-sm">
                    Elevator
                  </label>
                </div>
                <div className="flex items-center gap-3 p-3 glass-dark rounded-xl luxury-border">
                  <input
                    type="checkbox"
                    id="has_terrace"
                    checked={formData.has_terrace}
                    onChange={(e) => setFormData({ ...formData, has_terrace: e.target.checked })}
                    className="w-5 h-5 luxury-gradient rounded focus:ring-amber-400 cursor-pointer"
                  />
                  <label htmlFor="has_terrace" className="text-white font-semibold elegant-text cursor-pointer text-sm">
                    Terrace
                  </label>
                </div>
                <div className="flex items-center gap-3 p-3 glass-dark rounded-xl luxury-border">
                  <input
                    type="checkbox"
                    id="has_balcony"
                    checked={formData.has_balcony}
                    onChange={(e) => setFormData({ ...formData, has_balcony: e.target.checked })}
                    className="w-5 h-5 luxury-gradient rounded focus:ring-amber-400 cursor-pointer"
                  />
                  <label htmlFor="has_balcony" className="text-white font-semibold elegant-text cursor-pointer text-sm">
                    Balcony
                  </label>
                </div>
                <div className="flex items-center gap-3 p-3 glass-dark rounded-xl luxury-border">
                  <input
                    type="checkbox"
                    id="has_internet"
                    checked={formData.has_internet}
                    onChange={(e) => setFormData({ ...formData, has_internet: e.target.checked })}
                    className="w-5 h-5 luxury-gradient rounded focus:ring-amber-400 cursor-pointer"
                  />
                  <label htmlFor="has_internet" className="text-white font-semibold elegant-text cursor-pointer text-sm">
                    Internet
                  </label>
                </div>
                <div className="flex items-center gap-3 p-3 glass-dark rounded-xl luxury-border">
                  <input
                    type="checkbox"
                    id="has_parking"
                    checked={formData.has_parking}
                    onChange={(e) => setFormData({ ...formData, has_parking: e.target.checked })}
                    className="w-5 h-5 luxury-gradient rounded focus:ring-amber-400 cursor-pointer"
                  />
                  <label htmlFor="has_parking" className="text-white font-semibold elegant-text cursor-pointer text-sm">
                    Parking
                  </label>
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                Parking Price per Day
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={formData.parking_price_per_day}
                onChange={(e) => setFormData({ ...formData, parking_price_per_day: e.target.value })}
                className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                placeholder="10"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                Main Image
              </label>
              <div className="space-y-4">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-amber-400/20 file:text-amber-400 hover:file:bg-amber-400/30 file:cursor-pointer luxury-border"
                />
                {imagePreview && (
                  <div className="relative">
                    <img
                      src={imagePreview}
                      alt="Preview"
                      className="w-full h-64 object-cover rounded-xl luxury-border"
                    />
                    <button
                      type="button"
                      onClick={() => {
                        setFormData({ ...formData, main_image: null })
                        setImagePreview(null)
                      }}
                      className="absolute top-2 right-2 px-3 py-1 glass-dark text-red-400 rounded-lg hover:bg-red-400/10 transition-all font-semibold luxury-border"
                    >
                      Remove
                    </button>
                  </div>
                )}
              </div>
            </div>

            <div className="flex items-center gap-3 p-4 glass-dark rounded-xl luxury-border">
              <input
                type="checkbox"
                id="daily_enabled"
                checked={formData.daily_enabled}
                onChange={(e) => setFormData({ ...formData, daily_enabled: e.target.checked })}
                className="w-5 h-5 luxury-gradient rounded focus:ring-amber-400 cursor-pointer"
              />
              <label htmlFor="daily_enabled" className="text-white font-semibold elegant-text cursor-pointer">
                Enable daily bookings
              </label>
            </div>

            <div className="flex gap-4 pt-4">
              <motion.button
                type="submit"
                disabled={mutation.isPending}
                whileHover={{ scale: mutation.isPending ? 1 : 1.02 }}
                whileTap={{ scale: mutation.isPending ? 1 : 0.98 }}
                className="flex-1 px-8 py-4 luxury-gradient text-black rounded-xl transition-all shadow-lg glow-effect font-bold disabled:opacity-50"
              >
                {mutation.isPending ? 'Creating...' : 'Create Listing'}
              </motion.button>
              <motion.button
                type="button"
                onClick={onClose}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex-1 px-8 py-4 glass-dark text-amber-400 rounded-xl hover:bg-amber-400/10 transition-all font-semibold luxury-border"
              >
                Cancel
              </motion.button>
            </div>
          </form>
        </motion.div>
      </div>
    </AnimatePresence>
  )
}

export default AddListingForm

