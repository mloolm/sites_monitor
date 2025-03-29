<template>
  <v-container class="notification-container">
    <h2 class="text-center">Уведомления</h2>
    <!-- top pagination -->
    <div v-if="total_pages > 1" class="pagination top-pagination">
      <v-pagination
          v-model="current_page"
          :length="total_pages"
          :total-visible="5"
          @update:modelValue="changePage"
      ></v-pagination>
    </div>

    <!-- Loading or error -->
    <v-skeleton-loader v-if="loading" type="list-item-avatar-three-line" :loading="loading"></v-skeleton-loader>
    <v-alert v-else-if="error" type="error">{{ error }}</v-alert>
    <div v-else>
      <!-- Notices list -->
      <v-list v-if="notifications.length > 0">
        <v-list-item v-for="(notice, index) in notifications" :key="index" class="notification-item">
          <v-list-item-content>
            <v-list-item-title>{{ notice.title }}</v-list-item-title>
            <v-list-item-subtitle>{{ formatDate(notice.created_at) }}</v-list-item-subtitle>
            <v-list-item-subtitle>{{ notice.message }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <!-- If no notices -->
      <v-alert v-else type="info">No notices yet</v-alert>
    </div>

    <!-- bottom pagination -->
    <div v-if="total_pages > 1" class="pagination bottom-pagination">
      <v-pagination
          v-model="current_page"
          :length="total_pages"
          :total-visible="5"
          @update:modelValue="changePage"
      ></v-pagination>
    </div>
  </v-container>
</template>

<script>
import {onMounted, ref} from 'vue';
import api from '../api';

export default {
  name: 'NotificationList',
  setup() {
    const token = localStorage.getItem('token');
    const notifications = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const total_pages = ref(0);
    const current_page = ref(1);

    // Date formatting function
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleString(); // Formats the date into a human-readable format
    };

    // Function to get notifications
    const fetchNotificationList = async () => {
      try {
        const response = await api.getNotices(token, current_page.value);
        notifications.value = response.data;
      } catch (err) {
        error.value = 'Error fetching notifications';
        console.error('Error fetching notifications:', err);
      } finally {
        loading.value = false;
      }
    };

    // Function to get the total number of pages
    const fetchTotalPages = async () => {
      try {
        const response = await api.getNoticesTotalPages(token);
        total_pages.value = response.data;
      } catch (err) {
        console.error('Error fetching total pages:', err);
      }
    };

    // Function to change the page
    const changePage = (page) => {
      if (page < 1 || page > total_pages.value) return;
      current_page.value = page;
      fetchNotificationList(); // Loading notifications for the new page
    };


    onMounted(() => {
      fetchNotificationList();
      fetchTotalPages();
    });

    return {
      notifications,
      loading,
      error,
      formatDate,
      total_pages,
      current_page,
      changePage,
    };
  },
};
</script>

<style scoped>
.notification-container {
  max-width: 800px;
  margin: 0 auto;
}

.pagination.top-pagination {
  margin-bottom: 20px;
}

.pagination.bottom-pagination {
  margin-top: 20px;
}

.notification-item {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
}
</style>