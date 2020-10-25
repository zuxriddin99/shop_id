from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """
        savatga jonatish

        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        savatdagi narsalarni tekshiish va ma'lumotlar bazasidan olish

        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)  # maxsulotlarni savatga qoshish
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        savatdagi barcha narsalarni sanaydi
        """

        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        obshi ssummani isoplidi.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        """
        savatni  butunlay tozalash
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def add(self, product, quantity=1, update_quantity=False):
        """
        savatga ma'lumot qoshish va uni yangilash
        """
        product_id = str(product.id)

        if product_id not in str(self.cart):
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # savat sesiyasini yangilash
        self.session[settings.CART_SESSION_ID] = self.cart
        # ozgariwni tasdiqlash
        self.session.modified = True

    def remove(self, product):
        """
        tavorlarni o'chirish
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
