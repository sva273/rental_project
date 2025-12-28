import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { reviewsApi, Review } from '../services/reviews'
import ReviewCard from '../components/reviews/ReviewCard'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ErrorMessage from '../components/common/ErrorMessage'
import { useAuthStore } from '../store/authStore'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

const ReviewsPage = () => {
  const { isAuthenticated, user } = useAuthStore()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [editingReview, setEditingReview] = useState<Review | null>(null)

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['reviews'],
    queryFn: () => reviewsApi.getReviews(),
    enabled: isAuthenticated,
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => reviewsApi.deleteReview(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews'] })
    },
  })

  if (!isAuthenticated) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 mb-4">Please login to view reviews</p>
        <button
          onClick={() => navigate('/login')}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Login
        </button>
      </div>
    )
  }

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (error) {
    return (
      <ErrorMessage
        message="Failed to load reviews"
        onRetry={() => refetch()}
      />
    )
  }

  const reviews = data?.results || []

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold text-white mb-2 drop-shadow-lg">Reviews</h1>
        <p className="text-white/90">Read what others have to say</p>
      </div>

      {reviews.length === 0 ? (
        <div className="glass rounded-3xl shadow-2xl p-12 text-center border border-white/20">
          <div className="w-24 h-24 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-12 h-12 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
          </div>
          <p className="text-gray-700 text-xl font-semibold mb-2">No reviews yet</p>
          <p className="text-gray-600">Reviews will appear here once they are submitted</p>
        </div>
      ) : (
        <div className="space-y-6">
          {reviews.map((review) => (
            <ReviewCard
              key={review.id}
              review={review}
              canEdit={review.tenant === user?.id}
              onDelete={(id) => deleteMutation.mutate(id)}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default ReviewsPage

