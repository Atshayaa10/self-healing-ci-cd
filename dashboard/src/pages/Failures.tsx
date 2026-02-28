import { useQuery } from '@tanstack/react-query'
import { fetchFailures } from '../api/client'
import { formatDistanceToNow } from 'date-fns'

export default function Failures() {
  const { data: failures, isLoading } = useQuery({ 
    queryKey: ['failures'], 
    queryFn: fetchFailures 
  })
  
  if (isLoading) return <div>Loading...</div>
  
  return (
    <div>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '2rem' }}>
        Failure Analyses
      </h1>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {failures?.map((failure: any) => (
          <div
            key={failure.id}
            style={{
              background: '#1e293b',
              padding: '1.5rem',
              borderRadius: '0.75rem',
              border: '1px solid #334155'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <div>
                <CategoryBadge category={failure.error_category} />
                <span style={{ 
                  marginLeft: '1rem', 
                  fontSize: '0.875rem', 
                  color: '#64748b' 
                }}>
                  Confidence: {failure.confidence_score}%
                </span>
              </div>
              <span style={{ fontSize: '0.875rem', color: '#64748b' }}>
                {formatDistanceToNow(new Date(failure.analyzed_at), { addSuffix: true })}
              </span>
            </div>
            
            <div style={{ marginBottom: '0.75rem' }}>
              <strong style={{ color: '#f87171' }}>Error:</strong>
              <p style={{ marginTop: '0.5rem', color: '#cbd5e1' }}>
                {failure.error_message}
              </p>
            </div>
            
            {failure.root_cause && (
              <div>
                <strong style={{ color: '#60a5fa' }}>Root Cause:</strong>
                <p style={{ marginTop: '0.5rem', color: '#cbd5e1' }}>
                  {failure.root_cause}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function CategoryBadge({ category }: { category: string }) {
  const colors: any = {
    dependency_conflict: '#f59e0b',
    test_failure: '#ef4444',
    syntax_error: '#ec4899',
    configuration_error: '#8b5cf6',
    environment_issue: '#06b6d4',
    timeout: '#f97316',
    resource_limit: '#84cc16',
    unknown: '#6b7280'
  }
  
  return (
    <span style={{
      padding: '0.25rem 0.75rem',
      borderRadius: '0.375rem',
      fontSize: '0.75rem',
      fontWeight: '500',
      background: `${colors[category] || colors.unknown}20`,
      color: colors[category] || colors.unknown
    }}>
      {category.replace(/_/g, ' ')}
    </span>
  )
}
