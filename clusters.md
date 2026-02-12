## 1. Цифровые и интеллектуальные технологии
Фокус: алгоритмы, данные, цифровые системы, автоматизация.
Входят:
AI — ИИ и машинное обучение
Data — Данные и аналитика
IT — ИТ
Cyber — Кибербезопасность
Robotics — Робототехника
Systems — Системная инженерия
Technology — Технологические отрасли
Drones — Дроны и беспилотные системы
## 2. Наука, медицина и новые материалы
Фокус: фундаментальные исследования + прикладная бионаука и здоровье.
Входят:
Science — Наука
Innovation — Наука и инновации
Biotech — Биотехнологии
Materials — Новые материалы и нанотехнологии
Health — Медицина
## 3. Устойчивая среда и природные ресурсы
Фокус: экология, энергия, природные системы, ресурсы планеты.
Входят:
Ecology — Экология
Energy — Энергетика
Water — Морская индустрия и водные ресурсы
Mining — Добыча и переработка полезных ископаемых
Agriculture — Сельское хозяйство
## 4. Инфраструктура, транспорт и промышленность
Фокус: физический мир, производство, города.
Входят:
Industry — Промышленность
Construction — Строительство
Infrastructure — Инфраструктура и строительство
Urban — Городская среда и урбанистика
Transport — Транспорт и логистика
Logistics — Транспорт и логистика
Aviation — Авиация
Space — Космос
## 5. Экономика, управление и рынок труда
Фокус: организационные системы и управление людьми и ресурсами.
Входят:
Economy — Финансовый сектор
Management — Менеджмент
Work — Рынок труда и менеджмент
Career — Карьера и профориентация
Safety — Безопасность
## 6. Человек, общество и креативные индустрии
Фокус: культура, коммуникации, социальные процессы.
Входят:
Education — Образование
Psychology — Социальная сфера
Society — Социальная сфера
Ethics — Социальная сфера
Communication — Коммуникации и медиа
Media — Медиа и развлечения
Culture — Культура и искусство
Design — Дизайн и креативные индустрии
Food — Пищевая промышленность
Tourism — Индустрия туризма и гостеприимства

CLUSTERS = {
    "digital_intelligence": "Цифровые и интеллектуальные технологии",
    "science_health_materials": "Наука, медицина и новые материалы",
    "sustainable_environment": "Устойчивая среда и природные ресурсы",
    "infrastructure_transport_industry": "Инфраструктура, транспорт и промышленность",
    "economy_management_work": "Экономика, управление и рынок труда",
    "human_society_creative": "Человек, общество и креативные индустрии",
}


SPHERE_TO_CLUSTER_ID = {
    # 1) Цифровые и интеллектуальные технологии
    "AI": "digital_intelligence",
    "Data": "digital_intelligence",
    "IT": "digital_intelligence",
    "Cyber": "digital_intelligence",
    "Robotics": "digital_intelligence",
    "Systems": "digital_intelligence",
    "Technology": "digital_intelligence",
    "Drones": "digital_intelligence",

    # 2) Наука, медицина и новые материалы
    "Science": "science_health_materials",
    "Innovation": "science_health_materials",
    "Biotech": "science_health_materials",
    "Materials": "science_health_materials",
    "Health": "science_health_materials",

    # 3) Устойчивая среда и природные ресурсы
    "Ecology": "sustainable_environment",
    "Energy": "sustainable_environment",
    "Water": "sustainable_environment",
    "Mining": "sustainable_environment",
    "Agriculture": "sustainable_environment",

    # 4) Инфраструктура, транспорт и промышленность
    "Industry": "infrastructure_transport_industry",
    "Construction": "infrastructure_transport_industry",
    "Infrastructure": "infrastructure_transport_industry",
    "Urban": "infrastructure_transport_industry",
    "Transport": "infrastructure_transport_industry",
    "Logistics": "infrastructure_transport_industry",
    "Aviation": "infrastructure_transport_industry",
    "Space": "infrastructure_transport_industry",

    # 5) Экономика, управление и рынок труда
    "Economy": "economy_management_work",
    "Management": "economy_management_work",
    "Work": "economy_management_work",
    "Career": "economy_management_work",
    "Safety": "economy_management_work",

    # 6) Человек, общество и креативные индустрии
    "Education": "human_society_creative",
    "Psychology": "human_society_creative",
    "Society": "human_society_creative",
    "Ethics": "human_society_creative",
    "Communication": "human_society_creative",
    "Media": "human_society_creative",
    "Culture": "human_society_creative",
    "Design": "human_society_creative",
    "Food": "human_society_creative",
    "Tourism": "human_society_creative",
}