'use client';

import {useEffect} from 'react';
import {ResponsiveLayout, Spinner} from '@telefonica/mistica';
import {useRouter} from 'next/navigation';
import {useAuth} from '@/lib/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({children}: ProtectedRouteProps) {
  const {isAuthenticated, loading} = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [loading, isAuthenticated, router]);

  if (loading) {
    return (
      <ResponsiveLayout>
        <div style={{display: 'flex', justifyContent: 'center', paddingTop: 48}}>
          <Spinner size={48} />
        </div>
      </ResponsiveLayout>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
