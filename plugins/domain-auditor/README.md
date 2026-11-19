# domain-auditor: sahə auditoru

Proqramı yazıb bitirəndən sonra onu həmin sahənin mütəxəssisi gözü ilə yoxlatmaq üçün plugin. Məsələn:

```
/audit HR
/audit maliyyə
/audit anbar
```

Claude sahə auditoru kimi layihəni öyrənir: kodu, verilənlər bazası sxemini, testləri və sənədləri oxuyur, mümkün olduqda proqramı işə salıb ekranlara baxır. Sonra layihəni sahənin yoxlama siyahısı üzrə yoxlayır və layihənin kök qovluğunda `audit-hesabati-<sahə>-<tarix>.md` hesabatını yazır.

## Nə yoxlanılır (HR)

- Funksional tamlıq: işə qəbul, əmrlər, müqavilə, məzuniyyət, ezamiyyət, xəstəlik vərəqəsi, xitam, kadr uçotu, ştat cədvəli, performans
- Azərbaycan Respublikasının Əmək Məcəlləsinə uyğunluq
- Hesablamalar: məzuniyyət qalığı, staj, iş günləri, bayramlar
- "Fərdi məlumatlar haqqında" Qanun: FİN, maaş və səhhət məlumatlarının qorunması
- Rollar, icazələr, audit izi
- Sənəd şablonları, istifadə rahatlığı, qısa texniki yoxlama

Hüquqi dəyərlər yaddaşdan yazılmır. Onlar e-qanun.az-dan maddə, link və yoxlama tarixi ilə götürülür. Yoxlana bilməyən bəndlər "HR mütəxəssisi tərəfindən təsdiqlənməlidir" kimi işarələnir.

## Hesabat

- İcmal: 1–5 qiymət, risk dərəcələri üzrə say, ən vacib 3 tövsiyə
- Tapıntılar: nömrə, bölmə, risk (Kritik / Yüksək / Orta / Aşağı), təsvir, sübut (fayl:sətir), niyə problemdir, tövsiyə
- Uyğun bəndlər, yoxlanılmayanlar, hüquqi mənbələr
- Qeyd: daxili yoxlamadır, rəsmi audit rəyi deyil

Excel-ə ixrac (yalnız standart Python kitabxanası ilə):

```bash
python3 skills/audit/scripts/export_xlsx.py audit-hesabati-hr-2026-11-19.md
```

## Struktur

```
domain-auditor/
├── .claude-plugin/plugin.json
├── commands/audit.md            # /audit <sahə>
├── agents/domain-auditor.md     # yalnız oxuma alətləri (Read, Grep, Glob, WebFetch, WebSearch)
└── skills/audit/
    ├── SKILL.md                 # audit mərhələləri
    ├── references/
    │   ├── hr.md                # HR yoxlama siyahısı + təsdiqlənmiş hüquqi dəyərlər
    │   ├── umumi-metodologiya.md# siyahısı olmayan sahələr üçün
    │   └── hesabat-shablonu.md
    └── scripts/export_xlsx.py
```

## Yeni sahə əlavə etmək

`skills/audit/references/<sahə>.md` faylını `hr.md`-nin strukturu ilə yaradın (təsdiqlənmiş dəyərlər cədvəli + 9 bölmə). Faylın adı sahənin açar sözü olmalıdır (`maliyye`, `anbar`) və SKILL.md-dəki sahə xəritəsinə əlavə edilməlidir. Siyahısı olmayan sahələr üçün auditor ümumi metodologiyadan istifadə edir və bunu hesabatda qeyd edir.

## Məhdudiyyətlər

Bu plugin daxili yoxlama alətidir. Onun hesabatı rəsmi audit rəyi və ya hüquqi məsləhət deyil. Qanunvericilik dəyişir: `hr.md`-dəki dəyərlərin yoxlama tarixinə baxın.

## Lisenziya

MIT
