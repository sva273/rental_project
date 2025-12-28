import { useQuery } from '@tanstack/react-query'
import { listingsApi } from '../services/listings'
import { authApi } from '../services/auth'
import ListingCard from '../components/listings/ListingCard'
import ListingFilters from '../components/listings/ListingFilters'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ErrorMessage from '../components/common/ErrorMessage'
import Pagination from '../components/common/Pagination'
import AnimatedSection from '../components/common/AnimatedSection'
import AnimatedCard from '../components/common/AnimatedCard'
import AddListingForm from '../components/listings/AddListingForm'
import { motion } from 'framer-motion'
import { useState } from 'react'
import { ListingFilters as Filters } from '../types/listing'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

const HomePage = () => {
  const { user, isAuthenticated, setUser } = useAuthStore()
  const [filters, setFilters] = useState<Filters>({})
  const [page, setPage] = useState(1)
  const [showAddForm, setShowAddForm] = useState(false)
  const pageSize = 12

  // Загружаем данные пользователя, если их нет в store
  const { data: userData } = useQuery({
    queryKey: ['profile'],
    queryFn: () => authApi.getCurrentUser(),
    enabled: isAuthenticated && !user,
    onSuccess: (data) => {
      setUser(data)
    },
  })

  // Используем данные из запроса или из store
  const currentUser = userData || user

  // Проверяем, является ли пользователь landlord
  const isLandlord = currentUser?.role === 'landlord' || currentUser?.role === 'LANDLORD'
  
  // Отладка
  console.log('HomePage - isAuthenticated:', isAuthenticated)
  console.log('HomePage - user from store:', user)
  console.log('HomePage - userData from query:', userData)
  console.log('HomePage - currentUser:', currentUser)
  console.log('HomePage - currentUser role:', currentUser?.role)
  console.log('HomePage - isLandlord:', isLandlord)

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['listings', filters, page],
    queryFn: () => listingsApi.getListings({ ...filters, page, page_size: pageSize }),
  })

  const handlePageChange = (newPage: number) => {
    setPage(newPage)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleFiltersChange = (newFilters: Filters) => {
    setFilters(newFilters)
    setPage(1) // Reset to first page when filters change
  }

  const totalPages = data?.count ? Math.ceil(data.count / pageSize) : 0

  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <motion.div 
        className="relative mb-16 overflow-hidden rounded-3xl premium-shadow"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1.2, ease: "easeOut" }}
      >
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-br from-black via-gray-900 to-black"></div>
          <div className="absolute inset-0 luxury-gradient opacity-20"></div>
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNEMUFFMzciIGZpbGwtb3BhY2l0eT0iMC4wNSI+PHBhdGggZD0iTTM2IDM0YzAtMS4xLS45LTItMi0ycy0yIC45LTIgMiAuOSAyIDIgMiAyLS45IDItMnoiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-30"></div>
        </div>
        
        <div className="relative px-8 py-24 md:py-40 text-center">
          <motion.div
            className="mb-8"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.3 }}
          >
            <div className="inline-block px-6 py-2 glass-dark rounded-full mb-6 luxury-border">
              <span className="text-amber-400 text-sm font-semibold tracking-widest uppercase elegant-text">Exclusive Collection</span>
            </div>
          </motion.div>
          
          <motion.h1 
            className="text-7xl md:text-9xl font-black mb-8 text-shadow-luxury"
            style={{ fontFamily: "'Playfair Display', serif" }}
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.2, delay: 0.4 }}
          >
            <span className="gradient-text">Extraordinary</span>
            <br />
            <span className="text-white">Residences</span>
          </motion.h1>
          
          <motion.p 
            className="text-xl md:text-2xl text-gray-300 mb-12 max-w-2xl mx-auto font-light leading-relaxed elegant-text"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.6 }}
          >
            Curated selection of the world's most prestigious properties. Where elegance meets excellence.
          </motion.p>
          <motion.div 
            className="flex justify-center items-center"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            <motion.div
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.98 }}
            >
              <Link
                to="#listings"
                className="group relative px-12 py-5 luxury-gradient text-black rounded-xl font-bold text-lg overflow-hidden glow-effect block"
              >
                <span className="relative z-10 font-black tracking-wide">Explore Collection</span>
                <motion.div
                  className="absolute inset-0 bg-white opacity-0 group-hover:opacity-20"
                  transition={{ duration: 0.3 }}
                />
              </Link>
            </motion.div>
          </motion.div>
        </div>
        
        {/* Premium decorative elements */}
        <div className="absolute top-10 left-10 w-32 h-32 border border-amber-400/20 rounded-full"></div>
        <div className="absolute top-20 left-20 w-16 h-16 border border-amber-400/30 rounded-full"></div>
        <div className="absolute bottom-10 right-10 w-40 h-40 border border-amber-400/15 rounded-full"></div>
        <div className="absolute bottom-20 right-20 w-20 h-20 border border-amber-400/25 rounded-full"></div>
        
        <motion.div 
          className="absolute top-1/4 right-1/4 w-px h-32 bg-gradient-to-b from-transparent via-amber-400/30 to-transparent"
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 3, repeat: Infinity }}
        />
        <motion.div 
          className="absolute bottom-1/4 left-1/4 w-px h-24 bg-gradient-to-b from-transparent via-amber-400/30 to-transparent"
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 3, repeat: Infinity, delay: 1.5 }}
        />
      </motion.div>

      <AnimatedSection id="listings" delay={0.2}>
        <ListingFilters filters={filters} onFiltersChange={handleFiltersChange} />

        {isLoading && <LoadingSpinner />}

        {error && (
          <ErrorMessage
            message="Failed to load listings. Please try again."
            onRetry={() => refetch()}
          />
        )}

        {!isLoading && !error && (
          <>
            {data?.results && data.results.length > 0 ? (
              <>
                <AnimatedSection delay={0.3}>
                  <div className="mb-10 flex items-center justify-between">
                    <div className="glass-dark px-8 py-5 rounded-2xl luxury-border">
                      <div className="flex items-baseline gap-3">
                        <span className="text-gray-300 font-light text-base elegant-text uppercase tracking-wider">Collection</span>
                        <span className="text-4xl font-black gradient-text" style={{ fontFamily: "'Playfair Display', serif" }}>
                          {data.count || data.results.length}
                        </span>
                        <span className="text-gray-400 font-light text-sm elegant-text">
                          {data.results.length === 1 ? 'residence' : 'residences'}
                        </span>
                      </div>
                    </div>
                    {isLandlord && (
                      <motion.button
                        onClick={() => setShowAddForm(true)}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="px-8 py-4 luxury-gradient text-black rounded-xl transition-all shadow-lg glow-effect font-bold"
                      >
                        + Add Listing
                      </motion.button>
                    )}
                    {!isLandlord && isAuthenticated && (
                      <div className="text-sm text-gray-400 elegant-text">
                        Role: {currentUser?.role || 'N/A'}
                      </div>
                    )}
                  </div>
                </AnimatedSection>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {data.results.map((listing, index) => (
                    <AnimatedCard key={listing.id} delay={index * 0.1}>
                      <ListingCard listing={listing} />
                    </AnimatedCard>
                  ))}
                </div>
                {totalPages > 1 && (
                  <AnimatedSection delay={0.5}>
                    <Pagination
                      currentPage={page}
                      totalPages={totalPages}
                      onPageChange={handlePageChange}
                      hasNext={!!data.next}
                      hasPrevious={!!data.previous}
                    />
                  </AnimatedSection>
                )}
              </>
              ) : (
                <AnimatedSection delay={0.3}>
                  <div className="text-center py-20 glass-dark rounded-3xl premium-shadow luxury-border">
                    <motion.div
                      animate={{ rotate: [0, 10, -10, 0] }}
                      transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
                    >
                      <svg className="w-32 h-32 mx-auto text-amber-400 mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </motion.div>
                    <p className="text-white text-2xl font-bold mb-2 elegant-text">No listings found</p>
                    <p className="text-gray-400 text-lg mb-6 elegant-text">
                      {isLandlord 
                        ? 'Create your first listing to get started' 
                        : 'Try adjusting your filters to see more results'}
                    </p>
                    {isLandlord && (
                      <motion.button
                        onClick={() => setShowAddForm(true)}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="px-8 py-4 luxury-gradient text-black rounded-xl transition-all shadow-lg glow-effect font-bold"
                      >
                        + Add Your First Listing
                      </motion.button>
                    )}
                  </div>
                </AnimatedSection>
              )}
          </>
        )}
      </AnimatedSection>
      {showAddForm && (
        <AddListingForm
          onClose={() => setShowAddForm(false)}
          onSuccess={() => {
            setShowAddForm(false)
            refetch()
          }}
        />
      )}
    </div>
  )
}

export default HomePage

