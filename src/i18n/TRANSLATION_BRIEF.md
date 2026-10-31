# Translation brief — Eastbridge Strategic Partners website

The site is for wealthy private buyers building or renovating a villa in Dubai or Abu Dhabi.
Eastbridge is an independent client-side project manager (owner's representative), paid only by the owner,
led by founder Philip Chapman, who spent 21 years running P Chapman Construction, an award-winning premium
builder in Cornwall, UK. Tone: calm, senior, precise, plain. Like a private bank or top architecture practice.
Never salesy, never machine-sounding. Write as a native professional copywriter in the target language would,
not word for word. Keep sentences short and clear.

## Format rules (strict)
- Input: a JSON object {key: English text}. Output: the same keys, values translated. Every key, nothing extra.
- Values may contain HTML. Keep every tag and attribute exactly as given (same tags, same count, same href values).
  Translate only the visible text between tags. You may move a tag pair to wrap the equivalent words.
- Keep numbers, currency and units as figures: "AED 15.12m", "8,050 sq ft", "31%", "2025". Use Western digits (0–9)
  in all languages, including Arabic. Use the language's normal way of writing millions where natural
  (Arabic "15.12 مليون درهم" is fine; Chinese "1512万迪拉姆" is fine; Russian "15,12 млн дирхамов"; Hindi "AED 15.12 मिलियन").
- Text that is only a name, a place, a number or a code: keep as is (see names below).
- Output must be valid JSON (escape double quotes inside values as \").

## Keep in Latin script, untranslated
Eastbridge, Eastbridge Strategic Partners, P Chapman Construction, Philip Chapman (may also be transliterated once
in running text, but keep Latin where it stands alone), WhatsApp, Google, Instagram, RIBA, LABC, NHBC, RICS, AED, GBP, £,
sq ft, project and house names (Saqqara, Sea Glass House, Morvoren, St Michael's Hotel and Spa, etc.) and UK place names
(Cornwall, Falmouth, Feock, Rock, Polzeath, St Ives...). Meydan Free Zone licence numbers.

## Dubai names: use the standard local-language form
Dubai, Abu Dhabi, Nakheel, Emaar, Dubai Municipality, Dubai Development Authority (DDA), Trakhees, Palm Jumeirah,
Palm Jebel Ali, Jumeirah Islands, Emirates Hills, Dubai Hills Estate, Jumeirah Golf Estates, Al Barari, Tilal Al Ghaf,
District One, Saadiyat Island, DEWA. Use the official Arabic names in Arabic; established Russian/Chinese/Hindi forms
elsewhere (Chinese: 迪拜, 阿布扎比, 朱美拉棕榈岛, 杰贝阿里棕榈岛, 纳赫勒(Nakheel)). "Island E" stays "Island E".

## Key terms (be consistent)
| English | Arabic | Russian | Chinese | Hindi |
|---|---|---|---|---|
| client-side project manager | مدير مشروع من جانب المالك | менеджер проекта на стороне заказчика | 业主方项目经理 | क्लाइंट-साइड प्रोजेक्ट मैनेजर |
| owner's representative | ممثل المالك | представитель заказчика | 业主代表 | ओनर्स रिप्रेज़ेंटेटिव (मालिक का प्रतिनिधि) |
| registered consultant (consultant of record) | الاستشاري المسجّل | зарегистрированный консультант (проектировщик) | 注册顾问(设计及监理单位) | पंजीकृत कंसल्टेंट |
| main contractor | المقاول الرئيسي | генеральный подрядчик | 总承包商 | मुख्य ठेकेदार |
| master developer | المطوّر الرئيسي | мастер-девелопер | 总开发商 | मास्टर डेवलपर |
| plot | قطعة الأرض | участок | 地块 | प्लॉट |
| variation | أمر تغييري | изменение (вариация) | 变更 | वेरिएशन (बदलाव) |
| handover / snagging | التسليم / قائمة الملاحظات | передача / устранение недочётов | 交付 / 缺陷整改 | हैंडओवर / स्नैगिंग |
| contingency | مخصص الطوارئ | резерв на непредвиденные расходы | 不可预见费 | आकस्मिक निधि (कंटिंजेंसी) |
| tender / bids | مناقصة / عروض | тендер / предложения | 招标 / 报价 | टेंडर / बोलियाँ |
| Illustrative case study | دراسة حالة توضيحية | Иллюстративный кейс | 示例案例研究 | उदाहरणात्मक केस स्टडी |

## Compliance (must survive translation)
- Eastbridge is NOT an engineer, architect or contractor and does not design or sign drawings. It works alongside the
  registered consultant. Do not translate "project manager" as "engineer" or "consultant". Do not add claims.
- The Island E case study is illustrative. Keep every word that signals that ("illustrative", "modelled", "fictional").
- Do not add or imply that Eastbridge has completed projects or clients in the UAE.
- Don't soften or strengthen numbers, guarantees or legal statements. Translate "about", "typically", "can" faithfully.
- Hindi: natural modern Hindi as used by educated professionals; common English business terms may be written in
  Devanagari (प्रोजेक्ट, बजट, कॉन्ट्रैक्टर). Not Sanskritised, not Hinglish in Latin script.
- Chinese: Simplified Chinese for mainland buyers; use Chinese punctuation (，。：“”).
- Arabic: Modern Standard Arabic, Gulf-friendly, elegant and formal but not ornate.
- Russian: business Russian, «ёлочки» quotes, no anglicisms where a normal Russian term exists.
