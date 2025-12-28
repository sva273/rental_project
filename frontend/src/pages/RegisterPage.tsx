import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { authApi } from '../services/auth'
import ErrorMessage from '../components/common/ErrorMessage'
import { motion } from 'framer-motion'

const RegisterPage = () => {
  const { user } = useAuthStore()
  
  // Предзаполнение данных из localStorage или из authStore
  const getInitialFormData = () => {
    // Проверяем localStorage для сохраненных данных регистрации
    const savedData = localStorage.getItem('registerFormData')
    if (savedData) {
      try {
        const parsed = JSON.parse(savedData)
        return {
          username: parsed.username || '',
          email: parsed.email || '',
          password: '',
          passwordConfirm: '',
          first_name: parsed.first_name || '',
          last_name: parsed.last_name || '',
          phone_number: parsed.phone_number || '',
          role: (parsed.role || 'tenant') as 'tenant' | 'landlord',
        }
      } catch (e) {
        console.error('Error parsing saved form data:', e)
      }
    }
    
    // Если есть залогиненный пользователь, предзаполняем его данными
    if (user) {
      return {
        username: (user as any).username || '',
        email: user.email || '',
        password: '',
        passwordConfirm: '',
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        phone_number: (user as any).phone_number || '',
        role: (user.role || 'tenant') as 'tenant' | 'landlord',
      }
    }
    
    // По умолчанию
    return {
      username: '',
      email: '',
      password: '',
      passwordConfirm: '',
      first_name: '',
      last_name: '',
      phone_number: '',
      role: 'tenant' as 'tenant' | 'landlord',
    }
  }

  const [formData, setFormData] = useState(getInitialFormData)
  const [showPassword, setShowPassword] = useState(false)
  const [showPasswordConfirm, setShowPasswordConfirm] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuthStore()
  const navigate = useNavigate()

  // Сохраняем данные формы в localStorage при изменении (кроме паролей)
  useEffect(() => {
    const dataToSave = {
      username: formData.username,
      email: formData.email,
      first_name: formData.first_name,
      last_name: formData.last_name,
      phone_number: formData.phone_number,
      role: formData.role,
    }
    localStorage.setItem('registerFormData', JSON.stringify(dataToSave))
  }, [formData.username, formData.email, formData.first_name, formData.last_name, formData.phone_number, formData.role])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!formData.username?.trim()) {
      setError('Username is required')
      return
    }

    if (!formData.first_name?.trim() || !formData.last_name?.trim()) {
      setError('First name and last name are required')
      return
    }

    if (formData.password !== formData.passwordConfirm) {
      setError('Passwords do not match')
      return
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long')
      return
    }

    setLoading(true)

    try {
      const { username, email, password, passwordConfirm, first_name, last_name, phone_number, role } = formData
      const registerData = {
        username: username.trim(),
        email: email.trim(),
        password,
        password2: passwordConfirm,
        first_name: first_name.trim(),
        last_name: last_name.trim(),
        phone_number: phone_number.trim() || undefined,
        role: role || 'tenant',
      }
      console.log('Sending registration data:', { ...registerData, password: '***', password2: '***' })
      const registerResponse = await authApi.register(registerData)
      console.log('Registration response:', registerResponse)
      
      // Очищаем сохраненные данные после успешной регистрации
      localStorage.removeItem('registerFormData')
      
      // Сохраняем пользователя из ответа регистрации
      if (registerResponse.user) {
        login(email, password).then(() => {
          navigate('/')
        })
      } else {
        // Если нет user в ответе, делаем обычный login
        await login(email, password)
        navigate('/')
      }
    } catch (err: any) {
      console.error('Registration error:', err.response?.data)
      const errorData = err.response?.data
      let errorMessage = 'Registration failed. Please try again.'
      
      if (errorData) {
        if (errorData.detail) {
          errorMessage = errorData.detail
        } else if (errorData.email) {
          errorMessage = Array.isArray(errorData.email) ? errorData.email[0] : errorData.email
        } else if (errorData.password) {
          errorMessage = Array.isArray(errorData.password) ? errorData.password[0] : errorData.password
        } else if (errorData.first_name) {
          errorMessage = Array.isArray(errorData.first_name) ? errorData.first_name[0] : errorData.first_name
        } else if (errorData.last_name) {
          errorMessage = Array.isArray(errorData.last_name) ? errorData.last_name[0] : errorData.last_name
        } else if (errorData.non_field_errors) {
          errorMessage = Array.isArray(errorData.non_field_errors) ? errorData.non_field_errors[0] : errorData.non_field_errors
        } else {
          // Показываем первую ошибку из объекта
          const firstKey = Object.keys(errorData)[0]
          const firstError = errorData[firstKey]
          errorMessage = Array.isArray(firstError) ? firstError[0] : firstError
        }
      }
      
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Luxury animated background */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div 
          className="absolute -top-40 -right-40 w-96 h-96 bg-amber-400/30 rounded-full mix-blend-multiply filter blur-3xl"
          animate={{ 
            x: [0, 100, 0],
            y: [0, 50, 0],
            scale: [1, 1.2, 1]
          }}
          transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div 
          className="absolute -bottom-40 -left-40 w-96 h-96 bg-orange-500/30 rounded-full mix-blend-multiply filter blur-3xl"
          animate={{ 
            x: [0, -100, 0],
            y: [0, -50, 0],
            scale: [1, 1.3, 1]
          }}
          transition={{ duration: 25, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
        />
        <motion.div 
          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-yellow-500/30 rounded-full mix-blend-multiply filter blur-3xl"
          animate={{ 
            x: [0, 50, 0],
            y: [0, -100, 0],
            scale: [1, 1.1, 1]
          }}
          transition={{ duration: 30, repeat: Infinity, ease: "easeInOut", delay: 1 }}
        />
      </div>
      
      <motion.div 
        className="max-w-md w-full space-y-8 relative z-10"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6 }}
      >
        <motion.div 
          className="glass-dark rounded-3xl premium-shadow p-8 luxury-border"
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <motion.div 
            className="text-center mb-8"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <motion.div 
              className="w-24 h-24 luxury-gradient rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-2xl glow-effect"
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 4, repeat: Infinity, repeatDelay: 2 }}
            >
              <svg className="w-12 h-12 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </motion.div>
            <h2 className="text-5xl font-black gradient-text mb-3" style={{ fontFamily: "'Playfair Display', serif" }}>
              Join ÉLÉGANCE
            </h2>
            <p className="text-gray-400 text-lg elegant-text">Create your exclusive account</p>
          </motion.div>

          {error && <ErrorMessage message={error} />}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="role" className="block text-sm font-semibold text-amber-400 mb-3 elegant-text uppercase tracking-wider">
                I am a
              </label>
              <div className="grid grid-cols-2 gap-4">
                <motion.button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'tenant' })}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`px-6 py-4 rounded-xl font-semibold transition-all luxury-border ${
                    formData.role === 'tenant'
                      ? 'luxury-gradient text-black shadow-lg glow-effect'
                      : 'glass-dark text-amber-400 hover:bg-amber-400/10'
                  }`}
                >
                  Tenant
                </motion.button>
                <motion.button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'landlord' })}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`px-6 py-4 rounded-xl font-semibold transition-all luxury-border ${
                    formData.role === 'landlord'
                      ? 'luxury-gradient text-black shadow-lg glow-effect'
                      : 'glass-dark text-amber-400 hover:bg-amber-400/10'
                  }`}
                >
                  Landlord
                </motion.button>
              </div>
            </div>

            <div>
              <label htmlFor="username" className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                Username *
              </label>
              <input
                id="username"
                name="username"
                type="text"
                autoComplete="username"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                placeholder="johndoe"
                required
                maxLength={30}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="first_name" className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  First Name
                </label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="John"
                  required
                />
              </div>
              <div>
                <label htmlFor="last_name" className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                  Last Name
                </label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="Doe"
                  required
                />
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                placeholder="you@example.com"
                required
              />
            </div>

            <div>
              <label htmlFor="phone_number" className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                Phone Number (Optional)
              </label>
              <input
                id="phone_number"
                name="phone_number"
                type="tel"
                autoComplete="tel"
                value={formData.phone_number}
                onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                className="w-full px-4 py-3 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                placeholder="1234567890"
                pattern="[0-9]{10,15}"
                title="Phone number must contain 10-15 digits only"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-4 py-3 pr-12 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="••••••••"
                  required
                  minLength={8}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-amber-400 hover:text-amber-300 transition-colors"
                >
                  {showPassword ? (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            <div>
              <label htmlFor="passwordConfirm" className="block text-sm font-semibold text-amber-400 mb-2 elegant-text uppercase tracking-wider">
                Confirm Password
              </label>
              <div className="relative">
                <input
                  id="passwordConfirm"
                  name="passwordConfirm"
                  type={showPasswordConfirm ? 'text' : 'password'}
                  autoComplete="new-password"
                  value={formData.passwordConfirm}
                  onChange={(e) => setFormData({ ...formData, passwordConfirm: e.target.value })}
                  className="w-full px-4 py-3 pr-12 glass-dark border border-amber-400/20 rounded-xl focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/50 transition-all text-white placeholder-gray-500 luxury-border"
                  placeholder="••••••••"
                  required
                  minLength={8}
                />
                <button
                  type="button"
                  onClick={() => setShowPasswordConfirm(!showPasswordConfirm)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-amber-400 hover:text-amber-300 transition-colors"
                >
                  {showPasswordConfirm ? (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            <motion.button
              type="submit"
              disabled={loading}
              whileHover={{ scale: loading ? 1 : 1.02 }}
              whileTap={{ scale: loading ? 1 : 0.98 }}
              className="w-full luxury-gradient text-black py-4 rounded-xl font-bold focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg glow-effect"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creating account...
                </span>
              ) : (
                'Create Account'
              )}
            </motion.button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-400 elegant-text">
              Already have an account?{' '}
              <Link to="/login" className="font-semibold text-amber-400 hover:text-amber-300 transition-colors">
                Sign in
              </Link>
            </p>
          </div>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default RegisterPage

