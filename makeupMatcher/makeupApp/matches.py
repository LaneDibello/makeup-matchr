from makeupApp.models import Product
from django.db.models.query import QuerySet

class Match:
    def __init__(self, red : int, green : int, blue : int):
        """
        Initializes a Match that takes integer RGB values as input, and generates a QuerySet of matches
        """
        self.red = red
        self.green = green
        self.blue = blue

    def getMatches(rThresh : int = 3, gThresh : int = 3, bThresh : int = 3) -> QuerySet:
        """
        Returns a Django QuerySet of color matches within the passed thresh hold (each threshold is 3 by default) 
        """
        return Product.objects.filter(
            red__range = ((red - rThresh), (red + rThresh)),
            green__range = ((green - gThresh), (green + gThresh)),
            blue__range = ((blue - bThresh), (blue + bThresh))
            )
