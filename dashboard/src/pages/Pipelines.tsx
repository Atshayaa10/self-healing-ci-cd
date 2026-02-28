import { useQuery } from '@tanstack/react-query'
import { fetchPipelines } from '../api/client'
import { formatDistanceToNow } from 'date-fns'

export default function Pipelines() {
  const { data: pipelines, isLoading } = useQuery({ 
    queryKey: ['pipelines'], 
    queryFn: fetchPipelines 
  })
  
  if (isLoading) return <div>Loading...</div>
  
  return (
    <div>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '2rem' }}>
        Pipelines
      </h1>
      
      <div style={{
        background: '#1e293b',
        borderRadius: '0.75rem',
        border: '1px solid #334155',
        overflow: 'hidden'
      }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#0f172a', borderBottom: '1px solid #334155' }}>
              <th style={thStyle}>Repository</th>
              <th style={thStyle}>Branch</th>
              <th style={thStyle}>Commit</th>
              <th style={thStyle}>Status</th>
              <th style={thStyle}>Started</th>
            </tr>
          </thead>
          <tbody>
            {pipelines?.map((pipeline: any) => (
              <tr key={pipeline.id} style={{ borderBottom: '1px solid #334155' }}>
                <td style={tdStyle}>{pipeline.repository}</td>
                <td style={tdStyle}>{pipeline.branch}</td>
                <td style={tdStyle}>
                  <code style={{ fontSize: '0.875rem' }}>
                    {pipeline.commit_sha.substring(0, 7)}
                  </code>
                </td>
                <td style={tdStyle}>
                  <StatusBadge status={pipeline.status} />
                </td>
                <td style={tdStyle}>
                  {formatDistanceToNow(new Date(pipeline.started_at), { addSuffix: true })}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

const thStyle = {
  padding: '1rem',
  textAlign: 'left' as const,
  fontSize: '0.875rem',
  fontWeight: '600',
  color: '#94a3b8'
}

const tdStyle = {
  padding: '1rem',
  fontSize: '0.875rem'
}

function StatusBadge({ status }: { status: string }) {
  const colors: any = {
    success: '#34d399',
    failure: '#f87171',
    pending: '#fbbf24',
    running: '#60a5fa'
  }
  
  return (
    <span style={{
      padding: '0.25rem 0.75rem',
      borderRadius: '9999px',
      fontSize: '0.75rem',
      fontWeight: '500',
      background: `${colors[status]}20`,
      color: colors[status]
    }}>
      {status}
    </span>
  )
}
