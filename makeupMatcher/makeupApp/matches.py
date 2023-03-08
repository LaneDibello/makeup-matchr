from makeupApp.models import Product
from django.db.models.query import QuerySet
from django.db.models import F


class Match:
    def __init__(self, red : int, green : int, blue : int):
        """
        Initializes a Match that takes integer RGB values as input, and generates a QuerySet of matches
        """
        self.red = red
        self.green = green
        self.blue = blue
        self.distance = ((F('red')-self.red)**2 + (F('green')-self.green)**2 + (F('blue')-self.blue)**2)


    def getMatches(self, rThresh : int = 3, gThresh : int = 3, bThresh : int = 3) -> QuerySet:
        """
        Returns a Django QuerySet of color matches within the passed threshhold (each threshold is 3 by default) 
        """
        return Product.objects.filter(
            red__range = ((self.red - rThresh), (self.red + rThresh)),
            green__range = ((self.green - gThresh), (self.green + gThresh)),
            blue__range = ((self.blue - bThresh), (self.blue + bThresh))
            ).annotate(distance=self.distance).order_by('distance')
    
    def getMatchesKNearest(self, count : int):
        """
        Returns a collection of `count` products ordered by their euclidean distance from the product's color
        """
        return Product.objects.annotate(distance=self.distance).order_by('distance')[:count]
    

