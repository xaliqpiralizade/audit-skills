# Hesabat şablonu

Hesabatı bu struktura uyğun yaz. Tapıntıların formatını dəyişmə: `scripts/export_xlsx.py` tapıntıları `### <KOD>-<nömrə> · <başlıq>` başlığından və `- **Sahə adı:** dəyər` sətirlərindən oxuyur.

````markdown
# Audit hesabatı: <Sahə> — <Layihənin adı>

**Tarix:** YYYY-MM-DD
**Yoxlanılan layihə:** `<yol>` (commit: `<qısa hash, varsa>`)
**Yoxlama siyahısı:** `references/hr.md` (yaxud: ümumi metodologiya, bax: aşağıdakı qeyd)
**Auditor:** Claude (domain-auditor plugin)

> Qeyd: Bu sənəd daxili yoxlamanın nəticəsidir və rəsmi audit rəyi və ya hüquqi rəy deyil.

## 1. İcmal

**Ümumi qiymət:** 3/5. Əsas proseslər mövcuddur, amma məzuniyyət hesablamasında qanunvericiliyə zidd səhvlər və fərdi məlumatlara geniş giriş var.

| Risk dərəcəsi | Say |
|---|---|
| Kritik | 0 |
| Yüksək | 0 |
| Orta | 0 |
| Aşağı | 0 |
| **Cəmi** | 0 |

**Ən vacib 3 tövsiyə:**
1. ...
2. ...
3. ...

### Qiymət şkalası
- 5: sahədə istifadəyə hazırdır, yalnız aşağı riskli qeydlər var
- 4: kiçik düzəlişlərdən sonra hazırdır (Yüksək yoxdur, Kritik yoxdur)
- 3: istifadə mümkündür, amma Yüksək riskli tapıntılar həll edilməlidir
- 2: Kritik tapıntılar var, real istifadəyə hazır deyil
- 1: əsas funksiyalar yoxdur və ya sistem işləmir

## 2. Əhatə dairəsi və metodologiya

- Yoxlanılan hissələr: ...
- Proqram işə salındımı: Bəli / Xeyr (səbəb)
- Baxılan ekranlar: ...
- Xaric edilənlər: ...

## 3. Tapıntılar

### HR-001 · Məzuniyyət müddəti 21 gündən az hesablanır
- **Bölmə:** Əmək Məcəlləsinə uyğunluq
- **Risk dərəcəsi:** Kritik
- **Təsvir:** ...
- **Sübut:** `src/leave/calc.ts:42` — `const BASE_DAYS = 18;`
- **Niyə problemdir:** ƏM 114.2 əsas məzuniyyətin 21 təqvim günündən az olmamasını tələb edir ([e-qanun.az/framework/46943](https://e-qanun.az/framework/46943), yoxlama tarixi: YYYY-MM-DD).
- **Tövsiyə:** ...

(tapıntılar Kritik → Yüksək → Orta → Aşağı sırası ilə)

## 4. Uyğun bəndlər

- Əmək müqaviləsi formasında ƏM 43.2-nin bütün məcburi sahələri var (`src/forms/contract.tsx`).
- ...

## 5. Yoxlanılmayanlar

| Bənd | Səbəb |
|---|---|
| Ezamiyyə normaları | Normativ akt mənbədə tapılmadı. **HR mütəxəssisi tərəfindən təsdiqlənməlidir.** Proqramda istifadə olunan dəyər: `config/trip.ts:5` (gündəlik = 30 AZN) |
| UI ekranları | Proqram `.env` olmadan işə düşmədi |

## 6. İstifadə olunan hüquqi mənbələr

| Akt | Maddələr | Link | Yoxlama tarixi |
|---|---|---|---|
| Əmək Məcəlləsi | 89, 114, 116 | https://e-qanun.az/framework/46943 | YYYY-MM-DD |

---
*Bu sənəd daxili yoxlamanın nəticəsidir və rəsmi audit rəyi və ya hüquqi rəy deyil.*
````

## Yazı tərzi

- Sahə dilində yaz. Oxucu HR rəhbəri və proqramçıdır: təsvir və "niyə problemdir" HR rəhbəri, sübut və tövsiyə proqramçı üçündür.
- Hər tapıntıda bir problem olsun. Eyni səbəbdən yaranan bir neçə simptomu bir tapıntıda birləşdir.
- Tövsiyə icra oluna bilən olsun: "düzəlt" yox, "`BASE_DAYS` dəyərini vəzifə kateqoriyasından asılı et (21/30) və test əlavə et".
