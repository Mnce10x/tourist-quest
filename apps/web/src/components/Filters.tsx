export function Filters() {
  return <div style={{display:'grid',gridTemplateColumns:'repeat(6, minmax(120px, 1fr))', gap:8, margin:'16px 0'}}>
    {['Date Range','Quarter','Programme','KPI','Topic','Outlet'].map(f => <input key={f} placeholder={f} style={{padding:8}} />)}
  </div>
}
