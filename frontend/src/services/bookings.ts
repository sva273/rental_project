import apiClient from './api'
import { Booking, CreateBookingData } from '../types/booking'

export const bookingsApi = {
  // Получить список бронирований
  getBookings: async (): Promise<{ results: Booking[]; count: number }> => {
    const { data } = await apiClient.get('/bookings/')
    return data
  },

  // Получить одно бронирование
  getBooking: async (id: number): Promise<Booking> => {
    const { data } = await apiClient.get(`/bookings/${id}/`)
    return data
  },

  // Создать бронирование
  createBooking: async (bookingData: CreateBookingData): Promise<Booking> => {
    const { data } = await apiClient.post('/bookings/', bookingData)
    return data
  },

  // Отменить бронирование
  cancelBooking: async (id: number): Promise<void> => {
    await apiClient.post(`/bookings/${id}/cancel/`)
  },

  // Подтвердить бронирование (для landlord/admin)
  confirmBooking: async (id: number): Promise<void> => {
    await apiClient.post(`/bookings/${id}/confirm/`)
  },

  // Отклонить бронирование (для landlord/admin)
  rejectBooking: async (id: number): Promise<void> => {
    await apiClient.post(`/bookings/${id}/reject/`)
  },
}

