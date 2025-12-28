import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { bookingsApi } from '../services/bookings'
import { reviewsApi, Review } from '../services/reviews'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ErrorMessage from '../components/common/ErrorMessage'
import AnimatedSection from '../components/common/AnimatedSection'
import ReviewForm from '../components/reviews/ReviewForm'
import { useAuthStore } from '../store/authStore'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

const BookingsPage = () => {
  const { isAuthenticated, user } = useAuthStore()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [showReviewForm, setShowReviewForm] = useState<number | null>(null)

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['bookings'],
    queryFn: () => bookingsApi.getBookings(),
    enabled: isAuthenticated,
  })

  const cancelMutation = useMutation({
    mutationFn: (id: number) => bookingsApi.cancelBooking(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bookings'] })
    },
  })

  const confirmMutation = useMutation({
    mutationFn: (id: number) => bookingsApi.confirmBooking(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bookings'] })
    },
  })

  const rejectMutation = useMutation({
    mutationFn: (id: number) => bookingsApi.rejectBooking(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bookings'] })
    },
  })

  const { data: reviewsData } = useQuery({
    queryKey: ['reviews'],
    queryFn: () => reviewsApi.getReviews(),
    enabled: isAuthenticated && (user?.role === 'tenant' || !user?.role),
  })

  const createReviewMutation = useMutation({
    mutationFn: (data: { listing: number; rating: number; comment: string }) =>
      reviewsApi.createReview(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews'] })
      queryClient.invalidateQueries({ queryKey: ['bookings'] })
      setShowReviewForm(null)
    },
  })

  const isLandlord = user?.role === 'landlord'
  const isTenant = user?.role === 'tenant'

  // Check if booking is completed and tenant can leave a review
  const canLeaveReview = (booking: any) => {
    if (!isTenant) return false
    if (booking.status !== 'confirmed') return false
    
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const endDate = new Date(booking.end_date)
    endDate.setHours(0, 0, 0, 0)
    
    if (endDate >= today) return false // Booking hasn't ended yet
    
    // Check if review already exists
    const existingReview = reviewsData?.results?.find(
      (review: Review) => review.listing === booking.listing
    )
    
    return !existingReview
  }

  if (!isAuthenticated) {
    return (
      <div className="text-center py-20">
        <div className="glass-dark rounded-3xl p-12 luxury-border max-w-md mx-auto">
          <p className="text-amber-400 mb-6 text-lg elegant-text">Please login to view your bookings</p>
          <motion.button
            onClick={() => navigate('/login')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-3 luxury-gradient text-black rounded-xl hover:shadow-lg glow-effect inline-block font-bold"
          >
            Sign In
          </motion.button>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (error) {
    return (
      <ErrorMessage
        message="Failed to load bookings"
        onRetry={() => refetch()}
      />
    )
  }

  const bookings = data?.results || []

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed':
        return 'luxury-gradient text-black shadow-lg glow-effect'
      case 'pending':
        return 'glass-dark text-amber-400 border-amber-400/30 luxury-border'
      case 'cancelled':
        return 'glass-dark text-gray-400 border-gray-400/30 luxury-border'
      case 'rejected':
        return 'glass-dark text-red-400 border-red-400/30 luxury-border'
      default:
        return 'glass-dark text-gray-400 border-gray-400/30 luxury-border'
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <AnimatedSection delay={0.1}>
        <div className="mb-10 text-center">
          <h1 className="text-6xl font-black gradient-text mb-4" style={{ fontFamily: "'Playfair Display', serif" }}>
            {isLandlord ? 'Property Bookings' : 'My Bookings'}
          </h1>
          <p className="text-gray-400 text-lg elegant-text">
            {isLandlord ? 'Manage bookings for your properties' : 'Manage your exclusive reservations'}
          </p>
        </div>
      </AnimatedSection>

      {bookings.length === 0 ? (
        <AnimatedSection delay={0.2}>
          <div className="glass-dark rounded-3xl premium-shadow p-16 text-center luxury-border">
            <motion.div 
              className="w-32 h-32 luxury-gradient rounded-full flex items-center justify-center mx-auto mb-8 shadow-2xl glow-effect"
              whileHover={{ rotate: 10, scale: 1.05 }}
              transition={{ duration: 0.5 }}
            >
              <svg className="w-16 h-16 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </motion.div>
            <h2 className="text-3xl font-black text-white mb-4 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
              No bookings yet
            </h2>
            <p className="text-gray-400 mb-8 text-lg elegant-text">Start exploring our premium residences</p>
            <motion.button
              onClick={() => navigate('/')}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-10 py-4 luxury-gradient text-black rounded-xl transition-all shadow-lg glow-effect font-bold"
            >
              Browse Residences
            </motion.button>
          </div>
        </AnimatedSection>
      ) : (
        <div className="space-y-6">
          {bookings.map((booking, index) => (
            <AnimatedSection key={booking.id} delay={0.1 + index * 0.05}>
              <motion.div 
                className="glass-dark rounded-3xl premium-shadow p-8 luxury-border"
                whileHover={{ scale: 1.01, y: -5 }}
                transition={{ duration: 0.3 }}
              >
                <div className="flex flex-col md:flex-row justify-between items-start gap-6 mb-6">
                  <div className="flex-1">
                    <h3 className="text-3xl font-black text-white mb-4 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
                      {booking.listing_title}
                    </h3>
                    <div className="flex flex-wrap gap-6 text-gray-300">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 glass-dark rounded-xl flex items-center justify-center luxury-border">
                          <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                        </div>
                        <span className="font-semibold elegant-text">
                          {new Date(booking.start_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })} - {new Date(booking.end_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                        </span>
                      </div>
                      {booking.parking_included && (
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 luxury-gradient rounded-xl flex items-center justify-center shadow-md glow-effect">
                            <svg className="w-5 h-5 text-black" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                          </div>
                          <span className="font-semibold text-amber-400 elegant-text">Parking included</span>
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="text-right">
                    <motion.span 
                      className={`inline-block px-6 py-3 rounded-xl text-sm font-bold mb-4 border ${getStatusColor(booking.status)}`}
                      whileHover={{ scale: 1.05 }}
                    >
                      {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                    </motion.span>
                    <div className="text-4xl font-black gradient-text" style={{ fontFamily: "'Playfair Display', serif" }}>
                      ${booking.total_price}
                    </div>
                    <p className="text-gray-400 text-sm mt-2 elegant-text">Total amount</p>
                  </div>
                </div>
                {booking.status === 'pending' && (
                  <div className="flex gap-4 mt-6 pt-6 border-t border-amber-400/20">
                    {isLandlord ? (
                      <>
                        <motion.button
                          onClick={() => {
                            if (confirm('Are you sure you want to confirm this booking?')) {
                              confirmMutation.mutate(booking.id)
                            }
                          }}
                          disabled={confirmMutation.isPending || rejectMutation.isPending}
                          whileHover={{ scale: confirmMutation.isPending ? 1 : 1.02 }}
                          whileTap={{ scale: confirmMutation.isPending ? 1 : 0.98 }}
                          className="flex-1 px-8 py-4 luxury-gradient text-black rounded-xl hover:shadow-lg glow-effect disabled:opacity-50 transition-all font-bold"
                        >
                          {confirmMutation.isPending ? 'Confirming...' : 'Confirm Booking'}
                        </motion.button>
                        <motion.button
                          onClick={() => {
                            if (confirm('Are you sure you want to reject this booking?')) {
                              rejectMutation.mutate(booking.id)
                            }
                          }}
                          disabled={confirmMutation.isPending || rejectMutation.isPending}
                          whileHover={{ scale: rejectMutation.isPending ? 1 : 1.02 }}
                          whileTap={{ scale: rejectMutation.isPending ? 1 : 0.98 }}
                          className="flex-1 px-8 py-4 glass-dark text-red-400 rounded-xl hover:bg-red-400/10 disabled:opacity-50 transition-all font-semibold luxury-border border-red-400/30"
                        >
                          {rejectMutation.isPending ? 'Rejecting...' : 'Reject Booking'}
                        </motion.button>
                      </>
                    ) : (
                      <motion.button
                        onClick={() => {
                          if (confirm('Are you sure you want to cancel this booking?')) {
                            cancelMutation.mutate(booking.id)
                          }
                        }}
                        disabled={cancelMutation.isPending}
                        whileHover={{ scale: cancelMutation.isPending ? 1 : 1.02 }}
                        whileTap={{ scale: cancelMutation.isPending ? 1 : 0.98 }}
                        className="px-8 py-4 glass-dark text-red-400 rounded-xl hover:bg-red-400/10 disabled:opacity-50 transition-all font-semibold luxury-border border-red-400/30"
                      >
                        {cancelMutation.isPending ? 'Cancelling...' : 'Cancel Booking'}
                      </motion.button>
                    )}
                  </div>
                )}
                {/* Review form for completed bookings */}
                {isTenant && canLeaveReview(booking) && (
                  <AnimatePresence>
                    {showReviewForm === booking.id ? (
                      <ReviewForm
                        listingId={booking.listing}
                        listingTitle={booking.listing_title}
                        onSubmit={async (data) => {
                          await createReviewMutation.mutateAsync(data)
                        }}
                        onCancel={() => setShowReviewForm(null)}
                        isLoading={createReviewMutation.isPending}
                        error={createReviewMutation.error ? (createReviewMutation.error as any)?.response?.data?.detail || 'Failed to create review' : undefined}
                      />
                    ) : (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="mt-6 pt-6 border-t border-amber-400/20"
                      >
                        <motion.button
                          onClick={() => setShowReviewForm(booking.id)}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          className="w-full px-8 py-4 luxury-gradient text-black rounded-xl hover:shadow-lg glow-effect transition-all font-bold"
                        >
                          Leave a Review
                        </motion.button>
                      </motion.div>
                    )}
                  </AnimatePresence>
                )}
                {/* Show existing review if exists */}
                {isTenant && !canLeaveReview(booking) && booking.status === 'confirmed' && (() => {
                  const existingReview = reviewsData?.results?.find(
                    (review: Review) => review.listing === booking.listing
                  )
                  if (existingReview) {
                    return (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-6 pt-6 border-t border-amber-400/20"
                      >
                        <div className="glass-dark rounded-xl p-4 luxury-border border-amber-400/30">
                          <div className="flex items-center gap-3 mb-2">
                            <div className="flex gap-1">
                              {[1, 2, 3, 4, 5].map((star) => (
                                <svg
                                  key={star}
                                  className={`w-5 h-5 ${
                                    star <= existingReview.rating
                                      ? 'text-amber-400'
                                      : 'text-gray-500'
                                  }`}
                                  fill="currentColor"
                                  viewBox="0 0 20 20"
                                >
                                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                              ))}
                            </div>
                            <span className="text-gray-300 elegant-text font-semibold">
                              Your Review
                            </span>
                          </div>
                          <p className="text-gray-300 elegant-text">{existingReview.comment}</p>
                          <p className="text-gray-500 text-sm mt-2 elegant-text">
                            {new Date(existingReview.created_at).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric',
                            })}
                          </p>
                        </div>
                      </motion.div>
                    )
                  }
                  return null
                })()}
              </motion.div>
            </AnimatedSection>
          ))}
        </div>
      )}
    </div>
  )
}

export default BookingsPage

