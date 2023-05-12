# Имеется шаблон формы для фильтрации товаров на сайте:
#
# <form class="form" action="" method="get">
#     <div class="form-group">
#         <div class="range Section-columnRange">
#             <input class="range-line" id="price" name="price" type="text" data-type="double" data-min="7" data-max="50"
#                    data-from="7" data-to="27"/>
#             <div class="range-price">Цена:&#32;
#                 <div class="rangePrice">
#                 </div>
#             </div>
#         </div>
#     </div>
#     <div class="form-group">
#         <input class="form-input form-input_full" id="title" name="title" type="text" placeholder="Название"/>
#     </div>
#     <div class="form-group">
#         <!-- - var options = setOptions(items, ['value', 'selected', 'disabled']);-->
#     </div>
#     <div class="form-group">
#         <label class="toggle">
#             <input name="in_stock" type="checkbox"/><span class="toggle-box"></span><span class="toggle-text">Только товары в наличии</span>
#         </label>
#     </div>
#     <div class="form-group">
#         <label class="toggle">
#             <input name="free_shipping" type="checkbox"/><span class="toggle-box"></span><span class="toggle-text">С бесплатной доставкой</span>
#         </label>
#     </div>
#     <div class="form-group">
#         <div class="buttons"><a class="btn btn_square btn_dark btn_narrow" href="#">Фильтр</a>
#         </div>
#     </div>
# </form>
#
# Напишите класс представления на Django для фильтрации товаров на сайте для модели товаров по полям price, title,freeDelivery и in_stock:
#
# class Product(models.Model):  # товар
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Product category'))
#     price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_('Price'))
#     quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))
#     date = models.DateTimeField(auto_now_add=True, verbose_name=_('Created data'))
#     title = models.CharField(max_length=150, verbose_name=_('Title'))
#     fullDescription = models.TextField(max_length=100, verbose_name=_('Full description product'))
#     freeDelivery = models.BooleanField(default=False, verbose_name=_('Free shipping'))  # бесплатная доставка
#     tag = models.SlugField(max_length=200, db_index=True, verbose_name=_('Tag product'))
#     limited = models.BooleanField(default=False, verbose_name=_('Limited edition'))  # ограниченный тираж
#     banner = models.BooleanField(default=False, verbose_name=_('Banner on home page'))
#     brand = models.CharField(max_length=100, verbose_name=_('Brand'))
#     attributes = models.JSONField(default=dict, blank=True, verbose_name=_('Attributes'))
#     in_stock = models.BooleanField(default=True, verbose_name=_('In stock'))
#
# и приведите код html страницы
