from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView
from ordersapp.models import Order


# Для Class-Based View
# задаётся шаблон по умолчанию: его название = "НазваниеМодели"_list.html (название модели во вьюхе)
# переменная в шаблоне по умолчанию называется {% object_list %} - это список всех заказов
# ===== Изменяем свойства класса ======
# 1) Имя шаблона.
# По умолчанию во вьюъе указывается модель - "model = Order" - это и становится "якорем" для поиска
# Класс может наследоваться, например, от (ListView) - имя шаблона будет order_list.html,
# или от (DetailView) - тогда имя шаблона строится как order_detail.html. Эти правила скрыты в родительском классе.
# (template_name_suffix в классе BaseListView, например)
# Переменная template_name = 'MyTemplate' / При этом Джанго все равно будет искать по стандартному имени шаблона
# 2) Изменить название списка в шаблоне.
# context_object_name = 'Orders' / Джанго в шаблоне будет так же искать сперва по этой переменной, потом по стандартной
#
#
# =================== МЕТОДЫ КЛАССА, КОТОРЫЕ БУДЕМ ИЗМЕНЯТЬ ============================
# _______________________________Основные________________________________
# dispatch()
# get_context_data()
# get()
#
# vvv____Итоговый список:____vvv
# его содержимое передается в object_list вьюхи
# get_queryset()


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # - мы переопределили метод, добавив фильтр по пользователю

    #       (чтобы на странице не выпадали сразу все заказы всех пользователей)
    # vvv____Дополнительные данные (помимо итогового списка):____vvv
    def get_context_data(self, *args, **kwargs):
        # этот метод возвращает словарь с данными
        context = super().get_context_data(*args, **kwargs)  # <= тут обычно только 1 переменная (object_list)
        context['page_title'] = 'Список заказов'  # {{page_title}} для вывода на страницу доп. инфы
        return context

    # vvv____В метод get приходит get-request____vvv:
    def get(self, *args, **kwargs):
        print('kwargs', kwargs)  # в kwargs влетает гет-запрос
        return super().get(self, *args, **kwargs)

    # vvv____Возвращение шаблона, который мы редактируем____vvv:
    def get_template_names(self):
        if self.request.user.is_staff:
            return 'staff.html'
        else:
            return 'other.html'


class OrderRead(DetailView):  # - DetailView - класс для просмотра конкретного заказа
    model = Order

    # ОСНОВНОЙ МЕТОД КЛАССА:
    def get_object(self, queryset=None):  # - отрабатывает путем выборки из get_queryset, что логично.

        return 'Отдельный объект'

    def get_context_data(self, **kwargs):  # - дополнительно в классе переопределен метод, чтобы вывести title
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDelete(DeleteView):  # - DeleteView - ну тут все вроде понятно
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    def order_forming_complete(request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.SENT_TO_PROCEED
        order.save()

        return HttpResponseRedirect(reverse('ordersapp:orders_list'))


# _____________________________Дополнительные______________________________
# setup()
# get_context_object_name()
# http_method_not_allowed()
# render_to_response()
# get_template_names()
# get_slug_field()
# get_object()
#
#
#
#
#
