import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

export function Audit() {
  const { data } = useQuery({ queryKey:['data-quality'], queryFn: async()=> (await api.get('/data-quality')).data, initialData:{total_documents:0,total_kpis:0,total_expenditure:0,total_media:0,extraction_success_rate:0,anomalies:['No ingested documents detected']} })
  return <div><h2>Data Quality & Audit</h2>
  <pre>{JSON.stringify(data, null, 2)}</pre>
  <p>All metrics/recommendations should map to source URL, file hash, and evidence snippets.</p>
  </div>
}
