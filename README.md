# YYSpor Esenlikle Sunar

## Dynamic Form Builder

> Web'de form tasarla, QR'la tarat, mobilde render et.

Dinamik form ihtiyacini cozmek icin yapildi.
Form alanlari web uzerinden olusturulur, QR kodu ile mobil uygulamaya iletilir, mobil tarafta canli render edilir.

Kimse "ben bu formu backend'den bekleyeyim 3 sprint" demesin diye var.

---

### Nasil Calisiyor?

1. **Web Builder'da** formu tasarla (text, dropdown, checkbox, date, amount, info card...)
2. **Paylas** butonuna bas - form JSON olarak buluta yuklenir, kisa bir URL olusur
3. **QR kodunu** mobil uygulama ile tarat
4. Form mobilde canli olarak render edilir, dependency'ler tetiklenir, validation calisir

Bulut servis cokerse (olur oyle seyler) otomatik olarak sikistirilmis QR fallback devreye girer.

---

### Dosyalar

```
index.html          # Web builder, tek dosya, sil bastan
templates.json      # Hazir form sablonlari (repo'ya ekle, otomatik yuklenir)
```

### Template Eklemek

`templates.json`'a yeni bir obje at, push'la, bitti:

```json
{
  "name": "Guzel Bir Form",
  "desc": "Ne icin oldugunu sen bilirsin",
  "json": {
    "Sections": [...],
    "FormFields": [...]
  }
}
```

Sayfa acildiginda GitHub'dan otomatik cekilir. Arkadaslarina link at, gerisini builder halleder.

---

*Bir sabah "ya QR ile form paylassak" dedik. 2 gun sonra CORS nedir ogrendik. Pisman miyiz? Biraz.*
