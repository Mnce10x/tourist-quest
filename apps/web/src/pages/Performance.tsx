import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import ReactECharts from 'echarts-for-react'
import { api, downloadCsv } from '../lib/api'
import { triggerCsvDownload } from '../lib/download'

export function Performance() {
  const { data } = useQuery({
    queryKey: ['kpi-trends'],
    queryFn: async () => (await api.get('/kpi-trends')).data,
    initialData: [
      { report_period: 'FY2024/25 Q2', programme: 'Marketing', kpi_name: 'International Arrivals', variance: -7.5 },
      { report_period: 'FY2024/25 Q3', programme: 'Marketing', kpi_name: 'International Arrivals', variance: -9.5 }
    ]
  })
  const [selected, setSelected] = useState<any>(null)

  const onExport = async () => {
    const csv = await downloadCsv('kpi')
    triggerCsvDownload('kpi-trends.csv', csv)
  }

  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: data.map((r:any)=>r.report_period) },
    yAxis: { type: 'value' },
    series: [{ type: 'line', smooth: true, data: data.map((r:any)=>r.variance) }]
  }

  return <div>
    <h2>Performance Dashboard</h2>
    <button onClick={onExport}>Export CSV snapshot</button>
    <ReactECharts option={option} style={{height:280, marginTop:12}} />
    <table><thead><tr><th>Period</th><th>Programme</th><th>KPI</th><th>Variance</th></tr></thead>
      <tbody>{data.map((r:any, i:number)=><tr key={i} onClick={()=>setSelected(r)} style={{cursor:'pointer'}}><td>{r.report_period}</td><td>{r.programme}</td><td>{r.kpi_name}</td><td>{r.variance}</td></tr>)}</tbody></table>
    <p><b>Explain panel:</b> {selected ? `${selected.kpi_name} in ${selected.report_period} variance ${selected.variance}. Query /api/explain for evidence snippets.` : 'Select a row.'}</p>
  </div>
}
