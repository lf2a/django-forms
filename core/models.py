from django.db import models
# SIGNALS
"""
https://docs.djangoproject.com/en/3.0/topics/signals/
https://docs.djangoproject.com/en/3.0/ref/signals/
"""
from django.db.models import signals
from django.template.defaultfilters import slugify
from stdimage.models import StdImageField


class Base(models.Model):
    criado = models.DateField('Data de criação', auto_now_add=True)
    modificado = models.DateField('Data de atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Produto(Base):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque')
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumb': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.nome


# vai ser executado quando salvar os dados da instancia Produto
def produto_pre_save(signal, instance, sender, **kwargs):
    # vai criar uma url com o nome do produto ex. Relogio Rolex -> relogio-rolex-123
    # esse valor vai ser salvo no atributo slug da classe Produto
    instance.slug = slugify(instance.nome)


# diz que o produto vai ser executado antes de salvar
signals.pre_save.connect(produto_pre_save, sender=Produto)
