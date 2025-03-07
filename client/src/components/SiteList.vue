<!-- client/src/components/SiteList.vue -->
<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>URL</th>
          <th>Status</th>
          <th>Last Checked</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="site in sites" :key="site.id">
          <td>{{ site.url }}</td>
          <td :class="statusClass(site.is_online)">
            {{ site.is_online ? 'Online' : 'Offline' }}
          </td>
          <td>{{ site.last_checked }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sites: []
    };
  },
  methods: {
    async fetchSites() {
      const response = await axios.get('http://localhost:8000/api/sites/');
      this.sites = response.data;
    },
    statusClass(isOnline) {
      return { 'status-online': isOnline, 'status-offline': !isOnline };
    }
  },
  mounted() {
    this.fetchSites();
  }
};
</script>

<style>
.status-online { color: green; }
.status-offline { color: red; }
</style>