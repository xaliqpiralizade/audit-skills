# Ümumi audit metodologiyası

Bu fayl sahə üçün hazır yoxlama siyahısı (`references/<sahə>.md`) **olmadıqda** istifadə olunur. Məqsəd həmin sahə üçün ağlabatan bir yoxlama siyahısını audit zamanı qurmaqdır. Hesabatda bunun ümumi metodologiya ilə aparıldığını açıq yaz.

## 1. Sahəni modelləşdir

Kodu oxumazdan əvvəl, həmin sahənin mütəxəssisi kimi düşün və qısa qeyd et:

- **Əsas obyektlər**: sahədə nələr idarə olunur? (maliyyə: hesab, provodka, faktura; anbar: məhsul, partiya, hərəkət, qalıq.)
- **Əsas proseslər**: hər obyektin həyat dövrü (yaradılır → təsdiqlənir → dəyişir → bağlanır/arxivlənir).
- **İnvariantlar**: nə heç vaxt pozulmamalıdır? (debet = kredit; qalıq mənfi olmaz; bağlanmış dövr dəyişməz.)
- **Hesablamalar**: hansı rəqəmlər hesablanır və səhv olarsa, kim zərər çəkir?
- **Tənzimləyici çərçivə**: hansı qanunlar və standartlar tətbiq oluna bilər (Vergi Məcəlləsi, mühasibat uçotu standartları, sahə qaydaları)? Rəqəm yazma, yalnız mövzunu adlandır. Konkret dəyəri mənbədən (e-qanun.az, rəsmi dövlət saytları) yoxla, tapa bilməsən "<sahə> mütəxəssisi tərəfindən təsdiqlənməlidir" kimi işarələ.
- **Rollar**: kim nə edir, kim nəyi təsdiqləyir, kim nəyi görməməlidir (vəzifələrin bölünməsi).

## 2. Yoxlama siyahısını qur

Hər sahədə tətbiq olunan doqquz baxış bucağı (HR siyahısının strukturu ilə eyni):

1. **Funksional tamlıq** — əsas proseslər başdan sona varmı?
2. **Tənzimləyici uyğunluq** — mənbə ilə yoxlanılan bəndlər.
3. **Hesablamaların düzgünlüyü** — sərhəd halları, yuvarlaqlaşdırma, tarix/valyuta.
4. **Məlumatların bütövlüyü** — invariantlar DB səviyyəsində (constraint, tranzaksiya) qorunurmu?
5. **Konfidensial məlumatlar** — fərdi və kommersiya məlumatları (bax: "Fərdi məlumatlar haqqında" Qanun, https://e-qanun.az/framework/19675).
6. **Hüquqlar, rollar, audit izi**.
7. **Sənədlər və hesabatlar** — sahə üçün məcburi formalar.
8. **İstifadə rahatlığı** — sahə mütəxəssisinin gündəlik işi.
9. **Qısa texniki yoxlama** — sirlər, autentifikasiya, ehtiyat nüsxə, xəta halları.

Hər baxış bucağı üçün 3–8 konkret, yoxlanıla bilən bənd yaz. Qurduğun siyahını hesabatın "Əhatə dairəsi və metodologiya" bölməsinə qısa şəkildə daxil et ki, oxucu nəyin yoxlandığını bilsin.

## 3. Məhdudiyyətləri qeyd et

Hesabatın əvvəlinə bu xəbərdarlığı əlavə et:

> Bu sahə (`<sahə>`) üçün hazır yoxlama siyahısı yoxdur. Audit ümumi metodologiya əsasında aparılıb. Yoxlama siyahısını auditor özü qurub, ona görə sahəyə xas bəzi tələblər nəzərdən qaçmış ola bilər. Nəticələri sahə mütəxəssisi ilə müzakirə etmək tövsiyə olunur.

Audit bitəndən sonra istifadəçiyə təklif et ki, qurulmuş yoxlama siyahısı gələcək auditlər üçün `references/<sahə>.md` kimi saxlanılsın.
