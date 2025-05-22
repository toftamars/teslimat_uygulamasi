# -*- coding: utf-8 -*-

DELIVERY_SCHEDULE = {
    "anadolu": {
        "pazartesi": ["MALTEPE", "KARTAL", "PENDİK", "TUZLA", "SULTANBEYLİ"],
        "sali": ["ÜSKÜDAR", "KADIKÖY", "ÜMRANİYE", "ATAŞEHİR"],
        "carsamba": ["ÜSKÜDAR", "KADIKÖY", "ÜMRANİYE", "ATAŞEHİR"],
        "persembe": ["MALTEPE", "KARTAL", "PENDİK", "TUZLA", "SULTANBEYLİ"],
        "cuma": ["ÜSKÜDAR", "KADIKÖY", "ÜMRANİYE", "ATAŞEHİR"],
        "cumartesi": ["BEYKOZ", "ÇEKMEKÖY", "SANCAKTEPE", "ŞİLE"],
        "pazar": [],  # Teslimat yok
    },
    "avrupa": {
        "pazartesi": ["ŞİŞLİ", "BEŞİKTAŞ", "BEYOĞLU", "KAĞITHANE"],
        "sali": ["SARIYER", "EYÜPSULTAN", "SULTANGAZİ", "GAZİOSMANPAŞA"],
        "carsamba": ["BAĞCILAR", "BAHÇELİEVLER", "BAKIRKÖY", "GÜNGÖREN", "ESENLER", "ZEYTİNBURNU", "BAYRAMPAŞA", "FATİH"],
        "persembe": ["BÜYÜKÇEKMECE", "SİLİVRİ", "ÇATALCA", "ARNAVUTKÖY", "BAKIRKÖY"],
        "cuma": ["ŞİŞLİ", "BEŞİKTAŞ", "BEYOĞLU", "KAĞITHANE"],
        "cumartesi": ["BÜYÜKÇEKMECE", "SİLİVRİ", "ÇATALCA", "ARNAVUTKÖY", "BAKIRKÖY"],
        "pazar": [],  # Teslimat yok
    }
}

MAX_DELIVERIES_PER_DAY = {
    "anadolu": 7,
    "avrupa": 7,
}

# İlçelerin hangi yakada olduğunu hızlıca bulmak için
DISTRICT_TO_REGION = {}
for region, days in DELIVERY_SCHEDULE.items():
    for day, districts in days.items():
        for district in districts:
            if district not in DISTRICT_TO_REGION:
                DISTRICT_TO_REGION[district] = region 