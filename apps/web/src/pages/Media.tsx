import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import ReactECharts from 'echarts-for-react'
import { api, downloadCsv } from '../lib/api'
import { triggerCsvDownload } from '../lib/download'

export function Media() {
  const { data } = useQuery({ queryKey:['media-lifecycle'], queryFn: async()=> (await api.get('/media-lifecycle')).data, initialData:[{date:'2025-02-10',topic:'safety',count:3,avg_sentiment:-0.22}] })
  const [topic, setTopic] = useState('all')

  const onExport = async () => {
    const csv = await downloadCsv('media_lifecycle')
    triggerCsvDownload('media-lifecycle.csv', csv)
  }

  const rows = topic === 'all' ? data : data.filter((r:any)=>r.topic===topic)
  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: rows.map((r:any)=>String(r.date)) },
    yAxis: [{ type: 'value' }, { type: 'value', min: -1, max: 1 }],
    series: [
      { type: 'bar', name: 'Story Count', data: rows.map((r:any)=>r.count) },
      { type: 'line', name: 'Avg Sentiment', yAxisIndex: 1, data: rows.map((r:any)=>r.avg_sentiment) },
    ]
  }

  return <div><h2>Media & Sentiment</h2>
  <label>Topic filter: </label>
  <select value={topic} onChange={e=>setTopic(e.target.value)}>
    <option value='all'>all</option>
    {[...new Set(data.map((r:any)=>r.topic))].map((t:any)=><option key={t} value={t}>{t}</option>)}
  </select>
  <button onClick={onExport} style={{marginLeft:8}}>Export CSV snapshot</button>
  <ReactECharts option={option} style={{height:280, marginTop:12}} />
  <table><thead><tr><th>Date</th><th>Topic</th><th>Count</th><th>Avg sentiment</th></tr></thead>
  <tbody>{rows.map((r:any,i:number)=><tr key={i}><td>{String(r.date)}</td><td>{r.topic}</td><td>{r.count}</td><td>{r.avg_sentiment}</td></tr>)}</tbody></table>
  <p>Story lifecycle tracked by topic over time (emerging → peak → fading).</p>
  </div>
}
