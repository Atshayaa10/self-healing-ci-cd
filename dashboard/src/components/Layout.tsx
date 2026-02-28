import { Outlet, Link, useLocation } from 'react-router-dom'
import { Activity, GitBranch, AlertCircle, Wrench } from 'lucide-react'

export default function Layout() {
  const location = useLocation()
  
  const isActive = (path: string) => location.pathname === path
  
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <nav style={{
        width: '250px',
        background: '#1e293b',
        padding: '2rem 1rem',
        borderRight: '1px solid #334155'
      }}>
        <h1 style={{ 
          fontSize: '1.5rem', 
          fontWeight: 'bold', 
          marginBottom: '2rem',
          color: '#60a5fa'
        }}>
          🤖 CI Healer
        </h1>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <NavLink to="/" icon={<Activity size={20} />} active={isActive('/')}>
            Dashboard
          </NavLink>
          <NavLink to="/pipelines" icon={<GitBranch size={20} />} active={isActive('/pipelines')}>
            Pipelines
          </NavLink>
          <NavLink to="/failures" icon={<AlertCircle size={20} />} active={isActive('/failures')}>
            Failures
          </NavLink>
          <NavLink to="/fixes" icon={<Wrench size={20} />} active={isActive('/fixes')}>
            Fixes
          </NavLink>
        </div>
      </nav>
      
      <main style={{ flex: 1, padding: '2rem', overflow: 'auto' }}>
        <Outlet />
      </main>
    </div>
  )
}

function NavLink({ to, icon, children, active }: any) {
  return (
    <Link
      to={to}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
        padding: '0.75rem 1rem',
        borderRadius: '0.5rem',
        textDecoration: 'none',
        color: active ? '#60a5fa' : '#94a3b8',
        background: active ? '#1e40af20' : 'transparent',
        transition: 'all 0.2s'
      }}
    >
      {icon}
      <span>{children}</span>
    </Link>
  )
}
