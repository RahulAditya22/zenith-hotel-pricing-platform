import { apiClient } from './client';
import type { 
  Property, 
  RoomType, 
  RoomSearchResult, 
  ReservationCreate, 
  Reservation, 
  PriceTrendResponse 
} from '../types';

export const fetchProperties = async (): Promise<Property[]> => {
  const { data } = await apiClient.get<Property[]>('/properties');
  return data;
};

export const fetchPropertyRooms = async (propertyId: number): Promise<RoomType[]> => {
  const { data } = await apiClient.get<RoomType[]>(`/properties/${propertyId}/rooms`);
  return data;
};

export const searchRooms = async (params: {
  city?: string;
  check_in_date?: string;
  check_out_date?: string;
  guests?: number;
  min_price?: number;
  max_price?: number;
  sort_by?: string;
}): Promise<RoomSearchResult[]> => {
  const { data } = await apiClient.get<RoomSearchResult[]>('/search', { params });
  return data;
};

export const fetchPriceTrend = async (params: {
  room_type_id: number;
  days?: number;
  start_date?: string;
}): Promise<PriceTrendResponse> => {
  const { data } = await apiClient.get<PriceTrendResponse>('/pricing/trend', { params });
  return data;
};

export const createReservation = async (payload: ReservationCreate): Promise<Reservation> => {
  const { data } = await apiClient.post<Reservation>('/bookings', payload);
  return data;
};

export const fetchReservation = async (code: string): Promise<Reservation> => {
  const { data } = await apiClient.get<Reservation>(`/bookings/${code}`);
  return data;
};
