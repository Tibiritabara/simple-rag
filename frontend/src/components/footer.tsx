export function Footer() {
  return (
    <footer className="border-t dark:border-gray-700">
      <div className="container mx-auto px-4 py-4 text-center text-sm text-gray-600 dark:text-gray-400">
        © {new Date().getFullYear()} Ricardo Santos. All rights reserved.
      </div>
    </footer>
  );
} 
