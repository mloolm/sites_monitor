// src/plugins/vuetify.js
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

export default createVuetify({
  components,
  directives,
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#1976D2', // Цвет основной темы
          secondary: '#424242', // Вторичный цвет
        },
      },
    },
  },
});