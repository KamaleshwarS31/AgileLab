# ⚡ Quick Setup - Supabase Edition

## 🎯 What You Need (All Free!)

1. **Supabase Account** → PostgreSQL Database
2. **Upstash Account** → Redis Cache  
3. **OpenWeather API Key** → Weather Data

---

## 📝 Quick Steps

### 1️⃣ Supabase (5 minutes)
```
1. Go to https://supabase.com/
2. Sign up → Create project
3. Settings → Database → Copy URI
4. SQL Editor → Run setup_supabase.sql
```

### 2️⃣ Upstash (3 minutes)
```
1. Go to https://upstash.com/
2. Sign up → Create database
3. Copy Redis URL
```

### 3️⃣ OpenWeather (2 minutes)
```
1. Go to https://openweathermap.org/api
2. Sign up → Get API key
3. Wait 10 minutes for activation
```

### 4️⃣ Configure (2 minutes)
```powershell
# Edit backend/.env
OPENWEATHER_API_KEY=your_key
DATABASE_URL=postgresql://postgres:pass@db.xxx.supabase.co:5432/postgres
REDIS_URL=redis://default:token@xxx.upstash.io:6379
CORS_ORIGINS=http://localhost:3000
```

### 5️⃣ Run (1 minute)
```powershell
# Terminal 1 - Backend
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 6️⃣ Open
```
http://localhost:3000
```

---

## ✅ That's It!

**Total Time**: ~15 minutes  
**Cost**: $0 (all free tiers)  
**Installation**: Zero local setup needed!

---

## 📖 Full Guide

See **SUPABASE_SETUP.md** for detailed instructions.

---

**This is actually BETTER than local setup! 🚀**
