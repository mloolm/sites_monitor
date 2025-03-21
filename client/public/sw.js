self.addEventListener('push', (event) => {
  console.log('Получено push-уведомление');

  if (!event.data) {
    return;
  }

  try {
    const data = event.data.json();
    console.log('New push:', data);

    event.waitUntil(
      self.registration.showNotification(data.title || 'New notice', {
        body: data.body || 'Сообщение без текста',
        icon: '/img/icons/android-chrome-192x192.png',
        badge: '/img/icons/android-chrome-512x512.png',
        data: { url: data.url || '/dashboard' },
      })
    );
  } catch (error) {
    console.error('Ошибка при парсинге данных push-уведомления:', error);
  }
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  const targetUrl = event.notification.data?.url || '/dashboard';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {

        if (client.url.includes(targetUrl) && 'focus' in client) {
          //console.log('Focus to:', client.url);
          return client.focus();
        }
      }
      return clients.openWindow(targetUrl);
    }).catch((error) => console.error('Ошибка при обработке клика по уведомлению:', error))
  );
});
