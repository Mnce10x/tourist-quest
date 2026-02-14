import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

export function Reports() {
  const { data } = useQuery({ queryKey:['kpis'], queryFn: async()=> (await api.get('/kpis')).data, initialData:[] })
  return <div><h2>Quarterly Reports Explorer</h2>
    <input placeholder='Search report period or programme' style={{padding:8, width:'40%'}} />
    <ul>{data.map((r:any)=> <li key={r.id}><b>{r.report_period}</b> - {r.programme} - {r.kpi_name}</li>)}</ul>
    <p>Highlights and extracted tables trace to source URL/file hash via provenance.</p>
  </div>
}
