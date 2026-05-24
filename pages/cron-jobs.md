---
title: المهام المجدولة (Cron)
description: أتمتة المهام المتكررة في Hermes Agent — مراقبة، تقارير، وتنبيهات دورية
order: 5
category: متقدم
---

# ⏰ المهام المجدولة (Cron Jobs)

هيرميس يدعم جدولة مهام متكررة تعمل تلقائياً — مثالية للمراقبة والتقارير والأتمتة.

## 🕐 الجدولة الأساسية

### إنشاء مهمة مجدولة

```bash
hermes cron create "تحقق من أسعار العملات كل ساعة" --schedule "0 * * * *"
```

### صيغ الجدولة المدعومة

| الصيغة | مثال | الوصف |
|--------|------|-------|
| **Cron expression** | `0 9 * * *` | الساعة 9 صباحاً يومياً |
| **اختصار** | `30m` | كل 30 دقيقة |
| **اختصار** | `every 2h` | كل ساعتين |
| **مرة واحدة** | `once` | تشغيل مرة واحدة |
| **ISO timestamp** | `2026-06-01T09:00:00` | في وقت محدد |

### أمثلة cron expressions

```
0 9 * * *       # 9:00 صباحاً يومياً
0 */6 * * *     # كل 6 ساعات
30 8 * * 1-5    # 8:30 صباحاً، الاثنين للجمعة
0 0 1 * *       # منتصف ليل أول يوم من كل شهر
```

## 📋 إدارة المهام

```bash
# عرض جميع المهام
hermes cron list

# تفاصيل مهمة محددة
hermes cron show <job_id>

# إيقاف مؤقت
hermes cron pause <job_id>

# استئناف
hermes cron resume <job_id>

# تشغيل يدوي الآن
hermes cron run <job_id>

# حذف مهمة
hermes cron delete <job_id>
```

## 🔗 سلسلة المهام (Chaining)

يمكن ربط المهام بحيث تعتمد مخرجات مهمة على أخرى:

```bash
# المهمة A: جمع البيانات
hermes cron create "جمع بيانات السوق" --schedule "*/15 * * * *" --name "market-collector"

# المهمة B: تحليل البيانات (تستخدم مخرجات A)
hermes cron create "تحليل اتجاهات السوق" --schedule "*/30 * * * *" --context-from "market-collector"
```

## 📨 توجيه النتائج (Delivery)

تحديد أين تُرسل نتائج المهمة:

```bash
# إرسال للجلسة الحالية + تيليغرام
hermes cron create "تقرير يومي" --schedule "0 9 * * *" --deliver "origin,telegram"

# إرسال لقناة تيليغرام محددة
hermes cron create "تنبيهات" --schedule "*/5 * * * *" --deliver "telegram:-1001234567890"
```

## 🛠 مهارات Cron

يمكن ربط المهام بمهارات محددة:

```bash
hermes cron create "مراقبة العملات" \
  --schedule "*/15 * * * *" \
  --skills "crypto-monitoring" \
  --deliver "telegram"
```

## 📊 أمثلة عملية

### 1. مراقب أسعار العملات الرقمية

```bash
hermes cron create "مراقبة BTC و ETH" \
  --schedule "*/15 * * * *" \
  --prompt "تحقق من أسعار BTC و ETH الحالية. إذا تغير السعر أكثر من 2%، أرسل تنبيه." \
  --deliver "telegram"
```

### 2. تقرير يومي

```bash
hermes cron create "تقرير الصباح" \
  --schedule "0 8 * * *" \
  --prompt "قدم تقريراً صباحياً: حالة النظام، الأخبار المهمة، مهام اليوم." \
  --deliver "origin,telegram"
```

### 3. نسخ احتياطي

```bash
hermes cron create "نسخ احتياطي أسبوعي" \
  --schedule "0 2 * * 0" \
  --prompt "قم بعمل نسخة احتياطية لملفات الإعدادات والمهارات في ~/.hermes/backups/" \
  --deliver "local"
```

### 4. مراقب استخدام الموارد

```bash
hermes cron create "مراقب النظام" \
  --schedule "*/10 * * * *" \
  --script "~/scripts/check_resources.sh" \
  --no_agent true \
  --deliver "telegram"
```

حيث `check_resources.sh`:

```bash
#!/bin/bash
CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
MEM=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if (( $(echo "$CPU > 80" | bc -l) )) || [ "$MEM" -gt 80 ]; then
    echo "⚠️ تحذير: CPU ${CPU}% | RAM ${MEM}%"
fi
```

:::warn
**انتبه**: نافذة المهام لمرة واحدة (one-shot) هي 120 ثانية فقط. استخدم `interval` مع `repeat=1` أو `cron expression` للمهام الطويلة.
:::

:::info
**تلميح**: استخدم `--no_agent true` مع `--script` لتشغيل سكريبتات Bash/Python مباشرة بدون استهلاك رصيد LLM. مثالي للمراقبة الخفيفة.
:::

## ⏭ التالي

- [واجهة الويب](webui.html) — إدارة مرئية
- [استكشاف الأخطاء](troubleshooting.html) — حل المشاكل
