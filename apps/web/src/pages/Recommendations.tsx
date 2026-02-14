import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

export function Recommendations() {
  const { data } = useQuery({ queryKey:['recommendations'], queryFn: async()=> (await api.get('/recommendations')).data, initialData:[{id:1,topic:'safety',action:'Publish FAQ and weekly briefings',confidence:0.82,rationale:'Negative mentions increasing',evidence:{sources:['media-1']}}] })
  return <div><h2>Recommendations</h2>{data.map((r:any)=><div key={r.id} style={{border:'1px solid #ddd',padding:12,margin:'8px 0'}}><b>{r.topic}</b> (confidence: {r.confidence})<p>{r.action}</p><small>{r.rationale}</small><pre>{JSON.stringify(r.evidence, null, 2)}</pre></div>)}</div>
}
