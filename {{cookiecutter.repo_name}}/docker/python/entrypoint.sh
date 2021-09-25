#!/bin/bash -eu
mkdir -p /var/app/run /var/app/static
chown -R app:app /var/app
# Fill in defaults if /etc/app is an empty volume
for path in /etc/app-defaults/*; do
  name=$(basename "$path")
  if [[ ! -e "/etc/app/$name" ]]; then
    echo "+ cp /etc/app-defaults/$name /etc/app/$name"
    cp "/etc/app-defaults/$name" "/etc/app/$name"
  fi
done
if [[ -n "${DJANGO_COLLECTSTATIC:-}" ]]; then
  set -x
  pysu app django-admin collectstatic --noinput --clear -v0
fi
if [[ -n "${DJANGO_DB_MIGRATE:-}" ]]; then
  set -x
  holdup --verbose pg://$DJANGO_DB_USER:$DJANGO_DB_PASSWORD@$DJANGO_DB_HOST:5432/$DJANGO_DB_NAME
  pysu app django-admin migrate --noinput --fake-initial
fi
set -x
exec "$@"
