import { useQuery } from '@tanstack/react-query'
import ReactECharts from 'echarts-for-react'
import { api } from '../lib/api'

export function Expenditure() {
  const { data } = useQuery({ queryKey:['expenditure'], queryFn: async()=> (await api.get('/expenditure')).data, initialData:[{id:1,programme:'Destination Development',item:'Infrastructure grants',planned_budget:250000000,actual_spend:231000000,variance:-19000000}] })
  const option = {
    tooltip: {},
    legend: { data: ['Planned', 'Actual'] },
    xAxis: { type: 'category', data: data.map((r:any)=>r.item) },
    yAxis: { type: 'value' },
    series: [
      { name: 'Planned', type: 'bar', data: data.map((r:any)=>r.planned_budget) },
      { name: 'Actual', type: 'bar', data: data.map((r:any)=>r.actual_spend) },
    ]
  }
  return <div><h2>Expenditure Dashboard</h2>
    <ReactECharts option={option} style={{height:280}} />
    <table><thead><tr><th>Programme</th><th>Item</th><th>Planned</th><th>Actual</th><th>Variance</th></tr></thead>
    <tbody>{data.map((r:any)=><tr key={r.id}><td>{r.programme}</td><td>{r.item}</td><td>{r.planned_budget}</td><td>{r.actual_spend}</td><td>{r.variance}</td></tr>)}</tbody></table>
    <p>Variance decomposition and procurement evidence available through explain endpoint.</p>
  </div>
}
