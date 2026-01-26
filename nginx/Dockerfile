FROM nginx:alpine

# Удаляем дефолтные конфиги
RUN rm /etc/nginx/conf.d/default.conf

# Копируем свой конфиг 
COPY fefu_lab.conf /etc/nginx/conf.d/

# Права (если нужно)
RUN chown -R nginx:nginx /etc/nginx/conf.d

# HEALTHCHECK на порт 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost || exit 1