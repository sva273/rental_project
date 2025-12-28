export interface Listing {
  id: number
  landlord: number
  landlord_email: string
  title: string
  description: string
  country: string
  city: string
  street: string
  house_number: string
  latitude?: string
  longitude?: string
  property_type: string
  rooms?: number
  floor?: number
  has_elevator: boolean
  has_terrace: boolean
  has_balcony: boolean
  bathroom_type: string
  has_internet: boolean
  has_parking: boolean
  views_count: number
  daily_enabled: boolean
  price_per_day?: string
  parking_price_per_day?: string
  is_active: boolean
  main_image?: string
  full_address: string
  average_rating: number
  reviews_count: number
  created_at: string
  updated_at: string
}

export interface ListingFilters {
  search?: string
  city?: string
  country?: string
  property_type?: string
  min_price?: number
  max_price?: number
  min_rooms?: number
  max_rooms?: number
  ordering?: string
}

