---
title: واجهة الويب المعرّبة (Hermes WebUI)
description: تثبيت وتشغيل واجهة Hermes WebUI العربية — تحكم مرئي كامل بالوكيل مع دعم RTL
order: 6
category: متقدم
---

# 🖥 واجهة هيرميس ويب المعرّبة

بعد تثبيت Hermes Agent، ثبّت واجهة الويب للتحكم به من المتصفح بواجهة عربية كاملة.

## 📥 التثبيت

المستودع العربي الرسمي مع دعم RTL كامل:

```bash
# استنساخ واجهة الويب المعرّبة
git clone https://github.com/aalhajrabih/hermes-webui.git ~/hermes-webui
cd ~/hermes-webui

# تثبيت الاعتماديات
npm install

# بناء التطبيق
npm run build
```

:::info النسخة المعرّبة
هذه النسخة معدّلة خصيصاً للغة العربية مع:
- اتجاه RTL كامل
- ترجمة عربية للواجهة
- دعم الخطوط العربية (Noto Sans Arabic)
- تخطيط متجاوب مع الهواتف
:::

## 🚀 التشغيل

### تشغيل تطويري (للاستخدام الشخصي)

```bash
cd ~/hermes-webui
npm run dev
```

الواجهة على: `http://localhost:3000`

### تشغيل للوصول من الهاتف أو الشبكة

```bash
cd ~/hermes-webui
HERMES_WEBUI_HOST=0.0.0.0 npm run dev
```

ثم افتح من هاتفك: `http://192.168.x.x:3000`

### تشغيل في الخلفية (Termux / Android)

```bash
cd ~/hermes-webui
nohup npm run dev > /tmp/hermes-webui.log 2>&1 &
```

للوصول من المتصفح على نفس الهاتف:

```bash
HERMES_WEBUI_HOST=0.0.0.0 nohup npm run dev > /tmp/hermes-webui.log 2>&1 &
```

## 🔗 الربط مع Hermes Agent

واجهة الويب تحتاج أن يكون Hermes Agent شغّال:

```bash
# الطرفية 1: شغّل Hermes
hermes serve

# الطرفية 2: شغّل الواجهة
cd ~/hermes-webui && npm run dev
```

أو باستخدام `nohup` لتشغيل الاثنين في الخلفية:

```bash
# تشغيل Hermes
nohup hermes serve > /tmp/hermes.log 2>&1 &

# تشغيل الواجهة
cd ~/hermes-webui
HERMES_WEBUI_HOST=0.0.0.0 nohup npm run dev > /tmp/hermes-webui.log 2>&1 &
```

## ☁️ تشغيل على VPS

للتثبيت على خادم Ubuntu/Debian:

```bash
# تثبيت Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# استنساخ وتثبيت
git clone https://github.com/aalhajrabih/hermes-webui.git /opt/hermes-webui
cd /opt/hermes-webui
npm install
npm run build
```

### كخدمة systemd

```ini
[Unit]
Description=Hermes WebUI
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/hermes-webui
Environment=HERMES_WEBUI_HOST=0.0.0.0
Environment=HERMES_WEBUI_PORT=3000
ExecStart=/usr/bin/npm run start
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now hermes-webui
```

## 🎨 المكونات

| العنصر | الوصف |
|--------|-------|
| **المحادثة** | واجهة محادثة مع Markdown كامل |
| **مدير الملفات** | تصفح وتحرير workspace |
| **المهام** | إدارة المهام المجدولة |
| **الإعدادات** | تغيير النموذج والمزود |
| **الذاكرة** | ذاكرة طويلة المدى |
| **المهارات** | تصفح وتثبيت المهارات |

## 🌐 اللغة العربية و RTL

الواجهة معرّبة بالكامل:

- القوائم والأزرار بالعربية
- اتجاه RTL تلقائي
- خط Noto Sans Arabic مدمج
- دعم المحادثات بالعربية

لتغيير اللغة: `الإعدادات → المظهر → اللغة → العربية`

## 🔧 إعدادات متقدمة

### Reverse Proxy مع Nginx

```nginx
server {
    listen 443 ssl;
    server_name hermes.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### تعيين كلمة مرور

```bash
hermes webui set-password
```

## 📱 الوصول من الهاتف

```bash
cd ~/hermes-webui
HERMES_WEBUI_HOST=0.0.0.0 npm run dev
```

ثم افتح `http://IP-الهاتف:3000` من المتصفح.

## ⏭ التالي

- [استكشاف الأخطاء](troubleshooting.html)
- [المهام المجدولة](cron-jobs.html)
