---
title: استكشاف الأخطاء والمشاكل المعروفة
description: حلول للمشاكل الشائعة في Hermes Agent — التثبيت، التشغيل، النماذج، والبوابات
order: 8
category: دعم
---

# 🐛 استكشاف الأخطاء

حلول للمشاكل الشائعة التي قد تواجهها مع Hermes Agent على أندرويد.

## 🔧 مشاكل التثبيت

??? خطأ ربط ffmpeg

```
CANNOT LINK EXECUTABLE "ffmpeg": cannot locate symbol "x265_api_get_215"
```

**الإصلاح:**

```bash
pkg upgrade
dpkg --remove --force-depends ffmpeg
pkg install ffmpeg
```

??? خطأ: تجميع `pydantic-core` فشل

```
error: can't find Rust compiler
```

**الإصلاح:** تأكد من تثبيت Rust:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

??? التثبيت يستغرق وقتاً طويلاً

هذا طبيعي! التثبيت الأول يستغرق 10-30 دقيقة لأن حزماً مثل `pydantic-core` و `cryptography` تُجمّع من الشيفرات المصدرية على معالج ARM.

**نصائح للتسريع:**

- أغلق التطبيقات الأخرى لتحرير RAM
- شغّل `termux-wake-lock` لمنع أندرويد من تعليق العملية
- لا تغلق الشاشة أثناء التثبيت
- تأكد من وجود 4GB RAM على الأقل

??? عمليات Termux تتوقف في الخلفية

أندرويد يعلّق عمليات Termux الخلفية. الحلول:

```bash
# منع التعليق
termux-wake-lock

# أو أبقِ Termux مرئياً في وضع تقسيم الشاشة
```

## 🤖 مشاكل النماذج

??? خطأ: `401 Unauthorized`

```
Error: 401 Unauthorized - Invalid API key
```

**الحل:** تأكد من صحة مفتاح API:

```bash
hermes config show
hermes config set providers.anthropic.api_key "sk-ant-..."
```

??? خطأ: `Rate limit exceeded`

```
Error: 429 Too Many Requests
```

**الحل:**

- انتظر دقيقة وأعد المحاولة
- استخدم مزوداً آخر كـ fallback:
  ```bash
  hermes config set models.fallback "openrouter/anthropic/claude-sonnet-4"
  ```

??? النموذج بطيء على الأندرويد

- استخدم نماذج أخف: `openrouter/mistral/mistral-small`
- استخدم API خارجي بدل Ollama المحلي
- جرّب Nous Portal (مجاني وسريع)

## 📡 مشاكل البوابات

??? تيليغرام: البوت لا يستجيب

```bash
# تحقق من حالة البوابة
hermes gateway status

# تحقق من السجلات
hermes gateway logs

# أعد تشغيل البوابة
hermes gateway restart
```

??? تيليغرام: خطأ `409 Conflict`

```
Error: 409 Conflict - Multiple instances
```

**الحل:** هناك نسخة أخرى من البوت تعمل. أوقفها أولاً:

```bash
pkill -f "hermes gateway"
hermes gateway run
```

## 💾 مشاكل الذاكرة والتخزين

??? خطأ: `No space left on device`

```bash
# تنظيف الملفات المؤقتة
hermes cache clear

# حذف البيئات الافتراضية القديمة
rm -rf ~/.hermes/hermes-agent/venv-old
```

## 🐍 مشاكل Python

??? `ModuleNotFoundError: No module named 'psutil'`

خاص بأندرويد Termux:

```bash
pkg install python-psutil
VENV_SITE=$(python -c "import site; print(site.getsitepackages()[0])")
echo "/data/data/com.termux/files/usr/lib/python3.13/site-packages" > "$VENV_SITE/system-site.pth"
```

??? خطأ: `GLIBC not found`

بعض الحزم تحتاج glibc غير المتوفر في Termux (يستخدم musl):

```bash
# استخدم constraints-termux.txt
pip install -c constraints-termux.txt
```

## 🔍 أدوات التشخيص

```bash
# فحص شامل
hermes doctor

# عرض الإعدادات الحالية
hermes config show

# عرض السجلات
hermes logs --tail 50

# اختبار الاتصال بالمزود
hermes test-connection

# فحص المهارات
hermes skills validate
```

## 📞 الحصول على المساعدة

- [توثيق Hermes Agent الرسمي](https://hermes-agent.nousresearch.com/docs/)
- [مستودع Hermes Agent على GitHub](https://github.com/NousResearch/hermes-agent)
- [موقع Nous Research](https://nousresearch.com)
- [موقع Termux الرسمي](https://termux.dev/)

:::success نصيحة
قبل طلب المساعدة، شغّل `hermes doctor` وأرفق المخرجات مع تقرير المشكلة.
:::
