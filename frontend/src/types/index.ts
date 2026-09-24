export interface Property {
  id: number;
  name: string;
  slug: string;
  description: string;
  city: string;
  state?: string;
  country: string;
  address: string;
  star_rating: number;
  review_score: number;
  review_count: number;
  image_url: string;
  amenities: string;
  created_at: string;
}

export interface RoomType {
  id: number;
  property_id: number;
  name: string;
  code: string;
  description: string;
  base_price: number;
  total_rooms: number;
  max_occupancy: number;
  amenities: string;
  image_url: string;
  created_at: string;
}

export interface PricingBreakdown {
  date: string;
  base_price: number;
  final_price: number;
  occupancy_rate: number;
  occupancy_multiplier: number;
  days_to_checkin: number;
  lead_time_multiplier: number;
  is_weekend: boolean;
  weekend_multiplier: number;
  demand_event_name?: string | null;
  demand_event_multiplier: number;
  total_multiplier: number;
  explanation: string;
}

export interface RoomSearchResult {
  property_id: number;
  property_name: string;
  property_city: string;
  star_rating: number;
  review_score: number;
  review_count: number;
  property_image_url: string;
  property_amenities: string[];
  
  room_type_id: number;
  room_name: string;
  room_code: string;
  room_image_url: string;
  max_occupancy: number;
  total_rooms: number;
  available_rooms: number;
  
  total_price: number;
  average_nightly_price: number;
  base_nightly_price: number;
  value_score: number;
  
  nightly_breakdown: PricingBreakdown[];
}

export interface ReservationCreate {
  room_type_id: number;
  guest_name: string;
  guest_email: string;
  check_in_date: string;
  check_out_date: string;
  guest_count: number;
}

export interface Reservation {
  id: number;
  reservation_code: string;
  room_type_id: number;
  guest_name: string;
  guest_email: string;
  check_in_date: string;
  check_out_date: string;
  guest_count: number;
  total_price: number;
  night_count: number;
  status: string;
  created_at: string;
}

export interface PriceTrendPoint {
  date: string;
  day_name: string;
  is_weekend: boolean;
  price: number;
  base_price: number;
  occupancy_rate: number;
  occupancy_multiplier: number;
  lead_time_multiplier: number;
  event_multiplier: number;
  event_name?: string | null;
}

export interface PriceTrendResponse {
  property_id: number;
  property_name: string;
  room_type_id: number;
  room_name: string;
  base_price: number;
  start_date: string;
  end_date: string;
  points: PriceTrendPoint[];
}
