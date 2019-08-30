from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.views.generic.list import BaseListView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem

from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.db import transaction

from ordersapp.forms import OrderItemForm
from django.forms import inlineformset_factory


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        # пришел гет запрос
        print('kwargs', kwargs)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        # возвращает словарь с данными
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Список заказов'
        return context

    # def get_template_names(self):
    #     # возвращает шаблон который мы редактируем
    #     if self.request.user.is_staff:
    #         return 'staff.html'
    #     else:
    #         return 'other.html'

    # Изменяем свойства класса
    # 1. имя шаблона
    template_name = 'order_list.html'
    # 2. название списка в шаблоне
    # context_object_name = 'orders'

    # Изменяем методы класса
    # ------------- Основные методы -----------------
    """

    dispatch()
    # итоговый список
    get_queryset()
    get_context_data()
    get()

    """
    # ------------- Другие методы -------------------
    """
    get_template_names()
    setup()
    http_method_not_allowed()
    get_context_object_name()
    render_to_response()
    """


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')
    template_name = 'order_form.html'

    """
    Основные методы
    post() # пришел post запрос
    form_valid() # после валидации формы
    form_invalid() # если форма не валидна
    """

    def get_context_data(self, **kwargs):

        """
        Передача данных в шаблон
        :param kwargs:
        :return:
        """
        # Получаем словарь по умолчаню
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        # Создаем нужный набор форм
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=2)

        if self.request.POST:
            # сохранение данных
            # заполняем данными набор форм
            formset = OrderFormSet(self.request.POST)
        else:
            # если выводим форму
            # получаем данные из корзины
            basket_items = Basket.get_items(self.request.user)
            # если они есть
            if len(basket_items):
                # создаем набор форм длиной как в корзине
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                # создаем его экземпляр
                formset = OrderFormSet()
                # сохраняем данные корзины
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):

        """форма валидна"""
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            # сохраняем заказ
            self.object = form.save()
            if orderitems.is_valid():
                # добавляем к items заказ
                orderitems.instance = self.object
                # сохраняем сразу все
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context

    # get_queryset - ???

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    # Основной метод это
    # def get_object(self, queryset=None):
    #     """
    #     Возвращает нужный нам объект
    #     :param queryset:
    #     :return:
    #     """
    #     return 'Мой объект'


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            data['orderitems'] = OrderFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))

