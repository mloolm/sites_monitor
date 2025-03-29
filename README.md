# Website Monitoring and Analysis Service

This service provides regular monitoring and analysis of websites, ensuring their availability and security through various features.

## Features

- **Regular Website Availability Checks**: Monitor the accessibility of websites at defined intervals.
- **SSL Certificate Monitoring**: Regularly check the status of SSL certificates.
- **Downtime Notifications**: Receive alerts when a website becomes unavailable.
- **SSL Expiration Notifications**: Get notified about upcoming SSL expiration dates, as well as alerts for expired or invalid SSL certificates.
- **Notification Channels**: Receive notifications via Telegram and push notifications.
- **Progressive Web App (PWA)**: Use the service as a website or as a mobile application.
- **User Management**: Manage users through the command line interface.

## Technology Stack

- **Server**: Python (FastAPI)
- **Client**: Vue.js
- **Containerization**: Docker

## Installation

Follow these steps to set up the service:

1. **Install Docker and Nginx (or Apache)**:
   Ensure that Docker and a web server (Nginx or Apache) are installed on your system.

2. **Clone the Repository**:
   Download this repository to your local machine.

   ```bash
   git clone https://github.com/mloolm/sites_monitor
   cd sites_monitor
   ```

3. **Build the Docker Containers**:
   Run the following command to build the Docker containers:

   ```bash
   docker-compose up --build
   ```

4. **Create a User**:
   Create a user by executing the following command:

   ```bash
   make create_user LOGIN PASSWORD
   ```

   To see other available commands, run:

   ```bash
   make help
   ```

5. **Configure Web Server**:
   Insert the domain or subdomain where the server and client will operate into the configuration files:
   - For Nginx, copy `sm_nginx.conf` from the `webserver_config` folder to `nginx/conf.d/`.
   - For Apache, copy `sm_apache.conf` to `/apache2/sites-available/` and enable the site with:

   ```bash
   a2ensite sm_apache
   ```

6. **Restart the Web Server**:
   Restart your web server to apply the changes.

7. **Set Up SSL**:
   It is recommended to use Certbot for easy SSL configuration.

## Roadmap

- [x] Basic website monitoring
- [x] SSL certificate checks
- [x] Telegram notifications and push-notifications
- [ ] Website analysis: broken link checking, slow-loading pages detection, heavy images identification  



## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License

## Contact

For any inquiries or support, please reach out to [krasheninin.p.a@gmail.com].
```

