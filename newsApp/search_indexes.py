from haystack import indexes
from .models import MyNews


class MyNewIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return MyNews

    def index_query(self, using=None):
        return self.get_model().objects.all()
