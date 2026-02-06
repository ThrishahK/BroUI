# BroCode Challenge Platform - Deployment Guide

This guide explains how to configure the database and run the API service for different environments.

## ⚙️ Environment Setup

### 1. Create Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env file with your configuration
```

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

## 🚀 Running the API Service

### Prerequisites
- Python 3.10+ installed
- Virtual environment activated
- Dependencies installed: `pip install -r requirements.txt`
- Database configured and verified

### Option A: Production Server (Recommended)
```bash
cd backend
source venv/bin/activate
python switch_database.py sqlite  # or postgresql as needed
python setup_database.py
python server.py
```
**Server will be available at**: `http://localhost:8000`

### Option B: Development Server (with auto-reload)
```bash
cd backend
source venv/bin/activate
python run.py
```
**Features**: Auto-reloads on code changes, better for development

### Verify Service is Running
```bash
# Test basic connectivity
curl http://localhost:8000/docs

# Test API endpoints
curl http://localhost:8000/api/questions/public/all

# Check service health
curl http://localhost:8000/api/health  # if available
```

### Service Endpoints
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

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

#### Database Issues:
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

#### API Service Issues:
**Port already in use**:
- Kill existing process: `lsof -ti:8000 | xargs kill -9`
- Or use different port: `uvicorn app.main:app --host 0.0.0.0 --port 8001`

**Module not found**:
- Ensure you're in virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Check if you're in the correct directory (`backend/`)

**Service won't start**:
- Check for syntax errors: `python -m py_compile server.py`
- Verify database connection: `python setup_database.py`
- Check logs for detailed error messages

**CORS errors in frontend**:
- Ensure frontend is configured to connect to correct backend URL
- Check CORS settings in FastAPI app configuration

## 📞 Support

If you encounter issues:
1. **Check service logs**: Look at terminal output when starting the service
2. **Verify database connection**: Run `python setup_database.py`
3. **Test API endpoints**: Use curl commands to test basic functionality
4. **Check service status**: Ensure the service is running on the correct port
5. **Verify environment**: Confirm virtual environment is activated
6. **Check dependencies**: Ensure all packages are installed correctly
7. **Review configuration**: Verify DATABASE_URL and other env vars are correct
