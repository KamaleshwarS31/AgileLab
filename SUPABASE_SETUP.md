# 🚀 Supabase + Upstash Setup Guide

## Why This is Better

✅ **No local installation** - Everything in the cloud  
✅ **Free tier** - Both services have generous free plans  
✅ **Production-ready** - Same setup for dev and production  
✅ **Zero maintenance** - Managed services  
✅ **Easy to scale** - Upgrade when needed  

---

## 📋 Complete Setup Guide

### **Step 1: Set Up Supabase (PostgreSQL)**

#### 1.1 Create Account
1. Go to https://supabase.com/
2. Click **"Start your project"**
3. Sign up with GitHub or Google (free)

#### 1.2 Create Project
1. Click **"New Project"**
2. Fill in details:
   - **Name**: `weather-app`
   - **Database Password**: Create a strong password (SAVE THIS!)
   - **Region**: Choose closest to you (e.g., Asia Pacific)
   - **Pricing Plan**: Free
3. Click **"Create new project"**
4. Wait 2-3 minutes for setup ⏳

#### 1.3 Get Database Connection String
1. Go to **Settings** (⚙️ icon in sidebar)
2. Click **Database**
3. Scroll to **"Connection string"** section
4. Select **"URI"** tab
5. Copy the connection string (looks like):
   ```
   postgresql://postgres:#AgileProj@26@db.pkplfxqwdvojmuteubzf.supabase.co:5432/postgres
   ```
6. Replace `[YOUR-PASSWORD]` with your actual password
7. **Save this URL** - you'll need it!

#### 1.4 Create Database Tables
1. Go to **SQL Editor** (in sidebar)
2. Click **"New query"**
3. Copy the entire content from `backend/setup_supabase.sql`
4. Paste it into the SQL editor
5. Click **"Run"** (or press Ctrl+Enter)
6. You should see: "Database setup complete! ✅"

#### 1.5 Verify Tables Created
1. Go to **Table Editor** (in sidebar)
2. You should see 4 tables:
   - `locations`
   - `weather_history`
   - `user_favorites`
   - `weather_alerts`

---

### **Step 2: Set Up Upstash (Redis)**

#### 2.1 Create Account
1. Go to https://upstash.com/
2. Click **"Get Started"**
3. Sign up with GitHub or Google (free)

#### 2.2 Create Redis Database
1. Click **"Create Database"**
2. Fill in details:
   - **Name**: `weather-cache`
   - **Type**: Regional
   - **Region**: Choose closest to you
   - **Eviction**: No eviction
3. Click **"Create"**

#### 2.3 Get Redis URL
1. Click on your database name
2. Scroll to **"REST API"** section
3. Copy the **"UPSTASH_REDIS_REST_URL"** 
   OR
4. Scroll to **"Connect"** section
5. Copy the **Redis URL** (looks like):
   ```
   redis://default:AYeNAAIncDI5ZWQ2ZmQ1ODdjOGI0ZmIwYWUwYTU5MWMwODU3M2Y5YnAyMzQ3MDE@ruling-mite-34701.upstash.io:6379
   ```
6. **Save this URL** - you'll need it!

---

### **Step 3: Get OpenWeather API Key**

1. Go to https://openweathermap.org/api
2. Click **"Sign Up"** (if you don't have an account)
3. After login, go to **"API keys"** tab
4. Copy your API key (or create a new one)
5. **Note**: New keys may take 5-10 minutes to activate
6. **Save this key** - you'll need it!

---

### **Step 4: Configure Backend**

#### 4.1 Create .env File
1. Navigate to `backend` folder
2. Create a new file named `.env` (no extension)
3. Copy the content from `.env.supabase.example`
4. Fill in your actual values:

```env
# OpenWeather API Key
OPENWEATHER_API_KEY=your_actual_api_key_here

# Supabase PostgreSQL URL
DATABASE_URL=postgresql://postgres:your-password@db.xxxxx.supabase.co:5432/postgres

# Upstash Redis URL
REDIS_URL=redis://default:your-token@xxxxx.upstash.io:6379

# CORS Origins
CORS_ORIGINS=http://localhost:3000

# Security
SECRET_KEY=your-secret-key-change-in-production

# Cache
CACHE_EXPIRATION=300
```

#### 4.2 Install Dependencies
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### **Step 5: Start the Application**

#### 5.1 Start Backend
```powershell
# In backend directory with venv activated
python -m uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

#### 5.2 Test Backend
Open browser: http://localhost:8000

You should see:
```json
{
  "message": "Weather Forecasting API",
  "version": "1.0.0",
  "docs": "/docs",
  "status": "operational"
}
```

#### 5.3 Start Frontend
Open **new terminal**:
```powershell
cd frontend
npm run dev
```

#### 5.4 Open Application
Visit: http://localhost:3000

🎉 **You should see your weather app!**

---

## ✅ Verification Checklist

- [ ] Supabase project created
- [ ] Database tables created (4 tables)
- [ ] Upstash Redis database created
- [ ] OpenWeather API key obtained
- [ ] Backend `.env` file configured
- [ ] Backend dependencies installed
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can search for cities
- [ ] Can view weather data
- [ ] Can add favorites

---

## 🐛 Troubleshooting

### Backend won't start

**Error: "Could not connect to database"**
- ✅ Check DATABASE_URL is correct
- ✅ Verify Supabase project is running
- ✅ Check password has no special characters that need escaping
- ✅ Try pinging: `ping db.xxxxx.supabase.co`

**Error: "Redis connection failed"**
- ✅ Check REDIS_URL is correct
- ✅ Verify Upstash database is active
- ✅ Check you're using the correct URL format

**Error: "OpenWeather API key invalid"**
- ✅ Wait 10 minutes for key activation
- ✅ Check for extra spaces in .env file
- ✅ Verify key is correct

### Frontend issues

**"Cannot connect to backend"**
- ✅ Verify backend is running on port 8000
- ✅ Check CORS_ORIGINS in backend/.env includes `http://localhost:3000`

---

## 💡 Benefits of This Setup

### Free Tier Limits (More than enough!)

**Supabase Free Tier:**
- 500 MB database
- Unlimited API requests
- 50,000 monthly active users
- 2 GB bandwidth

**Upstash Free Tier:**
- 10,000 commands/day
- 256 MB storage
- Perfect for caching

### Production Ready

This same setup works for production:
- Just update CORS_ORIGINS with your production URL
- Both services auto-scale
- Built-in backups (Supabase)
- Global CDN (both services)

---

## 🎯 Next Steps

1. ✅ Complete the setup above
2. ✅ Test all features
3. ✅ Customize the design
4. 🚀 Deploy to Vercel (frontend)
5. 🚀 Deploy to Render/Railway (backend)

---

## 📚 Additional Resources

- **Supabase Docs**: https://supabase.com/docs
- **Upstash Docs**: https://docs.upstash.com/
- **OpenWeather API**: https://openweathermap.org/api

---

**You're all set! This is actually a BETTER setup than local PostgreSQL and Redis! 🎉**
