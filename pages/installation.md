---
title: ⚕ هيرميس على أندرويد — دليل التثبيت الكامل
description: شغّل وكيل هيرميس الذكي على هاتفك الأندرويد عبر Termux — تثبيت، متطلبات، وإعداد
order: 1
category: البدء
---

# ⚕ هيرميس على أندرويد

شغّل وكيل هيرميس الذكي — الوكيل ذاتي التطوير من Nous Research — مباشرةً على هاتفك الأندرويد عبر Termux.

## 📱 ما هذا المشروع؟

هذا المشروع يوفر كل ما تحتاجه لتثبيت وتشغيل **وكيل هيرميس** على هاتف أندرويد باستخدام Termux. يحتوي على سكريبت تثبيت مخصص، تصحيحات خاصة بأندرويد، وأدلة خطوة بخطوة بالعربية والإنجليزية.

وكيل هيرميس هو وكيل ذكاء اصطناعي ذاتي التطوير:

- يتعلم من التجارب وينشئ مهاراته الخاصة
- يعمل مع أي نموذج لغوي (OpenAI، Anthropic، OpenRouter، NVIDIA NIM، Ollama محلي...)
- يتصل بتيليغرام، ديسكورد، سلاك، واتساب، سيغنال
- يشغّل أتمتة مجدولة (cron)
- يمتلك ذاكرة طويلة المدى واستدعاء عبر الجلسات

!!! الفكرة الجوهرية
والآن يعمل على هاتفك. **بدون حاجة للابتوب أو VPS.**

## ⚡ تثبيت سريع

تأكد من تثبيت Termux من F-Droid، ثم نفّذ:

```bash
curl -fsSL https://raw.githubusercontent.com/leecoin06-commits/hermes-agent-android/main/install-android.sh | bash
```

هذا الأمر الواحد سيقوم بـ:

1. تثبيت جميع الحزم النظامية المطلوبة
2. استنساخ مستودع Hermes Agent
3. إنشاء بيئة Python افتراضية
4. تطبيق التصحيحات الخاصة بأندرويد
5. تجميع وتثبيت جميع الاعتماديات
6. جعل أمر `hermes` متاحاً على مسار Termux

:::warn وقت التثبيت
**التثبيت يستغرق 10–30 دقيقة** لأن بعض الحزم الأساسية (`pydantic-core`، `cryptography`، `uvloop`) تُجمّع من شيفرات Rust/C المصدرية على معالج ARM.
:::

## 📋 المتطلبات

| المتطلب | ملاحظات |
|---------|---------|
| **Termux** | ثبته من F-Droid (وليس Google Play) |
| **أندرويد 7+** | يعمل على أندرويد 7 أو أحدث |
| **~3 جيجابايت مساحة** | للمستودع + البيئة الافتراضية + الحزم |
| **اتصال إنترنت** | لاستنساخ وتحميل الحزم |
| **4 جيجابايت RAM+** | مُوصى به لتجميع الحزم بسلاسة |

## 🛠 التثبيت اليدوي (خطوة بخطوة)

إذا كنت تفضل التحكم الكامل في عملية التثبيت:

### 1. تثبيت Termux والحزم النظامية

```bash
pkg update
pkg install -y git python clang rust make pkg-config libffi openssl nodejs ripgrep ca-certificates curl
pkg install -y python-psutil
```

### 2. استنساخ Hermes Agent

```bash
mkdir -p ~/.hermes
git clone --recurse-submodules https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent
```

### 3. إنشاء البيئة الافتراضية

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install maturin
```

### 4. ربط psutil النظامي

```bash
VENV_SITE=$(python -c "import site; print(site.getsitepackages()[0])")
echo "/data/data/com.termux/files/usr/lib/python3.13/site-packages" > "$VENV_SITE/system-site.pth"
```

### 5. تعديل pyproject.toml

```bash
sed -i 's/"psutil>=5.9.0,<8",/# "psutil>=5.9.0,<8", # Termux/' pyproject.toml
```

### 6. تثبيت Hermes

```bash
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
pip install -e '.[termux-all]' -c constraints-termux.txt
```

### 7. جعل `hermes` متاحاً في المسار

```bash
ln -sf ~/.hermes/hermes-agent/venv/bin/hermes $PREFIX/bin/hermes
```

### 8. التحقق

```bash
hermes version
hermes doctor
```

:::success
إذا ظهرت أرقام الإصدار بدون أخطاء — التثبيت ناجح! 🎉
:::

## 🚀 بعد التثبيت — ماذا بعد؟

بعد اكتمال التثبيت، انتقل إلى:

| الخطوة | الأمر | الوصف |
|---------|-------|--------|
| **الإعداد الأولي** | `hermes setup` | معالج تفاعلي لضبط المزود والمفاتيح |
| **اختيار النموذج** | `hermes model` | اختر النموذج المناسب (Nous Portal مجاني) |
| **بدء المحادثة** | `hermes` | واجهة CLI متكاملة |
| **بوابة تيليغرام** | `hermes gateway setup` | تواصل مع هيرميس عبر تيليغرام |

:::info
تفاصيل كل خطوة في صفحة [ما بعد التثبيت](post-install.html).
:::

## 🐛 المشاكل المعروفة

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

??? وقت التجميع الطويل

التثبيت الأول يستغرق 10–30 دقيقة لأن حزماً مثل `pydantic-core` و `cryptography` تُجمّع من الشيفرات المصدرية. التشغيلات اللاحقة أسرع بكثير.

??? عمليات Termux الخلفية

قد يعلّق أندرويد عمليات Termux الخلفية. استخدم `termux-wake-lock` أو أبقِ Termux في وضع تقسيم الشاشة.

??? أدوات المتصفح وتحويل الصوت

**Playwright:** تجريبية على أندرويد.

**تحويل الصوت:** استخدم Groq Whisper (`GROQ_API_KEY`) أو OpenAI Whisper (`VOICE_TOOLS_OPENAI_KEY`).

## ⏭ التالي

- [ما بعد التثبيت — الإعداد والتكوين](post-install.html)
- [اختيار النموذج المناسب](configuration.html)
- [استكشاف الأخطاء](troubleshooting.html)
