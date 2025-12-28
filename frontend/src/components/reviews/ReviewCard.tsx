import { Review } from '../../services/reviews'

interface ReviewCardProps {
  review: Review
  onEdit?: (review: Review) => void
  onDelete?: (id: number) => void
  canEdit?: boolean
}

const ReviewCard = ({ review, onEdit, onDelete, canEdit }: ReviewCardProps) => {
  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <svg
        key={i}
        className={`w-6 h-6 ${i < rating ? 'text-amber-400' : 'text-gray-600'}`}
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
      </svg>
    ))
  }

  return (
    <div className="glass-dark rounded-3xl premium-shadow p-8 luxury-border border-amber-400/30">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-amber-400 to-yellow-500 rounded-full flex items-center justify-center text-black font-black text-lg">
              {review.tenant_email?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div>
              <p className="font-bold text-white elegant-text text-lg">{review.tenant_email}</p>
              <p className="text-sm text-gray-400 elegant-text">
                {new Date(review.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 mb-4">
            {renderStars(review.rating)}
            <span className="text-xl font-black text-amber-400 elegant-text">{review.rating}.0</span>
          </div>
          <p className="text-gray-300 leading-relaxed elegant-text text-base">{review.comment}</p>
        </div>
        {canEdit && (onEdit || onDelete) && (
          <div className="flex gap-2 ml-4">
            {onEdit && (
              <button
                onClick={() => onEdit(review)}
                className="px-4 py-2 text-sm luxury-gradient text-black rounded-lg hover:shadow-lg glow-effect transition-all font-bold"
              >
                Edit
              </button>
            )}
            {onDelete && (
              <button
                onClick={() => {
                  if (confirm('Are you sure you want to delete this review?')) {
                    onDelete(review.id)
                  }
                }}
                className="px-4 py-2 text-sm glass-dark text-red-400 rounded-lg hover:bg-red-500/20 transition-all font-semibold luxury-border border-red-400/30"
              >
                Delete
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default ReviewCard

