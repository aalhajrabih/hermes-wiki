# 📚 موسوعة هيرميس — Hermes Wiki

<p align="center"><img src="logo.png" alt="Hermes Logo" height="140"></p>

> دليل شامل لوكلاء Hermes Agent — تثبيت، تكوين، مهارات، وأتمتة
>
> Comprehensive guide for Hermes Agent — installation, configuration, skills, and automation

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-All-green.svg)](https://aalhajrabih.github.io/hermes-wiki/)
[![Pages](https://img.shields.io/badge/Pages-9-orange.svg)](#-المحتويات)

---

## 🌐 الموقع المباشر

**[aalhajrabih.github.io/hermes-wiki](https://aalhajrabih.github.io/hermes-wiki/)**

---

## ✨ المميزات

- **ملف HTML واحد** — جميع الصفحات مضمّنة، بدون اعتماديات خارجية
- **يدعم العربية كاملاً** — RTL + خط Noto Sans Arabic
- **متجاوب مع الموبايل** — تصميم متكيف مع جميع أحجام الشاشات
- **أزرار نسخ** — لكل الأكواد والأوامر بنقرة واحدة
- **وضع ليلي** — 🌙 تبديل بين الوضعين الفاتح والداكن
- **قائمة جانبية** — تصنيف آلي للصفحات حسب القسم
- **يعمل بدون إنترنت** — بعد تحميل المرة الأولى، لا حاجة للاتصال
- **GitHub Pages جاهز** — انشره مباشرة بدون أي إعدادات إضافية

## 📖 المحتويات

| الصفحة | الوصف |
|---------|--------|
| 🏠 [الرئيسية](https://aalhajrabih.github.io/hermes-wiki/#index) | نظرة عامة على Hermes Agent |
| ⚡ [التثبيت](https://aalhajrabih.github.io/hermes-wiki/#installation) | تثبيت Hermes على أندرويد، Linux، VPS |
| 🚀 [بعد التثبيت](https://aalhajrabih.github.io/hermes-wiki/#post-install) | الإعداد الأولي، اختيار النموذج، تيليغرام |
| ⚙ [الإعدادات](https://aalhajrabih.github.io/hermes-wiki/#configuration) | تكوين النماذج والمزودات والأدوات |
| 🧩 [المهارات](https://aalhajrabih.github.io/hermes-wiki/#skills-guide) | إنشاء وإدارة المهارات المخصصة |
| 📡 [البوابات](https://aalhajrabih.github.io/hermes-wiki/#gateway) | ربط مع تيليغرام، ديسكورد، واتساب |
| ⏰ [المهام](https://aalhajrabih.github.io/hermes-wiki/#cron-jobs) | أتمتة المهام المجدولة والمراقبة |
| 🖥 [واجهة الويب](https://aalhajrabih.github.io/hermes-wiki/#webui) | Hermes WebUI المعرّبة |
| 🐛 [استكشاف الأخطاء](https://aalhajrabih.github.io/hermes-wiki/#troubleshooting) | حلول للمشاكل الشائعة |

## 🚀 الاستخدام

### مباشرة من المتصفح

افتح `index.html` مباشرة — لا حاجة لأي سيرفر أو تثبيت.

### GitHub Pages

1. ارفع المستودع على GitHub
2. فعّل Pages من Settings → Pages → main branch
3. الموقع جاهز على `username.github.io/hermes-wiki/`

### خادم محلي (اختياري)

```bash
python -m http.server 8080
# افتح http://localhost:8080
```

## 🛠 التعديل والتطوير

### إضافة صفحة جديدة

1. أنشئ ملف Markdown في `pages/`:

```markdown
---
title: عنوان الصفحة
description: وصف مختصر
category: البدء
---

# المحتوى هنا
```

2. شغّل البناء:

```bash
python build.py
```

### هيكل المشروع

```
hermes-wiki/
├── index.html          ← الموقع الكامل (ملف واحد)
├── build.py            ← سكريبت البناء من MD → HTML
├── pages/              ← ملفات Markdown المصدرية
│   ├── index.md
│   ├── installation.md
│   └── ...
└── README.md
```

### صيغ Markdown المدعومة

بالإضافة إلى Markdown القياسي، يدعم الباني:

```markdown
:::info
مربع معلومات
:::

:::warn تنبيه
مربع تحذير بعنوان مخصص
:::

:::success
مربع نجاح
:::

:::danger
مربع خطر
:::

!!! عنوان مميز
كتلة بارزة
!!!

??? عنوان قابل للطي
محتوى مخفي يظهر عند النقر
???
```

## 📜 الرخصة

Apache 2.0 — انظر [LICENSE](LICENSE)

---

<p align="center">صُنع بمساعدة Hermes Agent 🤖</p>
