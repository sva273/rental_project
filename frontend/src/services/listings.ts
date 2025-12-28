import apiClient from './api'
import { Listing, ListingFilters } from '../types/listing'

export interface PaginatedResponse<T> {
  results: T[]
  count: number
  next: string | null
  previous: string | null
}

export const listingsApi = {
  // Получить список объявлений с пагинацией
  getListings: async (filters?: ListingFilters & { page?: number; page_size?: number }): Promise<PaginatedResponse<Listing>> => {
    const { data } = await apiClient.get('/listings/', { params: filters })
    return data
  },

  // Получить одно объявление
  getListing: async (id: number): Promise<Listing> => {
    const { data } = await apiClient.get(`/listings/${id}/`)
    return data
  },

  // Создать объявление (только для landlord/admin)
  createListing: async (listingData: FormData | Partial<Listing>): Promise<Listing> => {
    const { data } = await apiClient.post('/listings/', listingData)
    return data
  },

  // Обновить объявление
  updateListing: async (id: number, listingData: Partial<Listing>): Promise<Listing> => {
    const { data } = await apiClient.patch(`/listings/${id}/`, listingData)
    return data
  },

  // Удалить объявление
  deleteListing: async (id: number): Promise<void> => {
    await apiClient.delete(`/listings/${id}/`)
  },

  // Переключить активность объявления
  toggleActive: async (id: number): Promise<{ is_active: boolean }> => {
    const { data } = await apiClient.post(`/listings/${id}/toggle_active/`)
    return data
  },
}

