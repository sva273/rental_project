import apiClient from './api'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  password2: string
  first_name: string
  last_name: string
  phone_number?: string
  role?: string
}

export interface AuthResponse {
  token: string
  user: {
    id: number
    username?: string
    email: string
    first_name: string
    last_name: string
    phone_number?: string
    role: string
  }
}

export const authApi = {
  // Вход
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const { data } = await apiClient.post('/auth/login/', credentials)
    if (data.token) {
      localStorage.setItem('token', data.token)
    }
    return data
  },

  // Регистрация
  register: async (registerData: RegisterData): Promise<AuthResponse> => {
    const { data } = await apiClient.post('/auth/register/', registerData)
    if (data.token) {
      localStorage.setItem('token', data.token)
    }
    return data
  },

  // Выход
  logout: (): void => {
    localStorage.removeItem('token')
    window.location.href = '/login'
  },

  // Получить текущего пользователя
  getCurrentUser: async (): Promise<AuthResponse['user']> => {
    const { data } = await apiClient.get('/profile/')
    return data
  },

  // Обновить профиль пользователя
  updateProfile: async (userData: Partial<AuthResponse['user']> & { username?: string; phone_number?: string; role?: string }): Promise<AuthResponse['user']> => {
    const { data } = await apiClient.patch('/profile/me/', userData)
    return data
  },
}

