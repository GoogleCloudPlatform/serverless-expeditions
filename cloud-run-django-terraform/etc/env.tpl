# Django Settings
DATABASE_URL="postgres://${user.name}:${user.password}@//cloudsql/${instance.project}:${instance.region}:${instance.name}/${database.name}"
GS_BUCKET_NAME="${bucket}"
SECRET_KEY="${secret_key}"