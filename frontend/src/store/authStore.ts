import { create } from 'zustand'
import { authApi, AuthResponse } from '../services/auth'

interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  role: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => void
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),

  login: async (email: string, password: string) => {
    try {
      const response = await authApi.login({ email, password })
      console.log('Login response:', response)
      if (response.token) {
        localStorage.setItem('token', response.token)
      }
      set({
        user: response.user,
        token: response.token,
        isAuthenticated: true,
      })
      console.log('User set in store:', response.user)
    } catch (error) {
      throw error
    }
  },

  logout: () => {
    authApi.logout()
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    })
  },

  checkAuth: () => {
    const token = localStorage.getItem('token')
    if (token) {
      // Можно загрузить данные пользователя
      authApi.getCurrentUser().then((user) => {
        console.log('User loaded from checkAuth:', user)
        set({ user, isAuthenticated: true, token })
      }).catch(() => {
        set({ user: null, token: null, isAuthenticated: false })
        localStorage.removeItem('token')
      })
    }
  },

  setUser: (user: User) => {
    set({ user })
  },
}))

