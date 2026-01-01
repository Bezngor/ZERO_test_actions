# GitHub Actions Workflows

## deploy.yml

Автоматический workflow для сборки Docker образа и деплоя на удаленный сервер.

### Как это работает

**Джоба 1: Build and Push**
1. Чекаутит код репозитория
2. Логинится в GitHub Container Registry (GHCR)
3. Собирает Docker образ
4. Пушит образ в GHCR с тегами `latest` и по SHA коммита

**Джоба 2: Deploy**
1. Подключается к удаленному серверу по SSH
2. Логинится в GHCR на сервере
3. Останавливает и удаляет старый контейнер
4. Скачивает новый образ из GHCR
5. Запускает новый контейнер
6. Очищает неиспользуемые образы

### Необходимые секреты GitHub

Добавьте следующие секреты в настройках репозитория:
**Settings → Secrets and variables → Actions → New repository secret**

| Секрет | Описание | Пример |
|--------|----------|--------|
| `REMOTE_HOST` | IP адрес или домен удаленного сервера | `192.168.1.100` или `example.com` |
| `REMOTE_USER` | Имя пользователя для SSH | `ubuntu` или `root` |
| `SSH_PRIVATE_KEY` | Приватный SSH ключ для подключения | Содержимое файла `~/.ssh/id_rsa` |
| `REMOTE_PORT` | (Опционально) Порт SSH | `22` (по умолчанию) |

**Примечание:** `GITHUB_TOKEN` создается автоматически и не требует настройки.

### Генерация SSH ключа

Если у вас еще нет SSH ключа:

```bash
# На вашем компьютере
ssh-keygen -t rsa -b 4096 -C "github-actions"

# Скопируйте публичный ключ на сервер
ssh-copy-id -i ~/.ssh/id_rsa.pub user@your-server.com

# Скопируйте ПРИВАТНЫЙ ключ в секреты GitHub
cat ~/.ssh/id_rsa
```

### Подготовка сервера

На удаленном сервере должен быть установлен Docker:

```bash
# Установка Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Перелогиньтесь или выполните
newgrp docker
```

### Запуск workflow

Workflow запускается автоматически при:
- Push в ветки `main` или `master`
- Ручном запуске через вкладку Actions в GitHub

### Проверка деплоя

После успешного деплоя, API будет доступен по адресу:
```
http://your-server-ip:8000
http://your-server-ip:8000/docs
```

### Отладка

Если деплой не работает:

1. Проверьте логи в Actions на GitHub
2. Убедитесь, что все секреты настроены правильно
3. Проверьте SSH подключение вручную:
   ```bash
   ssh -i ~/.ssh/id_rsa user@your-server-ip
   ```
4. Убедитесь, что на сервере установлен Docker и пользователь в группе docker
5. Проверьте, что порт 8000 открыт в файрволе:
   ```bash
   sudo ufw allow 8000
   ```

### Настройка образа как публичного

По умолчанию образы в GHCR приватные. Чтобы сделать образ публичным:

1. Перейдите на страницу пакета: `https://github.com/users/YOUR_USERNAME/packages/container/REPO_NAME`
2. **Package settings** → **Change visibility** → **Public**

Или оставьте приватным и сервер будет использовать `GITHUB_TOKEN` для доступа.

