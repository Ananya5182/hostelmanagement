# ==========================================
# Production Dockerfile for Hostel Frontend & Reverse Proxy
# Base: Nginx 1.25 Alpine (lightweight & high performance)
# ==========================================

FROM nginx:1.25-alpine

# Remove default Nginx welcome configuration
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration with reverse proxy definitions
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static frontend web assets
COPY static/ /usr/share/nginx/html/

# Expose HTTP port 80
EXPOSE 80

# Healthcheck to verify Nginx web server responsiveness
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost/ || exit 1

# Launch Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
