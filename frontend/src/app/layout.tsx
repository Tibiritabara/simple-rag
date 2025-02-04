import { Inter } from 'next/font/google';
import './globals.css';
import { ThemeProvider } from './providers';
import { Header } from '@/components/header';
import { Footer } from '@/components/footer';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Forgent Test',
  description: 'A Next.js application for file management and AI chat',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen flex flex-col`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Header />
          <main className="flex-1 container mx-auto p-4">
            {children}
          </main>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
}
