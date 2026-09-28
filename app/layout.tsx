import type {Metadata} from 'next';
import './globals.css'; // Global styles

export const metadata: Metadata = {
  title: 'Automated Restore-Readiness Drill | Multiplayer Session State',
  description: 'Automated restore-readiness drill engine and audit dashboard for multiplayer session-state systems, verifying RTO, RPO, and state integrity.',
  openGraph: {
    title: 'Automated Restore-Readiness Drill | Multiplayer Session State',
    description: 'Automated restore-readiness drill engine and audit dashboard for multiplayer session-state systems, verifying RTO, RPO, and state integrity.',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Automated Restore-Readiness Drill | Multiplayer Session State',
    description: 'Automated restore-readiness drill engine and audit dashboard for multiplayer session-state systems, verifying RTO, RPO, and state integrity.',
  },
};

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="en">
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}
