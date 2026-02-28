import { useQuery } from '@tanstack/react-query'
import { fetchFixes } from '../api/client'
import { formatDistanceToNow } from 'date-fns'
import { CheckCircle, XCircle, Clock } from 'lucide-react'

export default function Fixes() {
  const { data: fixes, isLoading } = useQuery({ 
    queryKey: ['fixes'], 
    queryFn: fetchFixes 
  })
  
  if (isLoading) return <div>Loading...</div>
  
  return (
    <div>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '2rem' }}>
        Applied Fixes
      </h1>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {fixes?.map((fix: any) => (
          <div
            key={fix.id}
            style={{
              background: '#1e293b',
              padding: '1.5rem',
              borderRadius: '0.75rem',
              border: '1px solid #334155'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <SuccessIcon success={fix.success} />
                <div>
                  <div style={{ fontWeight: '600', fontSize: '1.125rem' }}>
                    {fix.fix_type.replace(/_/g, ' ')}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#64748b', marginTop: '0.25rem' }}>
                    {fix.description}
                  </div>
                </div>
              </div>
              <StatusBadge status={fix.status} />
            </div>
            
            {fix.commit_sha && (
              <div style={{ 
                marginTop: '1rem', 
                padding: '0.75rem', 
                background: '#0f172a', 
                borderRadius: '0.5rem',
                fontSize: '0.875rem'
              }}>
                <strong>Commit:</strong> <code>{fix.commit_sha.substring(0, 7)}</code>
              </div>
            )}
            
            {fix.applied_at && (
              <div style={{ marginTop: '0.75rem', fontSize: '0.875rem', color: '#64748b' }}>
                Applied {formatDistanceToNow(new Date(fix.applied_at), { addSuffix: true })}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function SuccessIcon({ success }: { success: boolean }) {
  return success ? (
    <CheckCircle size={24} color="#34d399" />
  ) : (
    <XCircle size={24} color="#f87171" />
  )
}

function StatusBadge({ status }: { status: string }) {
  const colors: any = {
    pending: '#fbbf24',
    in_progress: '#60a5fa',
    applied: '#34d399',
    verified: '#10b981',
    failed: '#f87171'
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
      {status.replace(/_/g, ' ')}
    </span>
  )
}
