// src/api.js
import axios from "axios";

const apiClient = axios.create({
  baseURL: "/api", // Используем прокси
  withCredentials: false, // Если не используете cookies
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
      headers: { Authorization: `Bearer ${token}` },
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
        { url: url },
        {
            headers: { Authorization: `Bearer ${token}` } // Заголовки
        }
    );
  },

  deleteSite(token, id){
    return apiClient.post(
        '/delete-site',
        { site_id: id },
        {
            headers: { Authorization: `Bearer ${token}` } // Заголовки
        }
    );
  },

  getNotificationData(token){
    return apiClient.get("/user-noty-providers", {
      headers: {Authorization: `Bearer ${token}`},
    });
  },

  getTelegramAuthCode(token){
    return apiClient.get("/get-telegram-auth-code", {
      headers: {Authorization: `Bearer ${token}`},
    });
  },

  sendNotyMessage(token, message)
  {
        return apiClient.post(
        '/noty-message',
        { message: message},
        {
            headers: { Authorization: `Bearer ${token}` } // Заголовки
        }
    );

  }

};