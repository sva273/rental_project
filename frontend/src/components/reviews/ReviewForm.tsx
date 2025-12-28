import { useState } from 'react'
import { motion } from 'framer-motion'
import { CreateReviewData } from '../../services/reviews'

interface ReviewFormProps {
  listingId: number
  listingTitle: string
  onSubmit: (data: CreateReviewData) => Promise<void>
  onCancel: () => void
  isLoading?: boolean
  error?: string
}

const ReviewForm = ({ listingId, listingTitle, onSubmit, onCancel, isLoading, error: externalError }: ReviewFormProps) => {
  const [rating, setRating] = useState(5)
  const [comment, setComment] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!comment.trim()) {
      setError('Please enter a comment')
      return
    }

    if (rating < 1 || rating > 5) {
      setError('Please select a rating')
      return
    }

    try {
      await onSubmit({
        listing: listingId,
        rating,
        comment: comment.trim(),
      })
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to submit review. Please try again.')
    }
  }

  const displayError = error || externalError

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="glass-dark rounded-2xl p-6 luxury-border border-amber-400/30 mt-6"
    >
      <h4 className="text-xl font-bold text-white mb-4 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
        Leave a Review for {listingTitle}
      </h4>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Rating */}
        <div>
          <label className="block text-gray-300 mb-2 elegant-text font-semibold">Rating</label>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                onClick={() => setRating(star)}
                className={`w-12 h-12 rounded-xl transition-all ${
                  star <= rating
                    ? 'luxury-gradient text-black shadow-lg glow-effect'
                    : 'glass-dark text-gray-400 border border-gray-400/30'
                }`}
              >
                <svg className="w-6 h-6 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </button>
            ))}
          </div>
        </div>

        {/* Comment */}
        <div>
          <label className="block text-gray-300 mb-2 elegant-text font-semibold">Your Review</label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows={4}
            className="w-full glass-dark rounded-xl p-4 text-white placeholder-gray-500 border border-amber-400/20 focus:border-amber-400/50 focus:outline-none focus:ring-2 focus:ring-amber-400/30 transition-all elegant-text"
            placeholder="Share your experience..."
            required
          />
        </div>

        {displayError && (
          <div className="text-red-400 text-sm elegant-text bg-red-400/10 rounded-lg p-3 border border-red-400/30">
            {displayError}
          </div>
        )}

        {/* Buttons */}
        <div className="flex gap-4 pt-2">
          <motion.button
            type="submit"
            disabled={isLoading}
            whileHover={{ scale: isLoading ? 1 : 1.02 }}
            whileTap={{ scale: isLoading ? 1 : 0.98 }}
            className="flex-1 px-6 py-3 luxury-gradient text-black rounded-xl hover:shadow-lg glow-effect disabled:opacity-50 transition-all font-bold"
          >
            {isLoading ? 'Submitting...' : 'Submit Review'}
          </motion.button>
          <motion.button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            whileHover={{ scale: isLoading ? 1 : 1.02 }}
            whileTap={{ scale: isLoading ? 1 : 0.98 }}
            className="px-6 py-3 glass-dark text-gray-400 rounded-xl hover:bg-gray-400/10 disabled:opacity-50 transition-all font-semibold luxury-border border-gray-400/30"
          >
            Cancel
          </motion.button>
        </div>
      </form>
    </motion.div>
  )
}

export default ReviewForm

