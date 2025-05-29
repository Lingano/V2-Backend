# 🔒 Security Setup Guide

## ⚠️ BEFORE DEPLOYING TO PRODUCTION

### 1. Generate a New Secret Key

```python
# Run this in your Django shell to generate a new secret key
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 2. Environment Variables Setup

1. Copy `.env.example` to `.env`
2. Fill in your actual values:
    - `SECRET_KEY`: Use the generated key from step 1
    - `DEBUG`: Set to `False` for production
    - `DB_PASSWORD`: Your actual database password
    - API keys for external services (optional)

### 3. Security Checklist

-   [ ] New SECRET_KEY generated and set in .env
-   [ ] DEBUG=False in production
-   [ ] Database password set in environment variables
-   [ ] .env file added to .gitignore (already done)
-   [ ] No hardcoded credentials in code
-   [ ] ALLOWED_HOSTS configured for your domain

### 4. Development vs Production

**Development:**

```bash
DEBUG=True
SECRET_KEY=your-dev-key
DB_PASSWORD=your-local-db-password
```

**Production:**

```bash
DEBUG=False
SECRET_KEY=your-super-secure-production-key
DB_PASSWORD=your-secure-production-password
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

### 5. Additional Security Measures

-   Use HTTPS in production
-   Set up proper firewall rules
-   Use a secret management service for sensitive data
-   Regularly rotate API keys and passwords
-   Monitor for security vulnerabilities

## 🚨 Never Commit These to Git:

-   `.env` files
-   Database passwords
-   API keys
-   Secret keys
-   Any sensitive configuration
