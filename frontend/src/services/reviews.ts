import apiClient from './api'

export interface Review {
  id: number
  listing: number
  listing_title?: string
  tenant: number
  tenant_email: string
  rating: number
  comment: string
  created_at: string
}

export interface CreateReviewData {
  listing: number
  rating: number
  comment: string
}

export const reviewsApi = {
  // Получить список отзывов
  getReviews: async (listingId?: number): Promise<{ results: Review[]; count: number }> => {
    const params = listingId ? { listing: listingId } : {}
    const { data } = await apiClient.get('/reviews/', { params })
    return data
  },

  // Получить один отзыв
  getReview: async (id: number): Promise<Review> => {
    const { data } = await apiClient.get(`/reviews/${id}/`)
    return data
  },

  // Создать отзыв
  createReview: async (reviewData: CreateReviewData): Promise<Review> => {
    const { data } = await apiClient.post('/reviews/', reviewData)
    return data
  },

  // Обновить отзыв
  updateReview: async (id: number, reviewData: Partial<CreateReviewData>): Promise<Review> => {
    const { data } = await apiClient.patch(`/reviews/${id}/`, reviewData)
    return data
  },

  // Удалить отзыв
  deleteReview: async (id: number): Promise<void> => {
    await apiClient.delete(`/reviews/${id}/`)
  },
}

