---
title: دليل المهارات
description: إنشاء وإدارة المهارات المخصصة في Hermes Agent باستخدام Python
order: 3
category: متقدم
---

# 🧩 دليل المهارات

المهارات هي آلية هيرميس **لتوسيع قدراته** وتعلّم مهام جديدة. كل مهارة هي وحدة Python مستقلة تُضاف للنظام.

## 📖 ما هي المهارة؟

المهارة في هيرميس هي:

- **كود Python** ينفذ مهمة محددة
- **موثقة ذاتياً** — هيرميس يقرأ الوصف ويعرف متى يستخدمها
- **قابلة للمشاركة** — يمكن تثبيت مهارات من المجتمع
- **ذاتية التحميل** — بمجرد وضعها في المجلد الصحيح

## 🛠 إنشاء مهارة جديدة

أبسط شكل للمهارة:

```python
# ~/.hermes/skills/my_skill.py
from hermes.skill import skill

@skill(
    name="weather_lookup",
    description="يحصل على حالة الطقس الحالية لمدينة محددة"
)
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # الكود الخاص بك هنا
    return f"حالة الطقس في {city}: مشمس، 25°C"
```

### بنية المهارة المتقدمة

```python
from hermes.skill import skill, SkillContext

@skill(
    name="code_reviewer",
    description="يراجع كود Python ويقدم اقتراحات للتحسين",
    triggers=["راجع الكود", "code review", "فحص الكود"]
)
class CodeReviewer:
    """مراجع كود Python احترافي."""

    def __init__(self, ctx: SkillContext):
        self.ctx = ctx
        self.model = ctx.model  # النموذج النشط

    async def execute(self, code: str, language: str = "python") -> dict:
        """
        يراجع الكود ويعيد تقريراً.

        المعاملات:
            code: الكود المطلوب مراجعته
            language: لغة البرمجة

        المخرجات:
            dict يحتوي على issues و suggestions و score
        """
        # منطق المراجعة هنا
        return {
            "issues": [...],
            "suggestions": [...],
            "score": 8.5
        }
```

## 📁 هيكل ملفات المهارة

المهارات المعقدة يمكن تنظيمها في مجلد:

```
~/.hermes/skills/my-advanced-skill/
├── SKILL.md           # وثائق المهارة (إجباري)
├── __init__.py        # كود المهارة
├── references/        # ملفات مرجعية
│   └── api-docs.md
├── templates/         # قوالب
│   └── report.md
└── scripts/           # سكريبتات مساعدة
    └── validate.py
```

محتوى `SKILL.md`:

```markdown
---
name: my-advanced-skill
description: وصف موجز للمهارة
version: 1.0.0
author: اسمك
tags: [تحليل, تقارير]
---

# My Advanced Skill

وصف تفصيلي للمهارة...

## الاستخدام

...

## المعاملات

...
```

## 🔌 تثبيت مهارات المجتمع

هيرميس يدعم Registry عام للمهارات:

```bash
# البحث عن مهارات
hermes skills search "crypto trading"

# تثبيت مهارة
hermes skills install hermes-crypto-evaluator

# تحديث المهارات المثبتة
hermes skills update

# عرض المهارات المثبتة
hermes skills list
```

## ⚡ مهارات cron (المهام المجدولة)

المهارات يمكن أن تعمل كمهام Cron تلقائية:

```yaml
# مثال: مهارة تعمل كل ساعة
---
name: crypto-monitor
schedule: "0 * * * *"
enabled: true
---
```

## 🎯 أفضل الممارسات

:::success
**نصائح لمهارات فعالة**
- اكتب أوصافاً دقيقة — هيرميس يعتمد عليها لاختيار المهارة المناسبة
- استخدم type hints في Python
- عالج الأخطاء gracefully
- وثّق المخرجات بوضوح
:::

:::warn
**تجنب**
- المهارات التي تعدّل إعدادات النظام بدون تأكيد
- الاعتماد على مسارات مطلقة (استخدم مسارات نسبية)
- استدعاءات شبكة غير محدودة الوقت
:::

## ⏭ التالي

- [دليل البوابات](gateway.html) — ربط هيرميس مع تطبيقات المراسلة
- [المهام المجدولة](cron-jobs.html) — أتمتة متقدمة
