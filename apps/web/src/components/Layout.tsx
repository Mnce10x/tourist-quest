import { Link } from 'react-router-dom'
import { PropsWithChildren } from 'react'

const pages = [
  ['/', 'Executive'],
  ['/performance', 'Performance'],
  ['/expenditure', 'Expenditure'],
  ['/reports', 'Reports'],
  ['/media', 'Media'],
  ['/recommendations', 'Recommendations'],
  ['/audit', 'Data Quality']
]

export function Layout({ children }: PropsWithChildren) {
  return <div style={{fontFamily:'Inter, sans-serif', padding:20}}>
    <h1>Tourism Performance & Media Intelligence</h1>
    <nav style={{display:'flex', gap:12, flexWrap:'wrap'}}>{pages.map(([p,t]) => <Link key={p} to={p}>{t}</Link>)}</nav>
    <div style={{marginTop:20}}>{children}</div>
  </div>
}
