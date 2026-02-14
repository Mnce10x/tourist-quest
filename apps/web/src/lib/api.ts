import axios from 'axios'

export const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || 'http://localhost:8000') + '/api',
  headers: {
    'x-role': 'admin'
  }
})

export async function downloadCsv(dataset: string): Promise<string> {
  const response = await api.get(`/export/${dataset}`, { responseType: 'text' })
  return response.data
}
