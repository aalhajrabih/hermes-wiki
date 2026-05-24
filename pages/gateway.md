---
title: بوابات المراسلة والتعايش مع OpenClaw
description: ربط Hermes Agent مع تيليغرام، ديسكورد، واتساب، سلاك، والتعايش مع OpenClaw
order: 5
category: متقدم
---

# 📡 بوابات المراسلة

بوابات هيرميس تسمح لك بالتفاعل مع الوكيل عبر تطبيقات المراسلة المفضلة لديك.

## 📱 البوابات المدعومة

| البوابة | الحالة | المميزات |
|---------|--------|----------|
| **تيليغرام** | ✅ مستقر | بوت كامل، دعم media، أزرار تفاعلية |
| **ديسكورد** | ✅ مستقر | خوادم وقنوات |
| **سلاك** | ✅ مستقر | قنوات ورسائل مباشرة |
| **واتساب** | ⚠️ تجريبي | عبر Baileys |
| **سيغنال** | ⚠️ تجريبي | عبر signal-cli |
| **ماتريكس** | ✅ مستقر | غرف ومحادثات مباشرة |

## 🤖 إعداد بوت تيليغرام

### 1. إنشاء البوت

تحدث مع [@BotFather](https://t.me/BotFather):

```
/newbot
HermesAssistant
hermes_yourname_bot
```

ستحصل على **توكن البوت** (مثل `123456789:ABCdef...`).

### 2. تكوين البوابة

```bash
hermes gateway setup
```

اختر "Telegram" وأدخل التوكن.

أو يدوياً في `config.yaml`:

```yaml
gateway:
  telegram:
    enabled: true
    bot_token: "123456789:ABCdef..."
    allowed_users: []
```

### 3. تشغيل البوابة

```bash
hermes gateway run
```

:::success
**البوت جاهز!** ابحث عن بوتك على تيليغرام وابدأ المحادثة.
:::

## 🔄 التعايش مع OpenClaw ووكلاء آخرين

إذا كنت تشغّل **OpenClaw** أو أي وكيل آخر على نفس التطبيق:

| الوكيل | البوت | الطريقة |
|--------|-------|---------|
| **Hermes** | بوت #1 | `hermes gateway setup` |
| **OpenClaw** | بوت #2 | توكن مختلف في إعدادات OpenClaw |

باستخدام توكنات منفصلة، يعمل كلا الوكيلين معاً دون تعارض.

:::success بدون تعارض
مع توكنات منفصلة، يعمل كلا الوكيلين معاً دون أي مشاكل.
:::

## 💬 إعداد ديسكورد

```yaml
gateway:
  discord:
    enabled: true
    bot_token: "your_discord_bot_token"
    channels:
      - "general"
      - "hermes-chat"
```

1. اذهب إلى [Discord Developer Portal](https://discord.com/developers/applications)
2. أنشئ تطبيقاً جديداً
3. Bot → Add Bot → انسخ التوكن
4. ادعُ البوت إلى خادمك

## 🛡 الأمان والصلاحيات

```yaml
gateway:
  security:
    allowed_users:
      telegram: [123456789, 987654321]
      discord: ["user_id_1"]
    require_auth: true
```

:::warn تنبيه أمني
لا تشارك توكنات البوتات أبداً. إذا تم تسريب توكن، استبدله فوراً من BotFather أو Discord Developer Portal.
:::

## ⏭ التالي

- [المهام المجدولة](cron-jobs.html) — أتمتة عبر الزمن
- [واجهة الويب](webui.html) — تحكم مرئي
