import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import ReactECharts from 'echarts-for-react'
import { api } from '../lib/api'

export function Executive() {
  const { data } = useQuery({ queryKey:['overview'], queryFn: async()=> (await api.get('/overview')).data, initialData: {kpi_count: 12, media_items:44, avg_sentiment:-0.1, alerts:['2 KPI records show high variance']} })
  const { data: outliers } = useQuery({ queryKey:['outliers'], queryFn: async()=> (await api.get('/outliers')).data, initialData: [] })
  const [showExplain, setShowExplain] = useState(false)

  const option = {
    xAxis: { type: 'category', data: ['KPI', 'Media', 'Outliers'] },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: [data.kpi_count, data.media_items, outliers.length], itemStyle: { color: '#0a66c2' } }]
  }

  return <div>
    <div style={{display:'flex', gap:16, flexWrap:'wrap'}}>
      <Card label='KPI records' value={data.kpi_count} />
      <Card label='Media items' value={data.media_items} />
      <Card label='Avg sentiment' value={data.avg_sentiment} />
      <Card label='Outliers' value={outliers.length} />
    </div>
    <div style={{marginTop:16,border:'1px solid #ddd', borderRadius:8, padding:8}}>
      <ReactECharts option={option} style={{height:260}} />
    </div>
    <h3>Key alerts</h3>
    <ul>{data.alerts.map((a:string)=><li key={a}>{a}</li>)}</ul>
    <button onClick={()=>setShowExplain(v=>!v)}>Toggle explain panel</button>
    {showExplain && <p style={{background:'#f6f8fa',padding:8}}>Executive metrics are aggregated from KPI/media tables and outlier thresholds in analytics service.</p>}
  </div>
}

function Card({label,value}:{label:string,value:string|number}) { return <div style={{border:'1px solid #ddd',padding:16,borderRadius:8,minWidth:170}}><strong>{label}</strong><div>{value}</div></div> }
