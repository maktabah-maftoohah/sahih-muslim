"""Seed script for Sahih Muslim books and Book 1 data conforming to Maktabah Maftoohah standards."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
BOOKS_FILE = DATA_DIR / "books.json"
CHAPTERS_DIR = DATA_DIR / "chapters"
HADITHS_DIR = DATA_DIR / "hadiths"

# Canonical 54 books of Sahih Muslim
BOOKS_DATA = [
  {"book_number": 1, "title_ar": "كتاب الإيمان", "title_ms": "Kitab Iman", "title_en": "Book of Faith", "hadith_start": 1, "hadith_end": 430, "hadith_count": 430},
  {"book_number": 2, "title_ar": "كتاب الطهارة", "title_ms": "Kitab Bersuci (Taharah)", "title_en": "Book of Purification", "hadith_start": 431, "hadith_end": 578, "hadith_count": 148},
  {"book_number": 3, "title_ar": "كتاب الحيض", "title_ms": "Kitab Haid", "title_en": "Book of Menstruation", "hadith_start": 579, "hadith_end": 686, "hadith_count": 108},
  {"book_number": 4, "title_ar": "كتاب الصلاة", "title_ms": "Kitab Solat", "title_en": "Book of Prayers", "hadith_start": 687, "hadith_end": 1057, "hadith_count": 371},
  {"book_number": 5, "title_ar": "كتاب المساجد ومواضع الصلاة", "title_ms": "Kitab Masjid dan Tempat Solat", "title_en": "Book of Mosques and Places of Prayer", "hadith_start": 1058, "hadith_end": 1569, "hadith_count": 512},
  {"book_number": 6, "title_ar": "كتاب صلاة المسافرين وقصرها", "title_ms": "Kitab Solat Musafir dan Qasar", "title_en": "Book of Prayer of Travelers", "hadith_start": 1570, "hadith_end": 1782, "hadith_count": 213},
  {"book_number": 7, "title_ar": "كتاب الجمعة", "title_ms": "Kitab Solat Jumaat", "title_en": "Book of Friday Prayer", "hadith_start": 1783, "hadith_end": 1845, "hadith_count": 63},
  {"book_number": 8, "title_ar": "كتاب صلاة العيدين", "title_ms": "Kitab Solat Dua Hari Raya", "title_en": "Book of Prayer of Two Eids", "hadith_start": 1846, "hadith_end": 1867, "hadith_count": 22},
  {"book_number": 9, "title_ar": "كتاب صلاة الاستسقاء", "title_ms": "Kitab Solat Istisqa'", "title_en": "Book of Prayer for Rain", "hadith_start": 1868, "hadith_end": 1878, "hadith_count": 11},
  {"book_number": 10, "title_ar": "كتاب الكسوف", "title_ms": "Kitab Solat Gerhana", "title_en": "Book of Prayer of Eclipses", "hadith_start": 1879, "hadith_end": 1906, "hadith_count": 28},
  {"book_number": 11, "title_ar": "كتاب الجنائز", "title_ms": "Kitab Jenazah", "title_en": "Book of Funerals", "hadith_start": 1907, "hadith_end": 2043, "hadith_count": 137},
  {"book_number": 12, "title_ar": "كتاب الزكاة", "title_ms": "Kitab Zakat", "title_en": "Book of Zakat", "hadith_start": 2044, "hadith_end": 2341, "hadith_count": 298},
  {"book_number": 13, "title_ar": "كتاب الصيام", "title_ms": "Kitab Puasa", "title_en": "Book of Fasting", "hadith_start": 2342, "hadith_end": 2581, "hadith_count": 240},
  {"book_number": 14, "title_ar": "كتاب الاعتكاف", "title_ms": "Kitab Iktikaf", "title_en": "Book of I'tikaf", "hadith_start": 2582, "hadith_end": 2596, "hadith_count": 15},
  {"book_number": 15, "title_ar": "كتاب الحج", "title_ms": "Kitab Haji", "title_en": "Book of Pilgrimage (Hajj)", "hadith_start": 2597, "hadith_end": 3159, "hadith_count": 563},
  {"book_number": 16, "title_ar": "كتاب النكاح", "title_ms": "Kitab Nikah", "title_en": "Book of Marriage", "hadith_start": 3160, "hadith_end": 3397, "hadith_count": 238},
  {"book_number": 17, "title_ar": "كتاب الرضاع", "title_ms": "Kitab Penyusuan", "title_en": "Book of Suckling", "hadith_start": 3398, "hadith_end": 3462, "hadith_count": 65},
  {"book_number": 18, "title_ar": "كتاب الطلاق", "title_ms": "Kitab Talak", "title_en": "Book of Divorce", "hadith_start": 3463, "hadith_end": 3532, "hadith_count": 70},
  {"book_number": 19, "title_ar": "كتاب اللعان", "title_ms": "Kitab Li'an", "title_en": "Book of Invoking Curses (Li'an)", "hadith_start": 3533, "hadith_end": 3559, "hadith_count": 27},
  {"book_number": 20, "title_ar": "كتاب العتق", "title_ms": "Kitab Memerdekakan Hamba", "title_en": "Book of Emancipation of Slaves", "hadith_start": 3560, "hadith_end": 3608, "hadith_count": 49},
  {"book_number": 21, "title_ar": "كتاب البيوع", "title_ms": "Kitab Jual Beli", "title_en": "Book of Transactions", "hadith_start": 3609, "hadith_end": 3760, "hadith_count": 152},
  {"book_number": 22, "title_ar": "كتاب المساقاة", "title_ms": "Kitab Pengairan dan Pertanian", "title_en": "Book of Sharecropping and Watering", "hadith_start": 3761, "hadith_end": 3937, "hadith_count": 177},
  {"book_number": 23, "title_ar": "كتاب الفرائض", "title_ms": "Kitab Pembahagian Pusaka", "title_en": "Book of Inheritance", "hadith_start": 3938, "hadith_end": 3960, "hadith_count": 23},
  {"book_number": 24, "title_ar": "كتاب الهبات", "title_ms": "Kitab Hadiah (Hibah)", "title_en": "Book of Gifts", "hadith_start": 3961, "hadith_end": 3991, "hadith_count": 31},
  {"book_number": 25, "title_ar": "كتاب الوصية", "title_ms": "Kitab Wasiat", "title_en": "Book of Wills", "hadith_start": 3992, "hadith_end": 4016, "hadith_count": 25},
  {"book_number": 26, "title_ar": "كتاب النذر", "title_ms": "Kitab Nazar", "title_en": "Book of Vows", "hadith_start": 4017, "hadith_end": 4031, "hadith_count": 15},
  {"book_number": 27, "title_ar": "كتاب الأيمان", "title_ms": "Kitab Sumpah", "title_en": "Book of Oaths", "hadith_start": 4032, "hadith_end": 4104, "hadith_count": 73},
  {"book_number": 28, "title_ar": "كتاب القسامة والمحاربين والقصاص والديات", "title_ms": "Kitab Qasamah, Qisas dan Diyat", "title_en": "Book of Oaths, Retaliation and Blood Money", "hadith_start": 4105, "hadith_end": 4153, "hadith_count": 49},
  {"book_number": 29, "title_ar": "كتاب الحدود", "title_ms": "Kitab Hudud", "title_en": "Book of Punishments", "hadith_start": 4154, "hadith_end": 4213, "hadith_count": 60},
  {"book_number": 30, "title_ar": "كتاب الأقضية", "title_ms": "Kitab Kehakiman", "title_en": "Book of Judicial Decisions", "hadith_start": 4214, "hadith_end": 4235, "hadith_count": 22},
  {"book_number": 31, "title_ar": "كتاب اللقطة", "title_ms": "Kitab Barang Temuan", "title_en": "Book of Lost Property", "hadith_start": 4236, "hadith_end": 4252, "hadith_count": 17},
  {"book_number": 32, "title_ar": "كتاب الجهاد والسير", "title_ms": "Kitab Jihad dan Ekspedisi", "title_en": "Book of Jihad and Expeditions", "hadith_start": 4253, "hadith_end": 4446, "hadith_count": 194},
  {"book_number": 33, "title_ar": "كتاب الإمارة", "title_ms": "Kitab Kepimpinan dan Pemerintahan", "title_en": "Book of Government / Leadership", "hadith_start": 4447, "hadith_end": 4642, "hadith_count": 196},
  {"book_number": 34, "title_ar": "كتاب الصيد والذبائح وما يؤكل من الحيوان", "title_ms": "Kitab Buruan dan Sembelihan", "title_en": "Book of Hunting and Slaughter", "hadith_start": 4643, "hadith_end": 4721, "hadith_count": 79},
  {"book_number": 35, "title_ar": "كتاب الأضاحي", "title_ms": "Kitab Korban (Udhiyyah)", "title_en": "Book of Sacrifices", "hadith_start": 4722, "hadith_end": 4768, "hadith_count": 47},
  {"book_number": 36, "title_ar": "كتاب الأشربة", "title_ms": "Kitab Minuman", "title_en": "Book of Drinks", "hadith_start": 4769, "hadith_end": 4983, "hadith_count": 215},
  {"book_number": 37, "title_ar": "كتاب اللباس والزينة", "title_ms": "Kitab Pakaian dan Perhiasan", "title_en": "Book of Clothes and Decoration", "hadith_start": 4984, "hadith_end": 5126, "hadith_count": 143},
  {"book_number": 38, "title_ar": "كتاب الآداب", "title_ms": "Kitab Adab", "title_en": "Book of Manners and Etiquette", "hadith_start": 5127, "hadith_end": 5176, "hadith_count": 50},
  {"book_number": 39, "title_ar": "كتاب السلام", "title_ms": "Kitab Memberi Salam", "title_en": "Book of Greetings (Salam)", "hadith_start": 5177, "hadith_end": 5351, "hadith_count": 175},
  {"book_number": 40, "title_ar": "كتاب الألفاظ من الأدب وغيرها", "title_ms": "Kitab Lafaz-Lafaz dan Panggilan", "title_en": "Book of General Manners", "hadith_start": 5352, "hadith_end": 5373, "hadith_count": 22},
  {"book_number": 41, "title_ar": "كتاب الشعر", "title_ms": "Kitab Syair", "title_en": "Book of Poetry", "hadith_start": 5374, "hadith_end": 5382, "hadith_count": 9},
  {"book_number": 42, "title_ar": "كتاب الرؤيا", "title_ms": "Kitab Mimpi", "title_en": "Book of Dreams", "hadith_start": 5383, "hadith_end": 5408, "hadith_count": 26},
  {"book_number": 43, "title_ar": "كتاب الفضائل", "title_ms": "Kitab Keutamaan Nabi ﷺ", "title_en": "Book of Virtues", "hadith_start": 5409, "hadith_end": 5585, "hadith_count": 177},
  {"book_number": 44, "title_ar": "كتاب فضائل الصحابة", "title_ms": "Kitab Keutamaan Para Sahabat", "title_en": "Book of Virtues of the Companions", "hadith_start": 5586, "hadith_end": 5835, "hadith_count": 250},
  {"book_number": 45, "title_ar": "كتاب البر والصلة والآداب", "title_ms": "Kitab Kebajikan, Silaturahim dan Akhlak", "title_en": "Book of Virtue, Good Manners and Ties of Kinship", "hadith_start": 5836, "hadith_end": 6079, "hadith_count": 244},
  {"book_number": 46, "title_ar": "كتاب القدر", "title_ms": "Kitab Qadar (Ketetapan Ilahi)", "title_en": "Book of Destiny", "hadith_start": 6080, "hadith_end": 6124, "hadith_count": 45},
  {"book_number": 47, "title_ar": "كتاب العلم", "title_ms": "Kitab Ilmu", "title_en": "Book of Knowledge", "hadith_start": 6125, "hadith_end": 6147, "hadith_count": 23},
  {"book_number": 48, "title_ar": "كتاب الذكر والدعاء والتوبة والاستغفار", "title_ms": "Kitab Zikir, Doa, Taubat dan Istighfar", "title_en": "Book of Remembrance, Supplication and Repentance", "hadith_start": 6148, "hadith_end": 6314, "hadith_count": 167},
  {"book_number": 49, "title_ar": "كتاب الرقاق", "title_ms": "Kitab Kelembutan Hati", "title_en": "Book of Heart-Melting Traditions", "hadith_start": 6315, "hadith_end": 6370, "hadith_count": 56},
  {"book_number": 50, "title_ar": "كتاب التوبة", "title_ms": "Kitab Taubat", "title_en": "Book of Repentance", "hadith_start": 6371, "hadith_end": 6439, "hadith_count": 69},
  {"book_number": 51, "title_ar": "كتاب صفات المنافقين وأحكامهم", "title_ms": "Kitab Sifat-Sifat Golongan Munafik", "title_en": "Book of Characteristics of Hypocrites", "hadith_start": 6440, "hadith_end": 6461, "hadith_count": 22},
  {"book_number": 52, "title_ar": "كتاب صفة القيامة والجنة والنار", "title_ms": "Kitab Sifat Kiamat, Syurga dan Neraka", "title_en": "Book of Resurrection, Paradise and Hell", "hadith_start": 6462, "hadith_end": 6554, "hadith_count": 93},
  {"book_number": 53, "title_ar": "كتاب الجنة وصفة نعيمها وأهلها", "title_ms": "Kitab Syurga dan Kenikmatannya", "title_en": "Book of Paradise and Its Delights", "hadith_start": 6555, "hadith_end": 6640, "hadith_count": 86},
  {"book_number": 54, "title_ar": "كتاب الفتن وأشراط الساعة", "title_ms": "Kitab Fitnah Akhir Zaman dan Tanda Kiamat", "title_en": "Book of Tribulations and Signs of the Hour", "hadith_start": 6641, "hadith_end": 6776, "hadith_count": 136}
]

# Book 1 Chapters
CHAPTERS_BOOK_1 = [
  {"chapter_number": 1, "title_ar": "باب بَيَانِ الإِيمَانِ وَالإِسْلاَمِ وَالإِحْسَانِ وَوُجُوبِ الإِيمَانِ بِإِثْبَاتِ قَدَرِ اللَّهِ سُبْحَانَهُ وَتَعَالَى", "title_ms": "Bab: Penjelasan tentang Iman, Islam, Ihsan, dan Kewajipan Beriman kepada Takdir Allah", "title_en": "Chapter: Clarification of Iman, Islam, and Ihsan; and the Obligation of Believing in the Decree of Allah", "hadith_start": 1, "hadith_end": 2},
  {"chapter_number": 2, "title_ar": "باب بَيَانِ الإِيمَانِ الَّذِي يَدْخُلُ بِهِ الْجَنَّةَ", "title_ms": "Bab: Penjelasan Iman yang Membawa ke Syurga", "title_en": "Chapter: Clarification of Faith through which one enters Paradise", "hadith_start": 3, "hadith_end": 3},
  {"chapter_number": 3, "title_ar": "باب شُعَبِ الإِيمَانِ", "title_ms": "Bab: Cabang-Cabang Iman", "title_en": "Chapter: The Branches of Faith", "hadith_start": 4, "hadith_end": 4},
  {"chapter_number": 4, "title_ar": "باب بَيَانِ تَفَاضُلِ الإِسْلاَمِ وَأَيِّ أُمُورِهِ أَفْضَلُ", "title_ms": "Bab: Keutamaan Islam dan Amalan yang Paling Utama", "title_en": "Chapter: The Excellence of Islam and its Foremost Deeds", "hadith_start": 5, "hadith_end": 5}
]

# Book 1 Hadiths 1-5
HADITHS_BOOK_1 = [
  {
    "collection_id": "sahih-muslim",
    "hadith_number": 1,
    "in_book_number": 1,
    "book_number": 1,
    "book_title": {"ar": "كتاب الإيمان", "ms": "Kitab Iman", "en": "Book of Faith"},
    "chapter_number": 1,
    "chapter_title": {"ar": "باب بَيَانِ الإِيمَانِ وَالإِسْلاَمِ وَالإِحْسَانِ", "ms": "Bab: Penjelasan Iman, Islam, dan Ihsan", "en": "Chapter: Clarification of Iman, Islam, and Ihsan"},
    "arabic": "حَدَّثَنِي أَبُو خَيْثَمَةَ زُهَيْرُ بْنُ حَرْبٍ، حَدَّثَنَا وَكِيعٌ، عَنْ كَهْمَسٍ، عَنْ عَبْدِ اللَّهِ بْنِ بُرَيْدَةَ، عَنْ يَحْيَى بْنِ يَعْمَرَ، قَالَ: كَانَ أَوَّلَ مَنْ قَالَ فِي الْقَدَرِ بِالْبَصْرَةِ مَعْبَدٌ الْجُهَنِيُّ، فَانْطَلَقْتُ أَنَا وَحُمَيْدُ بْنُ عَبْدِ الرَّحْمَنِ الْحِمْيَرِيُّ حَاجَّيْنِ أَوْ مُعْتَمِرَيْنِ، فَقُلْنَا: لَوْ لَقِينَا أَحَدًا مِنْ أَصْحَابِ رَسُولِ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ فَسَأَلْنَاهُ عَمَّا يَقُولُ هَؤُلاَءِ فِي الْقَدَرِ، فَوُفِّقَ لَنَا عَبْدُ اللَّهِ بْنُ عُمَرَ بْنِ الْخَطَّابِ... فَقَالَ: حَدَّثَنِي أَبِي عُمَرُ بْنُ الْخَطَّابِ، قَالَ: بَيْنَمَا نَحْنُ عِنْدَ رَسُولِ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ ذَاتَ يَوْمٍ إِذْ طَلَعَ عَلَيْنَا رَجُلٌ شَدِيدُ بَيَاضِ الثِّيَابِ شَدِيدُ سَوَادِ الشَّعَرِ، لاَ يُرَى عَلَيْهِ أَثَرُ السَّفَرِ وَلاَ يَعْرِفُهُ مِنَّا أَحَدٌ، حَتَّى جَلَسَ إِلَى النَّبِيِّ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ فَأَسْنَدَ رُكْبَتَيْهِ إِلَى رُكْبَتَيْهِ وَوَضَعَ كَفَّيْهِ عَلَى فَخِذَيْهِ وَقَالَ: يَا مُحَمَّدُ، أَخْبِرْنِي عَنِ الإِسْلاَمِ...",
    "sanad_text": "حَدَّثَنِي أَبُو خَيْثَمَةَ زُهَيْرُ بْنُ حَرْبٍ، حَدَّثَنَا وَكِيعٌ، عَنْ كَهْمَسٍ، عَنْ عَبْدِ اللَّهِ بْنِ بُرَيْدَةَ، عَنْ يَحْيَى بْنِ يَعْمَرَ، عَنْ عَبْدِ اللَّهِ بْنِ عُمَرَ، عَنْ عُمَرَ بْنِ الْخَطَّابِ قَالَ:",
    "matn_text": "بَيْنَمَا نَحْنُ عِنْدَ رَسُولِ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ ذَاتَ يَوْمٍ إِذْ طَلَعَ عَلَيْنَا رَجُلٌ شَدِيدُ بَيَاضِ الثِّيَابِ شَدِيدُ سَوَادِ الشَّعَرِ... قَالَ: يَا مُحَمَّدُ، أَخْبِرْنِي عَنِ الإِسْلاَمِ. فَقَالَ رَسُولُ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ: «الإِسْلاَمُ أَنْ تَشْهَدَ أَنْ لاَ إِلَهَ إِلاَّ اللَّهُ وَأَنَّ مُحَمَّدًا رَسُولُ اللَّهِ، وَتُقِيمَ الصَّلاَةَ، وَتُؤْتِيَ الزَّكَاةَ، وَتَصُومَ رَمَضَانَ، وَتَحُجَّ الْبَيْتَ إِنِ اسْتَطَعْتَ إِلَيْهِ سَبِيلًا»... قَالَ: فَأَخْبِرْنِي عَنِ الإِحْسَانِ. قَالَ: «أَنْ تَعْبُدَ اللَّهَ كَأَنَّكَ تَرَاهُ فَإِنْ لَمْ تَكُنْ تَرَاهُ فَإِنَّهُ يَرَاكَ»...",
    "gradings": [{"scholar": "Imam Muslim", "grade": "Sahih", "grade_ar": "صحيح"}],
    "translations": {
      "ms": "Hadis Jibril yang masyhur: Umar ibn al-Khattab r.a. meriwayatkan: 'Sedang kami duduk bersama Rasulullah ﷺ pada suatu hari, tiba-tiba muncul seorang lelaki yang berpakaian sangat putih dan berambut sangat hitam. Tidak kelihatan padanya tanda-tanda perjalanan jauh dan tiada seorang pun daripada kami yang mengenalinya... Beliau bertanya tentang Islam, Iman, Ihsan, dan tanda-tanda Kiamat. Kemudian Rasulullah ﷺ bersabda: Wahai Umar, tahukah engkau siapakah penyoal itu? Itu adalah Jibril yang datang mengajarkan kepada kamu agama kamu.'",
      "en": "The famous Hadith of Gabriel narrated by 'Umar bin Al-Khattab: 'While we were sitting with the Messenger of Allah ﷺ one day, there appeared before us a man dressed in extremely white clothes and with very black hair. No traces of journey were seen upon him and none of us knew him... He asked about Islam, Iman, Ihsan, and the Hour. The Messenger of Allah said: O 'Umar, do you know who the questioner was? It was Gabriel who came to teach you your religion.'"
    },
    "tags": ["hadis-jibril", "rukun-islam", "rukun-iman", "ihsan", "teras-akidah"]
  },
  {
    "collection_id": "sahih-muslim",
    "hadith_number": 3,
    "in_book_number": 3,
    "book_number": 1,
    "book_title": {"ar": "كتاب الإيمان", "ms": "Kitab Iman", "en": "Book of Faith"},
    "chapter_number": 2,
    "chapter_title": {"ar": "باب بَيَانِ الإِيمَانِ الَّذِي يَدْخُلُ بِهِ الْجَنَّةَ", "ms": "Bab: Iman yang Membawa ke Syurga", "en": "Chapter: Faith Leading to Paradise"},
    "arabic": "حَدَّثَنَا أَبُو بَكْرِ بْنُ أَبِي شَيْبَةَ، حَدَّثَنَا أَبُو خَالِدٍ الأَحْمَرُ، عَنْ أَبِي مَالِكٍ الأَشْجَعِيِّ، عَنْ سَعْدِ بْنِ عُبَيْدَةَ، عَنِ ابْنِ عُمَرَ، عَنِ النَّبِيِّ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ قَالَ: «بُنِيَ الإِسْلاَمُ عَلَى خَمْسَةٍ: عَلَى أَنْ يُوَحَّدَ اللَّهُ، وَإِقَامِ الصَّلاَةِ، وَإِيتَاءِ الزَّكَاةِ، وَصِيَامِ رَمَضَانَ، وَالْحَجِّ».",
    "sanad_text": "حَدَّثَنَا أَبُو بَكْرِ بْنُ أَبِي شَيْبَةَ، حَدَّثَنَا أَبُو خَالِدٍ الأَحْمَرُ، عَنْ أَبِي مَالِكٍ الأَشْجَعِيِّ، عَنْ سَعْدِ بْنِ عُبَيْدَةَ، عَنِ ابْنِ عُمَرَ، عَنِ النَّبِيِّ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ قَالَ:",
    "matn_text": "«بُنِيَ الإِسْلاَمُ عَلَى خَمْسَةٍ: عَلَى أَنْ يُوَحَّدَ اللَّهُ، وَإِقَامِ الصَّلاَةِ، وَإِيتَاءِ الزَّكَاةِ، وَصِيَامِ رَمَضَانَ، وَالْحَجِّ».",
    "gradings": [{"scholar": "Imam Muslim", "grade": "Sahih", "grade_ar": "صحيح"}],
    "translations": {
      "ms": "Daripada Ibnu Umar r.a., daripada Nabi ﷺ bersabda: 'Islam dibina di atas lima perkara: mentauhidkan Allah, mendirikan solat, menunaikan zakat, berpuasa pada bulan Ramadan, dan menunaikan haji.'",
      "en": "Narrated Ibn 'Umar that the Prophet said: 'Islam is built on five pillars: to profess the Oneness of Allah, establish the prayers, pay Zakat, fast during Ramadan, and perform Hajj.'"
    },
    "tags": ["rukun-islam", "tauhid", "ibadah"]
  },
  {
    "collection_id": "sahih-muslim",
    "hadith_number": 4,
    "in_book_number": 4,
    "book_number": 1,
    "book_title": {"ar": "كتاب الإيمان", "ms": "Kitab Iman", "en": "Book of Faith"},
    "chapter_number": 3,
    "chapter_title": {"ar": "باب شُعَبِ الإِيمَانِ", "ms": "Bab: Cabang-Cabang Iman", "en": "Chapter: The Branches of Faith"},
    "arabic": "حَدَّثَنَا قُتَيْبَةُ بْنُ سَعِيدٍ، حَدَّثَنَا لَيْثٌ، عَنْ يَزِيدَ بْنِ أَبِي حَبِيبٍ، عَنْ أَبِي الْخَيْرِ، عَنْ عَبْدِ اللَّهِ بْنِ عَمْرٍو، أَنَّ رَجُلًا سَأَلَ رَسُولَ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ: أَيُّ الإِسْلاَمِ خَيْرٌ؟ قَالَ: «تُطْعِمُ الطَّعَامَ، وَتَقْرَأُ السَّلاَمَ عَلَى مَنْ عَرَفْتَ وَمَنْ لَمْ تَعْرِفْ».",
    "sanad_text": "حَدَّثَنَا قُتَيْبَةُ بْنُ سَعِيدٍ، حَدَّثَنَا لَيْثٌ، عَنْ يَزِيدَ بْنِ أَبِي حَبِيبٍ، عَنْ أَبِي الْخَيْرِ، عَنْ عَبْدِ اللَّهِ بْنِ عَمْرٍو:",
    "matn_text": "أَنَّ رَجُلًا سَأَلَ رَسُولَ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ: أَيُّ الإِسْلاَمِ خَيْرٌ؟ قَالَ: «تُطْعِمُ الطَّعَامَ، وَتَقْرَأُ السَّلاَمَ عَلَى مَنْ عَرَفْتَ وَمَنْ لَمْ تَعْرِفْ».",
    "gradings": [{"scholar": "Imam Muslim", "grade": "Sahih", "grade_ar": "صحيح"}],
    "translations": {
      "ms": "Daripada Abdullah ibn 'Amr bahawa seorang lelaki bertanya kepada Rasulullah ﷺ: 'Amalan Islam yang manakah paling baik?' Baginda bersabda: 'Engkau memberi makan, dan mengucapkan salam kepada orang yang engkau kenal dan yang tidak engkau kenal.'",
      "en": "Narrated 'Abdullah bin 'Amr: A man asked the Messenger of Allah ﷺ: 'Which aspect of Islam is best?' He replied: 'To feed people and to extend greetings of peace to those you know and those you do not know.'"
    },
    "tags": ["memberi-makan", "salam", "kebajikan"]
  },
  {
    "collection_id": "sahih-muslim",
    "hadith_number": 5,
    "in_book_number": 5,
    "book_number": 1,
    "book_title": {"ar": "كتاب الإيمان", "ms": "Kitab Iman", "en": "Book of Faith"},
    "chapter_number": 4,
    "chapter_title": {"ar": "باب بَيَانِ تَفَاضُلِ الإِسْلاَمِ وَأَيِّ أُمُورِهِ أَفْضَلُ", "ms": "Bab: Keutamaan Islam", "en": "Chapter: The Excellence of Islam"},
    "arabic": "حَدَّثَنَا سَعِيدُ بْنُ عَمْرٍو الأَشْعَثِيُّ، وَأَبُو بَكْرِ بْنُ أَبِي شَيْبَةَ، قَالاَ: حَدَّثَنَا سُفْيَانُ بْنُ عُيَيْنَةَ، عَنْ سُهَيْلِ بْنِ أَبِي صَالِحٍ، عَنْ أَبِيهِ، عَنْ أَبِي هُرَيْرَةَ، عَنِ النَّبِيِّ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ قَالَ: «الإِيمَانُ بِضْعٌ وَسَبْعُونَ أَوْ بِضْعٌ وَسِتُّونَ شُعْبَةً، فَأَفْضَلُهَا قَوْلُ: لاَ إِلَهَ إِلاَّ اللَّهُ، وَأَدْنَاهَا إِمَاطَةُ الأَذَى عَنِ الطَّرِيقِ، وَالْحَيَاءُ شُعْبَةٌ مِنَ الإِيمَانِ».",
    "sanad_text": "حَدَّثَنَا سَعِيدُ بْنُ عَمْرٍو، وَأَبُو بَكْرِ بْنُ أَبِي شَيْبَةَ، حَدَّثَنَا سُفْيَانُ، عَنْ سُهَيْلٍ، عَنْ أَبِيهِ، عَنْ أَبِي هُرَيْرَةَ، عَنِ النَّبِيِّ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ قَالَ:",
    "matn_text": "«الإِيمَانُ بِضْعٌ وَسَبْعُونَ أَوْ بِضْعٌ وَسِتُّونَ شُعْبَةً، فَأَفْضَلُهَا قَوْلُ: لاَ إِلَهَ إِلاَّ اللَّهُ، وَأَدْنَاهَا إِمَاطَةُ الأَذَى عَنِ الطَّرِيقِ، وَالْحَيَاءُ شُعْبَةٌ مِنَ الإِيمَانِ».",
    "gradings": [{"scholar": "Imam Muslim", "grade": "Sahih", "grade_ar": "صحيح"}],
    "translations": {
      "ms": "Daripada Abu Hurairah r.a., daripada Nabi ﷺ bersabda: 'Iman itu mempunyai tujuh puluh lebih (atau enam puluh lebih) cabang. Yang paling utama ialah ucapan La ilaha illallah, dan yang paling rendah ialah menyingkirkan duri/gangguan dari jalanan, dan sifat malu itu adalah satu cabang daripada iman.'",
      "en": "Narrated Abu Huraira: The Prophet ﷺ said: 'Faith has over seventy branches, the best of which is the declaration that there is no god but Allah, and the lowest of which is the removal of harm from the path, and modesty is a branch of faith.'"
    },
    "tags": ["cabang-iman", "tauhid", "kebersihan", "malu"]
  }
]

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    HADITHS_DIR.mkdir(parents=True, exist_ok=True)

    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(BOOKS_DATA, f, ensure_ascii=False, indent=2)
    print(f"Written {len(BOOKS_DATA)} books to {BOOKS_FILE}")

    chap_file = CHAPTERS_DIR / "01.json"
    with open(chap_file, "w", encoding="utf-8") as f:
        json.dump(CHAPTERS_BOOK_1, f, ensure_ascii=False, indent=2)
    print(f"Written {len(CHAPTERS_BOOK_1)} chapters to {chap_file}")

    hadith_file = HADITHS_DIR / "01.json"
    with open(hadith_file, "w", encoding="utf-8") as f:
        json.dump(HADITHS_BOOK_1, f, ensure_ascii=False, indent=2)
    print(f"Written {len(HADITHS_BOOK_1)} hadiths to {hadith_file}")

    coll_file = DATA_DIR / "collection.json"
    coll_data = {
      "collection": "sahih-muslim",
      "title": "Maktabah Maftoohah — Sahih Muslim",
      "title_ar": "صحيح مسلم",
      "total_books": len(BOOKS_DATA),
      "total_hadiths": 7500,
      "seeded_books": [1],
      "active_hadiths": len(HADITHS_BOOK_1)
    }
    with open(coll_file, "w", encoding="utf-8") as f:
        json.dump(coll_data, f, ensure_ascii=False, indent=2)
    print(f"Updated {coll_file}")

if __name__ == "__main__":
    main()
