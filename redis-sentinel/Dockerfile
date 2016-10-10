FROM redis
COPY redis-sentinel.conf /usr/local/etc/redis/redis-sentinel.conf
RUN chown redis /usr/local/etc/redis/redis-sentinel.conf
EXPOSE 26379
CMD [ "redis-sentinel", "/usr/local/etc/redis/redis-sentinel.conf" ]
