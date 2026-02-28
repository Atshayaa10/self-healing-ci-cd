import { useQuery } from '@tanstack/react-query'
import { fetchStats, fetchPipelines, fetchFailures, fetchFixes } from '../api/client'
import { Activity, AlertCircle, CheckCircle, TrendingUp } from 'lucide-react'

export default function Dashboard() {
  const { data: stats } = useQuery({ queryKey: ['stats'], queryFn: fetchStats })
  const { data: pipelines } = useQuery({ queryKey: ['pipelines'], queryFn: fetchPipelines })
  const { data: failures } = useQuery({ queryKey: ['failures'], queryFn: fetchFailures })
  const { data: fixes } = useQuery({ queryKey: ['fixes'], queryFn: fetchFixes })
  
  return (
    <div>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '2rem' }}>
        Dashboard
      </h1>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '1.5rem',
        marginBottom: '2rem'
      }}>
        <StatCard
          title="Total Pipelines"
          value={stats?.total_pipelines || 0}
          icon={<Activity size={24} />}
          color="#60a5fa"
        />
        <StatCard
          title="Total Failures"
          value={stats?.total_failures || 0}
          icon={<AlertCircle size={24} />}
          color="#f87171"
        />
        <StatCard
          title="Successful Fixes"
          value={stats?.successful_fixes || 0}
          icon={<CheckCircle size={24} />}
          color="#34d399"
        />
        <StatCard
          title="Success Rate"
          value={`${stats?.success_rate || 0}%`}
          icon={<TrendingUp size={24} />}
          color="#a78bfa"
        />
      </div>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '1.5rem'
      }}>
        <RecentActivity title="Recent Pipelines" items={pipelines?.slice(0, 5) || []} />
        <RecentActivity title="Recent Failures" items={failures?.slice(0, 5) || []} />
      </div>
    </div>
  )
}

function StatCard({ title, value, icon, color }: any) {
  return (
    <div style={{
      background: '#1e293b',
      padding: '1.5rem',
      borderRadius: '0.75rem',
      border: '1px solid #334155'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
        <div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
            {title}
          </p>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color }}>
            {value}
          </p>
        </div>
        <div style={{ color, opacity: 0.8 }}>
          {icon}
        </div>
      </div>
    </div>
  )
}

function RecentActivity({ title, items }: any) {
  return (
    <div style={{
      background: '#1e293b',
      padding: '1.5rem',
      borderRadius: '0.75rem',
      border: '1px solid #334155'
    }}>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem' }}>
        {title}
      </h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {items.length === 0 ? (
          <p style={{ color: '#64748b', textAlign: 'center', padding: '2rem' }}>
            No data available
          </p>
        ) : (
          items.map((item: any, idx: number) => (
            <div
              key={idx}
              style={{
                padding: '0.75rem',
                background: '#0f172a',
                borderRadius: '0.5rem',
                fontSize: '0.875rem'
              }}
            >
              <div style={{ fontWeight: '500', marginBottom: '0.25rem' }}>
                {item.repository || item.error_message?.substring(0, 50)}
              </div>
              <div style={{ color: '#64748b', fontSize: '0.75rem' }}>
                {item.branch || item.error_category}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
