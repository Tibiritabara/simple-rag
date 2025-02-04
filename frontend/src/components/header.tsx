'use client';

import { useTheme } from 'next-themes';
import { Moon, Sun } from 'lucide-react';

export function Header() {
  const { theme, setTheme } = useTheme();

  return (
    <header className="border-b dark:border-gray-700">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Forgent Test</h1>
        <button
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? (
            <Sun className="h-5 w-5" />
          ) : (
            <Moon className="h-5 w-5" />
          )}
        </button>
      </div>
    </header>
  );
} 
