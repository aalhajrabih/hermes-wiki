---
title: الإعدادات والتكوين
description: دليل تكوين Hermes Agent — النماذج، المزودات، مفاتيح API، والأدوات
order: 2
category: البدء
---

# ⚙ الإعدادات والتكوين

دليل شامل لتكوين Hermes Agent بعد التثبيت.

## 🚀 الإعداد الأولي

شغّل معالج الإعداد التفاعلي:

```bash
hermes setup
```

سيطلب منك المعالج:

1. **المزود (Provider)**: OpenAI، Anthropic، OpenRouter، إلخ
2. **مفتاح API**: المفتاح الخاص بمزودك
3. **النموذج الافتراضي**: النموذج الذي سيُستخدم في المحادثات
4. **تفضيلات الأدوات**: الأدوات التي تريد تفعيلها

## 🤖 اختيار النموذج

استخدم أمر `hermes model` لتغيير النموذج في أي وقت:

```bash
hermes model
```

### المزودات المدعومة

| المزود | المميزات | التكلفة |
|--------|----------|---------|
| **Nous Portal** | نماذج Hermes الأصلية، بدون مفتاح API | مجاني |
| **OpenRouter** | 200+ نموذج من مزودين متعددين | ادفع حسب الاستخدام |
| **OpenAI** | GPT-4o، GPT-4.1، o3 | حسب الاستهلاك |
| **Anthropic** | Claude Sonnet 4، Opus 4 | حسب الاستهلاك |
| **DeepSeek** | DeepSeek-V3، R1 | اقتصادي |
| **Ollama (محلي)** | نماذج محلية على جهازك | مجاني |

!!! توصية
للمبتدئين: ابدأ بـ **Nous Portal** (مجاني، لا يحتاج مفتاح). للمستخدمين المتقدمين: **Anthropic Claude** يعطي أفضل أداء للمهام المعقدة.

## 📝 ملف الإعدادات

الإعدادات مخزنة في `~/.hermes/config.yaml`. يمكنك تعديلها يدوياً:

```yaml
# مثال: ~/.hermes/config.yaml
models:
  default: anthropic/claude-sonnet-4
  fallback: openrouter/anthropic/claude-sonnet-4

providers:
  anthropic:
    api_key: sk-ant-...
  openrouter:
    api_key: sk-or-...

tools:
  browser: true
  terminal: true
  image_gen: true
  tts: true

gateway:
  telegram:
    enabled: true
```

## 🔧 متغيرات البيئة

يمكن أيضاً استخدام متغيرات البيئة (`.env`):

```bash
# ~/.hermes/.env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-...
GROQ_API_KEY=gsk_...
TELEGRAM_BOT_TOKEN=123456:ABC...
```

## 🧩 تفعيل الأدوات

هيرميس يأتي مع مجموعة غنية من الأدوات:

| الأداة | الوصف |
|--------|-------|
| `terminal` | تنفيذ أوامر shell |
| `file` | قراءة وكتابة الملفات |
| `web` | بحث وب وتصفح |
| `browser` | تصفح مواقع بتقنية Playwright |
| `image_gen` | توليد صور بالذكاء الاصطناعي |
| `tts` | تحويل النص إلى كلام |
| `vision` | تحليل الصور |
| `cronjob` | جدولة المهام المتكررة |
| `memory` | ذاكرة طويلة المدى |

لتفعيل/تعطيل الأدوات:

```bash
hermes tools enable browser
hermes tools disable image_gen
```

## ⏭ التالي

بعد الإعداد: [دليل المهارات](skills-guide.html)
