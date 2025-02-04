import { Sidebar } from '@/components/sidebar';
import { ChatView } from '@/components/chat-view';

export default function Home() {
  return (
    <div className="flex gap-6 h-[calc(100vh-8rem)]">
      <Sidebar />
      <ChatView />
    </div>
  );
}
