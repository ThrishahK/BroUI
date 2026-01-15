# BroCode Challenge Platform - Database Deployment Guide

This guide explains how to configure the database for different environments.

## 📊 Database Options

### 1. SQLite (Development - Current)
```env
DATABASE_URL=sqlite:///./brocode.db
```
**Pros**: Zero configuration, file-based, perfect for development
**Cons**: Not suitable for concurrent users, single-file storage

### 2. Local PostgreSQL Server
```env
DATABASE_URL=postgresql://brocode_user:your_password@localhost:5432/brocode_db
```
**Setup Steps**:
```bash
# Install PostgreSQL (if not already installed)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE brocode_db;
CREATE USER brocode_user WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE brocode_db TO brocode_user;
\q

# Update .env file
DATABASE_URL=postgresql://brocode_user:your_password@localhost:5432/brocode_db
```

### 3. Remote PostgreSQL Server (Competition)
```env
DATABASE_URL=postgresql://brocode_user:competition_password@your-server.com:5432/brocode_competition
```

## 🔧 Database Setup Commands

### Check Current Database Status
```bash
cd backend
source venv/bin/activate
python setup_database.py
```

### Switch Database Configuration

1. **Edit the `.env` file**:
   ```bash
   nano .env
   ```

2. **Update DATABASE_URL**:
   ```env
   # For your local PostgreSQL server
   DATABASE_URL=postgresql://brocode_user:your_password@localhost:5432/brocode_db
   ```

3. **Install PostgreSQL driver** (if switching from SQLite):
   ```bash
   pip install psycopg2-binary
   ```

4. **Run setup to verify**:
   ```bash
   python setup_database.py
   ```

## 🚀 Deployment Checklist

### For Local Server Deployment:
- [ ] PostgreSQL installed and running
- [ ] Database `brocode_db` created
- [ ] User `brocode_user` created with password
- [ ] Proper permissions granted
- [ ] `DATABASE_URL` updated in `.env`
- [ ] `psycopg2-binary` installed
- [ ] Database setup verified with `python setup_database.py`

### For Competition Server:
- [ ] Remote PostgreSQL server accessible
- [ ] Database credentials provided
- [ ] Network connectivity confirmed
- [ ] Firewall rules allow connections
- [ ] SSL/TLS encryption enabled (recommended)

## 🔒 Security Considerations

### Database Security:
- Use strong passwords for database users
- Restrict database access to necessary IPs only
- Enable SSL/TLS for remote connections
- Regularly backup database
- Use connection pooling for production

### Environment Variables:
- Never commit `.env` files to version control
- Use different credentials for each environment
- Rotate passwords regularly
- Use secret management services in production

## 🧪 Testing Database Switch

1. **Backup current data** (if any):
   ```bash
   cp brocode.db brocode.db.backup
   ```

2. **Update DATABASE_URL** in `.env`

3. **Run setup script**:
   ```bash
   python setup_database.py
   ```

4. **Start backend and test**:
   ```bash
   python server.py
   ```

5. **Verify API endpoints work**:
   ```bash
   curl http://localhost:8000/api/questions/public/all
   ```

## 📞 Troubleshooting

### Common Issues:

**Connection refused**:
- Check if PostgreSQL is running: `sudo systemctl status postgresql`
- Verify DATABASE_URL format
- Check firewall settings

**Authentication failed**:
- Verify username/password in DATABASE_URL
- Check if user has proper permissions
- Ensure database exists

**Table not found**:
- Run `python setup_database.py` to create tables
- Check if Base.metadata.create_all() is called in main.py

**Import errors**:
- Ensure psycopg2-binary is installed for PostgreSQL
- Check Python path and virtual environment

## 📞 Support

If you encounter issues:
1. Check the terminal output for error messages
2. Run `python setup_database.py` for diagnostics
3. Verify your DATABASE_URL format
4. Ensure database server is running and accessible
