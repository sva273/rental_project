import apiClient from './api'

export interface Notification {
  id: number
  notification_type: string
  title: string
  message: string
  related_booking: number | null
  related_review: number | null
  is_read: boolean
  created_at: string
}

export interface NotificationResponse {
  results: Notification[]
  count: number
}

export const notificationsApi = {
  // Get all notifications
  getNotifications: async (): Promise<NotificationResponse> => {
    const { data } = await apiClient.get('/notifications/')
    return data
  },

  // Get unread count
  getUnreadCount: async (): Promise<{ unread_count: number }> => {
    const { data } = await apiClient.get('/notifications/unread_count/')
    return data
  },

  // Mark notification as read (deletes it)
  markAsRead: async (id: number): Promise<void> => {
    await apiClient.patch(`/notifications/${id}/mark_read/`)
  },

  // Mark all notifications as read
  markAllAsRead: async (): Promise<{ detail: string }> => {
    const { data } = await apiClient.post('/notifications/mark_all_read/')
    return data
  },
}

