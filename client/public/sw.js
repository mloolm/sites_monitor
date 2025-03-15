self.addEventListener('push', (event) => {
  console.log('Получено push-уведомление');
  if (!event.data) return;

  const data = event.data.json();
  event.waitUntil(
    self.registration.showNotification(data.title || 'Новое уведомление', {
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

