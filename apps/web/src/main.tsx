import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Layout } from './components/Layout'
import { Filters } from './components/Filters'
import { Executive } from './pages/Executive'
import { Performance } from './pages/Performance'
import { Expenditure } from './pages/Expenditure'
import { Reports } from './pages/Reports'
import { Media } from './pages/Media'
import { Recommendations } from './pages/Recommendations'
import { Audit } from './pages/Audit'

const client = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={client}>
      <BrowserRouter>
        <Layout>
          <Filters />
          <Routes>
            <Route path='/' element={<Executive />} />
            <Route path='/performance' element={<Performance />} />
            <Route path='/expenditure' element={<Expenditure />} />
            <Route path='/reports' element={<Reports />} />
            <Route path='/media' element={<Media />} />
            <Route path='/recommendations' element={<Recommendations />} />
            <Route path='/audit' element={<Audit />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
)
