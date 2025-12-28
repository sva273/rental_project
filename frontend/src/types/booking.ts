export interface Booking {
  id: number
  listing: number
  listing_title: string
  tenant: number
  tenant_email: string
  start_date: string
  end_date: string
  parking_included: boolean
  status: 'pending' | 'confirmed' | 'cancelled' | 'rejected'
  total_price: string
  created_at?: string
}

export interface CreateBookingData {
  listing: number
  start_date: string
  end_date: string
  parking_included?: boolean
}

