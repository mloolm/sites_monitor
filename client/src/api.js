import axios from "axios";

const apiClient = axios.create({
    baseURL: "/api", // Using a proxy.
    withCredentials: false,
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
    },
});

export default {
    login(username, password) {
        return apiClient.post("/token", {
            username,
            password,
        });
    },
    getUserData(token) {
        return apiClient.get("/user-data", {
            headers: {Authorization: `Bearer ${token}`},
        });
    },
    getSites(token) {
        return apiClient.get("/sites/", {
            headers: {Authorization: `Bearer ${token}`},
        });
    },

    addSite(token, url) {
        return apiClient.post(
            '/add-site',
            {url: url},
            {
                headers: {Authorization: `Bearer ${token}`}
            }
        );
    },

    deleteSite(token, id) {
        return apiClient.post(
            '/delete-site',
            {site_id: id},
            {
                headers: {Authorization: `Bearer ${token}`}
            }
        );
    },

    getNotificationData(token) {
        return apiClient.get("/user-noty-providers", {
            headers: {Authorization: `Bearer ${token}`},
        });
    },

    getTelegramAuthCode(token) {
        return apiClient.get("/get-telegram-auth-code", {
            headers: {Authorization: `Bearer ${token}`},
        });
    },

    getVapidKey(token) {
        return apiClient.get("/vapid-key", {
            headers: {Authorization: `Bearer ${token}`},
        });
    },

    sendNotyMessage(token, message) {
        return apiClient.post(
            '/noty-message',
            {message: message},
            {
                headers: {Authorization: `Bearer ${token}`}
            }
        );
    },

    subscribePWA(token, data) {
        return apiClient.post(
            '/subscribe',
            {data: data},
            {
                headers: {Authorization: `Bearer ${token}`}
            }
        );
    },

    getSiteData(token, site_id, period = 'week') {
        if (!period) {
            period = 'week'
        }
        return apiClient.get(
            '/sites/' + site_id + '/' + period,
            {
                headers: {Authorization: `Bearer ${token}`}
            }
        );
    },

    getNoticesTotalPages(token) {
        return apiClient.get(
            '/notifications-page-count',
            {
                headers: {Authorization: `Bearer ${token}`}
            }
        );
    },

    getNotices(token, page = 1) {
        return apiClient.get(
            '/notifications/' + page,
            {
                headers: {Authorization: `Bearer ${token}`}
            }
        );
    }
};