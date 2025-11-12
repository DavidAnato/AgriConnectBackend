from decimal import Decimal
from django.contrib.auth import get_user_model
from app_products.models import Product  # adapte selon ton app

User = get_user_model()
producer = User.objects.get(id=3)

products_data = [
    {
        "name": "Igname",
        "unit_type": "kg",
        "unit_price": Decimal("900"),
        "quantity_available": Decimal("100"),
        "short_description": "Igname frais et ferme",
        "long_description": (
            "Igname cultivé dans la région de Kétou, Bénin. "
            "Parfait pour les plats traditionnels comme le foutou ou la pâte. "
            "Récolté à maturité pour conserver un goût sucré et une texture agréable."
        ),
        "location_commune": "Kétou",
        "location_village": "Agoué",
    },
    {
        "name": "Maïs",
        "unit_type": "kg",
        "unit_price": Decimal("450"),
        "quantity_available": Decimal("200"),
        "short_description": "Maïs biologique du Bénin",
        "long_description": (
            "Maïs cultivé dans la commune de Bohicon, localement. "
            "Idéal pour cuisson, égrenage ou farine. "
            "Récolte récente, grains sucrés et croquants, parfait pour l'alimentation familiale."
        ),
        "location_commune": "Bohicon",
        "location_village": "Hounnou",
    },
    {
        "name": "Légumes",
        "unit_type": "kg",
        "unit_price": Decimal("600"),
        "quantity_available": Decimal("150"),
        "short_description": "Assortiment de légumes frais",
        "long_description": (
            "Carottes, tomates, poivrons et autres légumes cultivés autour de Parakou. "
            "Tous cueillis le matin pour garantir fraîcheur et goût. "
            "Idéal pour salades, sauces et plats mijotés."
        ),
        "location_commune": "Parakou",
        "location_village": "Djougou",
    },
    {
        "name": "Riz",
        "unit_type": "kg",
        "unit_price": Decimal("1200"),
        "quantity_available": Decimal("80"),
        "short_description": "Riz blanc parfumé",
        "long_description": (
            "Riz produit à Banikoara, Bénin, grain long et parfumé. "
            "Parfait pour accompagner vos plats traditionnels ou modernes. "
            "Cultivé selon des méthodes locales respectueuses de l'environnement."
        ),
        "location_commune": "Banikoara",
        "location_village": "Sikki",
    },
    {
        "name": "Tomates",
        "unit_type": "kg",
        "unit_price": Decimal("650"),
        "quantity_available": Decimal("120"),
        "short_description": "Tomates rouges et juteuses",
        "long_description": (
            "Tomates locales cultivées autour de Ouidah, Bénin. "
            "Idéales pour salades, sauces et plats mijotés. "
            "Récoltées à maturité pour un goût sucré et une texture ferme."
        ),
        "location_commune": "Ouidah",
        "location_village": "Houéyogbé",
    },
    {
        "name": "Poivrons",
        "unit_type": "kg",
        "unit_price": Decimal("750"),
        "quantity_available": Decimal("90"),
        "short_description": "Poivrons colorés frais",
        "long_description": (
            "Poivrons verts, rouges et jaunes cultivés à Abomey-Calavi. "
            "Idéal pour cuisiner et garnir vos plats. "
            "Récolte du jour pour garantir une saveur optimale et un croquant naturel."
        ),
        "location_commune": "Abomey-Calavi",
        "location_village": "Godomey",
    },
    {
        "name": "Carottes",
        "unit_type": "kg",
        "unit_price": Decimal("500"),
        "quantity_available": Decimal("70"),
        "short_description": "Carottes croquantes",
        "long_description": (
            "Carottes cultivées autour de Parakou, Bénin, riches en vitamines. "
            "Parfaites pour les salades, jus ou plats mijotés. "
            "Récoltées fraîches, elles conservent saveur et texture."
        ),
        "location_commune": "Parakou",
        "location_village": "Gnonkourakali",
    },
    {
        "name": "Oignons",
        "unit_type": "kg",
        "unit_price": Decimal("400"),
        "quantity_available": Decimal("180"),
        "short_description": "Oignons savoureux",
        "long_description": (
            "Oignons rouges et blancs cultivés autour de Dassa-Zoumé. "
            "Parfaits pour assaisonner tous types de plats locaux ou modernes. "
            "Récolte récente pour garantir un goût prononcé et durable."
        ),
        "location_commune": "Dassa-Zoumé",
        "location_village": "Paouignan",
    },
    {
        "name": "Patates douces",
        "unit_type": "kg",
        "unit_price": Decimal("600"),
        "quantity_available": Decimal("130"),
        "short_description": "Patates douces sucrées",
        "long_description": (
            "Patates douces cultivées à Kandi, Bénin, sucrées et savoureuses. "
            "Parfaites pour friture, cuisson ou purée. "
            "Récolte du jour pour garantir fraîcheur et goût."
        ),
        "location_commune": "Kandi",
        "location_village": "Segbana",
    },
    {
        "name": "Bananes",
        "unit_type": "kg",
        "unit_price": Decimal("500"),
        "quantity_available": Decimal("100"),
        "short_description": "Bananes mûres et savoureuses",
        "long_description": (
            "Bananes cultivées localement à Lokossa, Bénin. "
            "Parfaites pour consommation directe, smoothie ou dessert. "
            "Récoltées à maturité pour un goût sucré et parfumé."
        ),
        "location_commune": "Lokossa",
        "location_village": "Hogbonou",
    },
]

for data in products_data:
    Product.objects.create(
        name=data["name"],
        unit_type=data["unit_type"],
        unit_price=data["unit_price"],
        quantity_available=data["quantity_available"],
        producer=producer,
        short_description=data["short_description"],
        long_description=data["long_description"],
        location_village=data["location_village"],
        location_commune=data["location_commune"],
        is_published=True,
    )

print("10 produits réalistes créés avec localisation béninoise et descriptions longues !")
