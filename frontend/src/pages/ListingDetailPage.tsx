import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { listingsApi } from '../services/listings'
import { reviewsApi } from '../services/reviews'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ErrorMessage from '../components/common/ErrorMessage'
import BookingForm from '../components/bookings/BookingForm'
import ReviewCard from '../components/reviews/ReviewCard'
import { useAuthStore } from '../store/authStore'

const ListingDetailPage = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()

  const { data: listing, isLoading, error, refetch } = useQuery({
    queryKey: ['listing', id],
    queryFn: () => listingsApi.getListing(Number(id)),
    enabled: !!id,
  })

  const { data: reviewsData } = useQuery({
    queryKey: ['reviews', id],
    queryFn: () => reviewsApi.getReviews(Number(id)),
    enabled: !!id && isAuthenticated,
  })

  const reviews = reviewsData?.results?.filter((review) => review.listing === Number(id)) || []

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (error || !listing) {
    return (
      <div className="max-w-4xl mx-auto">
        <ErrorMessage
          message="Listing not found or failed to load"
          onRetry={() => refetch()}
        />
        <button
          onClick={() => navigate('/')}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Back to Listings
        </button>
      </div>
    )
  }

  const defaultImage = 'https://via.placeholder.com/800x400?text=No+Image'

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <button
        onClick={() => navigate('/')}
        className="mb-6 px-4 py-2 glass rounded-xl hover:bg-white/80 transition-all flex items-center gap-2 text-gray-700 font-medium"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Listings
      </button>

      <div className="glass rounded-3xl shadow-2xl overflow-hidden border border-white/20">
        <div className="relative h-[500px] overflow-hidden">
          <img
            src={listing.main_image || defaultImage}
            alt={listing.title}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.currentTarget.src = defaultImage
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
          <div className="absolute bottom-8 left-8 right-8">
            <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-2 drop-shadow-lg">
              {listing.title}
            </h1>
            <p className="text-white/90 text-lg flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {listing.full_address}
            </p>
          </div>
        </div>

        <div className="p-8 bg-white/95">
          <div className="flex items-start justify-between mb-8">
            <div className="flex-1">
              {listing.average_rating > 0 && (
                <div className="flex items-center gap-2 mb-4">
                  <div className="flex items-center">
                    <svg className="w-6 h-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                    <span className="text-2xl font-bold ml-2">{listing.average_rating.toFixed(1)}</span>
                  </div>
                  <span className="text-gray-500">({listing.reviews_count} {listing.reviews_count === 1 ? 'review' : 'reviews'})</span>
                </div>
              )}
            </div>
            <div className="text-right">
              <div className="text-4xl font-extrabold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                ${listing.price_per_day}
                <span className="text-xl text-gray-500 font-normal">/night</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="mb-8">
                <h2 className="text-3xl font-bold mb-4 text-gray-900">About this place</h2>
                <p className="text-gray-700 leading-relaxed text-lg">{listing.description}</p>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                {listing.rooms && (
                  <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-5 rounded-xl border border-purple-100">
                    <div className="text-gray-600 text-sm mb-2 font-medium">Rooms</div>
                    <div className="text-2xl font-bold text-purple-600">{listing.rooms}</div>
                  </div>
                )}
                {listing.floor && (
                  <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-5 rounded-xl border border-purple-100">
                    <div className="text-gray-600 text-sm mb-2 font-medium">Floor</div>
                    <div className="text-2xl font-bold text-purple-600">{listing.floor}</div>
                  </div>
                )}
                <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-5 rounded-xl border border-purple-100">
                  <div className="text-gray-600 text-sm mb-2 font-medium">Property Type</div>
                  <div className="text-xl font-bold text-purple-600 capitalize">{listing.property_type}</div>
                </div>
                <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-5 rounded-xl border border-purple-100">
                  <div className="text-gray-600 text-sm mb-2 font-medium">Bathroom</div>
                  <div className="text-xl font-bold text-purple-600 capitalize">{listing.bathroom_type}</div>
                </div>
              </div>

              <div className="mb-8">
                <h3 className="text-2xl font-bold mb-6 text-gray-900">Amenities</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {listing.has_internet && (
                    <div className="flex items-center gap-3 p-4 bg-white rounded-xl border border-gray-200 hover:border-purple-300 transition-colors">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="font-semibold text-gray-700">WiFi</span>
                    </div>
                  )}
                  {listing.has_parking && (
                    <div className="flex items-center gap-3 p-4 bg-white rounded-xl border border-gray-200 hover:border-purple-300 transition-colors">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="font-semibold text-gray-700">Parking</span>
                    </div>
                  )}
                  {listing.has_elevator && (
                    <div className="flex items-center gap-3 p-4 bg-white rounded-xl border border-gray-200 hover:border-purple-300 transition-colors">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="font-semibold text-gray-700">Elevator</span>
                    </div>
                  )}
                  {listing.has_balcony && (
                    <div className="flex items-center gap-3 p-4 bg-white rounded-xl border border-gray-200 hover:border-purple-300 transition-colors">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="font-semibold text-gray-700">Balcony</span>
                    </div>
                  )}
                  {listing.has_terrace && (
                    <div className="flex items-center gap-3 p-4 bg-white rounded-xl border border-gray-200 hover:border-purple-300 transition-colors">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="font-semibold text-gray-700">Terrace</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div className="lg:col-span-1">
              {isAuthenticated && listing.is_active && listing.daily_enabled ? (
                <div className="sticky top-4">
                  <BookingForm listingId={listing.id} pricePerDay={Number(listing.price_per_day)} />
                </div>
              ) : (
                <div className="glass p-8 rounded-2xl border border-white/20 shadow-xl">
                  {!isAuthenticated ? (
                    <div className="text-center">
                      <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-indigo-500 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                      </div>
                      <p className="text-gray-700 mb-6 font-medium">Please login to book this listing</p>
                      <button
                        onClick={() => navigate('/login')}
                        className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl hover:from-purple-700 hover:to-indigo-700 transition-all shadow-lg font-semibold"
                      >
                        Sign In to Book
                      </button>
                    </div>
                  ) : !listing.is_active ? (
                    <div className="text-center">
                      <p className="text-gray-600 font-medium">This listing is currently unavailable</p>
                    </div>
                  ) : (
                    <div className="text-center">
                      <p className="text-gray-600 font-medium">Daily booking is not enabled for this listing</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Reviews Section */}
        {reviews.length > 0 && (
          <div className="mt-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Reviews ({reviews.length})</h2>
            <div className="space-y-4">
              {reviews.map((review) => (
                <ReviewCard key={review.id} review={review} />
              ))}
            </div>
          </div>
        )}
        {isAuthenticated && reviews.length === 0 && listing.reviews_count > 0 && (
          <div className="mt-12 glass rounded-2xl p-6 border border-white/20">
            <p className="text-gray-600 text-center">Reviews are being moderated and will appear here once approved.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default ListingDetailPage

