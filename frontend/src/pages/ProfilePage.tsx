import { useAuthStore } from '../store/authStore'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi } from '../services/auth'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ErrorMessage from '../components/common/ErrorMessage'
import AnimatedSection from '../components/common/AnimatedSection'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

const ProfilePage = () => {
  const { user, isAuthenticated, setUser } = useAuthStore()
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    role: '',
  })
  const queryClient = useQueryClient()

  const { data: profileData, isLoading, error: profileError } = useQuery({
    queryKey: ['profile'],
    queryFn: () => authApi.getCurrentUser(),
    enabled: isAuthenticated,
    onSuccess: (data) => {
      console.log('Profile data loaded:', data)
      // Обновляем user в store
      setUser(data)
    },
  })

  // Синхронизируем formData с profileData при загрузке или изменении данных
  useEffect(() => {
    if (profileData) {
      setFormData({
        username: (profileData as any).username || '',
        first_name: profileData.first_name || '',
        last_name: profileData.last_name || '',
        email: profileData.email || '',
        phone_number: (profileData as any).phone_number || '',
        role: (profileData as any).role || '',
      })
    }
  }, [profileData])

  const updateMutation = useMutation({
    mutationFn: (data: typeof formData) => {
      // Убираем role из данных для отправки, так как его нельзя менять
      const { role, ...dataToSend } = data
      return authApi.updateProfile(dataToSend)
    },
    onSuccess: (updatedUser) => {
      setUser(updatedUser)
      queryClient.setQueryData(['profile'], updatedUser)
      setIsEditing(false)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    updateMutation.mutate(formData)
  }

  const handleCancel = () => {
    if (profileData) {
      setFormData({
        username: (profileData as any).username || '',
        first_name: profileData.first_name || '',
        last_name: profileData.last_name || '',
        email: profileData.email || '',
        phone_number: (profileData as any).phone_number || '',
        role: (profileData as any).role || '',
      })
    }
    setIsEditing(false)
  }

  if (!isAuthenticated) {
    return (
      <div className="text-center py-20">
        <div className="glass-dark rounded-3xl p-12 luxury-border max-w-md mx-auto">
          <p className="text-amber-400 mb-6 text-lg elegant-text">Please login to view your profile</p>
          <Link
            to="/login"
            className="px-8 py-3 luxury-gradient text-black rounded-xl hover:shadow-lg glow-effect inline-block font-bold"
          >
            Sign In
          </Link>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return <LoadingSpinner />
  }

  const displayUser = profileData || user

  // Отладка
  console.log('ProfilePage - profileData:', profileData)
  console.log('ProfilePage - user from store:', user)
  console.log('ProfilePage - displayUser:', displayUser)

  return (
    <div className="max-w-5xl mx-auto">
      <AnimatedSection delay={0.1}>
        <div className="mb-10 text-center">
          <h1 className="text-6xl font-black text-white mb-4 text-shadow-luxury" style={{ fontFamily: "'Playfair Display', serif" }}>
            My Profile
          </h1>
          <p className="text-gray-400 text-lg elegant-text">Manage your exclusive account</p>
        </div>
      </AnimatedSection>
      
      <AnimatedSection delay={0.2}>
        <div className="glass-dark rounded-3xl premium-shadow p-10 luxury-border">
          <div className="mb-10 text-center">
            <motion.div 
              className="w-40 h-40 luxury-gradient rounded-full flex items-center justify-center mx-auto mb-6 shadow-2xl glow-effect relative"
              whileHover={{ scale: 1.05, rotate: 5 }}
              transition={{ duration: 0.3 }}
            >
              <span className="text-6xl font-black text-black" style={{ fontFamily: "'Playfair Display', serif" }}>
                {displayUser?.email?.charAt(0).toUpperCase() || 'U'}
              </span>
              <div className="absolute inset-0 border-4 border-amber-400/30 rounded-full animate-pulse"></div>
            </motion.div>
            <h2 className="text-4xl font-black text-white mb-2 elegant-text" style={{ fontFamily: "'Cormorant Garamond', serif" }}>
              {displayUser?.first_name || 'User'} {displayUser?.last_name || ''}
            </h2>
            <p className="text-amber-400 text-sm font-light tracking-wider uppercase">{displayUser?.email}</p>
          </div>

        {isEditing ? (
          <form onSubmit={handleSubmit} className="space-y-8">
            {updateMutation.isError && (
              <ErrorMessage
                message={updateMutation.error instanceof Error ? updateMutation.error.message : 'Failed to update profile'}
              />
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Username</label>
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="Enter username"
                  maxLength={30}
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="Enter email"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">First Name</label>
                <input
                  type="text"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="Enter first name"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Last Name</label>
                <input
                  type="text"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="Enter last name"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Phone Number</label>
                <input
                  type="tel"
                  value={formData.phone_number}
                  onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                  className="w-full px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="Enter phone number"
                  pattern="[0-9]{10,15}"
                  title="Phone number must contain 10-15 digits only"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Role</label>
                <div className="px-5 py-3.5 glass-dark border border-amber-400/20 rounded-xl text-white luxury-border">
                  <span className="capitalize font-semibold">{(displayUser as any)?.role || 'Not specified'}</span>
                  <span className="text-gray-400 text-sm ml-2">(cannot be changed)</span>
                </div>
              </div>
            </div>

            <div className="flex gap-4 pt-6 border-t border-amber-400/20">
              <motion.button
                type="submit"
                disabled={updateMutation.isPending}
                whileHover={{ scale: updateMutation.isPending ? 1 : 1.02 }}
                whileTap={{ scale: updateMutation.isPending ? 1 : 0.98 }}
                className="flex-1 px-8 py-4 luxury-gradient text-black rounded-xl transition-all shadow-lg glow-effect font-bold disabled:opacity-50"
              >
                {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
              </motion.button>
              <motion.button
                type="button"
                onClick={handleCancel}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex-1 px-8 py-4 glass-dark text-amber-400 rounded-xl hover:bg-amber-400/10 transition-all font-semibold luxury-border"
              >
                Cancel
              </motion.button>
            </div>
          </form>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
              <div className="glass-dark p-6 rounded-2xl luxury-border">
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Username</label>
                <p className="text-2xl font-bold text-white">{(displayUser as any)?.username || 'Not specified'}</p>
              </div>
              <div className="glass-dark p-6 rounded-2xl luxury-border">
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Email</label>
                <p className="text-2xl font-bold text-white">{displayUser?.email}</p>
              </div>
              <div className="glass-dark p-6 rounded-2xl luxury-border">
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Full Name</label>
                <p className="text-2xl font-bold text-white">
                  {displayUser?.first_name || displayUser?.last_name 
                    ? `${displayUser?.first_name || ''} ${displayUser?.last_name || ''}`.trim() 
                    : 'Not specified'}
                </p>
              </div>
              {(displayUser as any)?.phone_number && (
                <div className="glass-dark p-6 rounded-2xl luxury-border">
                  <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Phone Number</label>
                  <p className="text-2xl font-bold text-white">{(displayUser as any).phone_number}</p>
                </div>
              )}
              <div className="glass-dark p-6 rounded-2xl luxury-border">
                <label className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">Role</label>
                <p className="text-2xl font-bold text-white capitalize">{(displayUser as any)?.role || 'Not specified'}</p>
              </div>
            </div>

            <div className="flex flex-wrap gap-4 pt-8 border-t border-amber-400/20">
              <motion.button
                onClick={() => setIsEditing(true)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 luxury-gradient text-black rounded-xl transition-all shadow-lg glow-effect font-bold"
              >
                Edit Profile
              </motion.button>
              <Link
                to="/bookings"
                className="px-8 py-4 glass-dark text-amber-400 rounded-xl hover:bg-amber-400/10 transition-all font-semibold luxury-border"
              >
                My Bookings
              </Link>
              <Link
                to="/reviews"
                className="px-8 py-4 glass-dark text-amber-400 rounded-xl hover:bg-amber-400/10 transition-all font-semibold luxury-border"
              >
                Reviews
              </Link>
            </div>
          </>
        )}
        </div>
      </AnimatedSection>
    </div>
  )
}

export default ProfilePage

