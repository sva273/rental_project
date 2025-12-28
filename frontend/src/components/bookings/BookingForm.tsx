import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { bookingsApi } from '../../services/bookings'
import { CreateBookingData } from '../../types/booking'
import ErrorMessage from '../common/ErrorMessage'
import { motion } from 'framer-motion'

interface BookingFormProps {
  listingId: number
  pricePerDay: number
}

const BookingForm = ({ listingId, pricePerDay }: BookingFormProps) => {
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [parkingIncluded, setParkingIncluded] = useState(false)
  const [error, setError] = useState('')

  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (data: CreateBookingData) => bookingsApi.createBooking(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bookings'] })
      setError('')
      alert('Booking created successfully!')
      setStartDate('')
      setEndDate('')
      setParkingIncluded(false)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || 'Failed to create booking')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!startDate || !endDate) {
      setError('Please select both start and end dates')
      return
    }

    if (new Date(startDate) >= new Date(endDate)) {
      setError('End date must be after start date')
      return
    }

    const bookingData: CreateBookingData = {
      listing: listingId,
      start_date: startDate,
      end_date: endDate,
      parking_included: parkingIncluded,
    }

    mutation.mutate(bookingData)
  }

  const calculateDays = () => {
    if (!startDate || !endDate) return 0
    const start = new Date(startDate)
    const end = new Date(endDate)
    const diffTime = Math.abs(end.getTime() - start.getTime())
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  }

  const days = calculateDays()
  const totalPrice = days * pricePerDay
  const minDate = new Date().toISOString().split('T')[0]

  return (
    <motion.div 
      className="glass-dark rounded-3xl premium-shadow p-8 luxury-border"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="mb-8">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-14 h-14 luxury-gradient rounded-xl flex items-center justify-center glow-effect">
            <svg className="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <h3 className="text-3xl font-black text-white elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
              Reserve Your Stay
            </h3>
            <p className="text-gray-400 text-sm elegant-text">Select your dates to see pricing</p>
          </div>
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {error && <ErrorMessage message={error} />}

        <div>
          <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Check-in</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            min={minDate}
            className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Check-out</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            min={startDate || minDate}
            className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
            required
          />
        </div>

        <div className="flex items-center gap-3 p-4 glass-dark rounded-xl luxury-border">
          <input
            type="checkbox"
            id="parking"
            checked={parkingIncluded}
            onChange={(e) => setParkingIncluded(e.target.checked)}
            className="w-5 h-5 luxury-gradient rounded focus:ring-amber-400 cursor-pointer"
          />
          <label htmlFor="parking" className="text-white font-semibold elegant-text cursor-pointer">
            Include parking
          </label>
        </div>

        {days > 0 && (
          <motion.div 
            className="border-t border-amber-400/20 pt-6 space-y-4 glass-dark p-6 rounded-2xl luxury-border"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div className="flex justify-between text-sm text-gray-300 elegant-text">
              <span>${pricePerDay} x {days} night{days !== 1 ? 's' : ''}</span>
              <span className="font-semibold text-amber-400">${totalPrice.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center pt-4 border-t border-amber-400/10">
              <span className="text-xl font-bold text-white elegant-text">Total</span>
              <span className="text-3xl font-black gradient-text" style={{ fontFamily: "'Playfair Display', serif" }}>
                ${totalPrice.toFixed(2)}
              </span>
            </div>
          </motion.div>
        )}

        <motion.button
          type="submit"
          disabled={mutation.isPending || !startDate || !endDate}
          whileHover={{ scale: mutation.isPending || !startDate || !endDate ? 1 : 1.02 }}
          whileTap={{ scale: mutation.isPending || !startDate || !endDate ? 1 : 0.98 }}
          className="w-full px-8 py-4 luxury-gradient text-black rounded-xl font-bold disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg glow-effect"
        >
          {mutation.isPending ? (
            <span className="flex items-center justify-center gap-3">
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Booking...</span>
            </span>
          ) : (
            'Reserve Now'
          )}
        </motion.button>
      </form>
    </motion.div>
  )
}

export default BookingForm

