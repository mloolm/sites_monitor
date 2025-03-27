import { precacheAndRoute } from 'workbox-precaching';

self.addEventListener('push', (event) => {
  console.log('New push-notice received');
  if (!event.data) return;

  const data = event.data.json();
  event.waitUntil(
    self.registration.showNotification(data.title || 'New notice', {
      body: data.body || 'Сообщение без текста',
      icon: '/img/icons/android-chrome-192x192.png',
      badge: '/img/icons/android-chrome-512x512.png',
      data: { url: data.url || '/' },
    })
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data?.url || '/')
  );
});

// Подключаем Workbox для кэширования
precacheAndRoute(self.__WB_MANIFEST || []);
