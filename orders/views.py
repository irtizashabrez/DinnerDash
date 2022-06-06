from django.shortcuts import redirect, render
from django.views import View
from orders.models import *
from orders.form import *
from authentications.models import *
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                full_total = 0
                item_session = request.session['item']
                user_id = request.user
                check_cart = Order.objects.filter(
                    user_id=user_id, status='Pending').first()
                if check_cart == None:
                    check_cart = Order.objects.create(user_id=user_id)
                    # loop
                    for key, value in item_session.items():
                        new_item = Item.objects.get(title=key)
                        cart_item = OrderItem.objects.create(
                            order_id=check_cart,
                            item_id=new_item,
                            quantity=item_session[key]['quantity']
                        )
                        full_total += item_session[key]['quantity'] * \
                            item_session[key]['price']
                        cart_item.save()
                else:
                    for key, value in item_session.items():
                        new_item = Item.objects.get(title=key)
                        cart_item = OrderItem.objects.filter(
                            order_id=check_cart.id, item_id=new_item).first()
                        if cart_item == None:
                            cart_item = OrderItem.objects.create(
                                order_id=check_cart,
                                item_id=new_item,
                                quantity=1
                            )
                            cart_item.save()
                            full_total += new_item.price
                        else:
                            cart_item.quantity += item_session[key]['quantity']
                            full_total += cart_item.quantity * \
                                item_session[key]['price']
                            cart_item.save()
                check_cart.total = full_total
                check_cart.save()
                del request.session['item']
            except:
                pass

            user_id = request.user
            check_cart = Order.objects.filter(
                user_id=user_id, status='Pending').first()
            if check_cart == None or check_cart.total == 0:
                return render(request, 'orders/cart.html', {'cart_item': check_cart})
            cart_item = OrderItem.objects.filter(
                order_id=check_cart.id)
            context = {'cart_item': cart_item, 'total_price': check_cart.total}
            return render(request, 'orders/cart.html', context)
        else:
            try:
                item_session = request.session['item']
                total = 0
                # "=== My Cart Start ==="
                for key, value in item_session.items():
                    total += item_session[key]['price']
                # "=== My Cart End ==="
                context = {'item_session': item_session, 'total_price': total}
                return render(request, 'orders/cartunauth.html', context)

            except:
                print("if no session show empty")
            return render(request, 'orders/cart.html')


def add_to_cart(request, pk):

    try:
        item = Item.objects.get(id=pk, status='Available')
    except:
        item = None

    if not item:
        return render(request, 'noitem.html')

    if request.user.is_authenticated:
        try:
            item_session = request.session['item']
            user_id = request.user
            check_cart = Order.objects.filter(
                user_id=user_id, status='Pending').first()
            if check_cart == None:
                check_cart = Order.objects.create(user_id=user_id)
                # new item added into item_session
                title = item.title
                if title in item_session:
                    item_session[title]['quantity'] += 1
                    item_session[title]['item_total'] = item_session[title]['price'] * \
                        item_session[title]['quantity']
                else:
                    item_session1 = {}
                    item_session1[title] = {}
                    item_session1[title]['price'] = item.price
                    item_session1[title]['quantity'] = 1
                    item_session1[title]['item_total'] = item.price
                    item_session1[title]['image'] = item.photo.url
                    item_session.update(item_session1)
                # loop
                for key, value in item_session.items():
                    new_item = Item.objects.get(title=key)
                    cart_item = OrderItem.objects.create(
                        order_id=check_cart,
                        item_id=new_item,
                        quantity=item_session[key]['quantity']
                    )
                    cart_item.save()
                check_cart.save()
            else:
                for key, value in item_session.items():
                    new_item = Item.objects.get(title=key)
                    cart_item = OrderItem.objects.filter(
                        order_id=check_cart.id, item_id=new_item).first()
                    if cart_item == None:
                        cart_item = OrderItem.objects.create(
                            order_id=check_cart,
                            item_id=new_item,
                            quantity=1
                        )
                        cart_item.save()
                    else:
                        cart_item.quantity += item_session[key]['quantity']
                        cart_item.save()

            del request.session['item']
        except:
            user_id = request.user
            check_cart = Order.objects.filter(
                user_id=user_id, status='Pending').first()
            if check_cart == None:
                check_cart = Order.objects.create(user_id=user_id)
                cart_item = OrderItem.objects.create(
                    order_id=check_cart,
                    item_id=item,
                    quantity=1
                )
                check_cart.save()
                cart_item.save()
            else:
                cart_item = OrderItem.objects.filter(
                    order_id=check_cart.id, item_id=item).first()
                if cart_item == None:
                    cart_item = OrderItem.objects.create(
                        order_id=check_cart,
                        item_id=item,
                        quantity=1
                    )
                    cart_item.save()
                else:
                    cart_item.quantity += 1
                    cart_item.save()
        cart_item = OrderItem.objects.filter(
            order_id=check_cart.id)
        sub_total = 0

        for i in cart_item:
            sub_total = (i.item_id.price * i.quantity) + sub_total

        check_cart.total = sub_total
        check_cart.save()
    else:
        try:
            item_session = request.session['item']
            title = item.title
            if title in item_session:
                item_session[title]['quantity'] += 1
                item_session[title]['item_total'] = item_session[title]['price'] * \
                    item_session[title]['quantity']
            else:
                item_session1 = {}
                item_session1[title] = {}
                item_session1[title]['price'] = item.price
                item_session1[title]['quantity'] = 1
                item_session1[title]['item_total'] = item.price
                item_session1[title]['image'] = item.photo.url

                item_session.update(item_session1)
            request.session['item'] = item_session

        except:
            # "========create new======"
            request.session['item'] = {}
            title = item.title
            item_session = {}
            item_session[title] = {}
            item_session[title]['price'] = item.price
            item_session[title]['quantity'] = 1
            item_session[title]['item_total'] = item.price
            item_session[title]['image'] = item.photo.url
            request.session['item'] = item_session

    return redirect('home')


def add_item_quantity(request, pk):

    if request.user.is_authenticated:
        user_id = request.user
        check_cart = Order.objects.filter(
            user_id=user_id, status='Pending').first()
        cart_item = OrderItem.objects.filter(
            order_id=check_cart.id, id=pk).first()
        cart_item.quantity += 1
        cart_item.save()
        cart_item = OrderItem.objects.filter(
            order_id=check_cart.id)
        sub_total = 0

        for i in cart_item:
            sub_total = (i.item_id.price * i.quantity) + sub_total
        check_cart.total = sub_total
        check_cart.save()
    return redirect('cart')


def add_item_quantity_session(request, pk):

    if not request.user.is_authenticated:
        try:
            item_session = request.session['item']
            if pk in item_session:
                item_session[pk]['quantity'] += 1
                item_session[pk]['item_total'] = item_session[pk]['price'] * \
                    item_session[pk]['quantity']
                request.session['item'] = item_session
        except:
            pass
    return redirect('cart')


def minus_item_quantity_session(request, pk):

    if not request.user.is_authenticated:
        try:
            item_session = request.session['item']
            if pk in item_session:
                item_session[pk]['quantity'] -= 1
                if item_session[pk]['quantity'] <= 0:
                    del item_session[pk]
                else:
                    item_session[pk]['item_total'] = item_session[pk]['price'] * \
                        item_session[pk]['quantity']
                request.session['item'] = item_session
        except:
            pass
    return redirect('cart')


def minus_item_quantity(request, pk):

    if request.user.is_authenticated:
        user_id = request.user
        check_cart = Order.objects.filter(
            user_id=user_id, status='Pending').first()
        cart_item = OrderItem.objects.filter(
            order_id=check_cart.id, id=pk).first()
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        cart_item = OrderItem.objects.filter(
            order_id=check_cart.id)
        sub_total = 0
        for i in cart_item:
            sub_total = (i.item_id.price * i.quantity) + sub_total
        check_cart.total = sub_total
        check_cart.save()
    return redirect('cart')


def remove_item_cart(request, pk):
    if request.user.is_authenticated:
        user_id = request.user
        check_cart = Order.objects.filter(
            user_id=user_id, status='Pending').first()

        cart_item = OrderItem.objects.filter(
            order_id=check_cart.id, id=pk).first()

        cart_item.delete()
        cart_item = OrderItem.objects.filter(
            order_id=check_cart.id)
        sub_total = 0
        for i in cart_item:
            sub_total = (i.item_id.price * i.quantity) + sub_total
        check_cart.total = sub_total
        check_cart.save()
    return redirect('cart')


def remove_item_cart_session(request, pk):
    if not request.user.is_authenticated:
        try:
            item_session = request.session['item']
        except:
            return redirect('cart')
        del item_session[pk]
        request.session['item'] = item_session
    return redirect('cart')


class DashBoardView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        if request.user.is_admin:
            if request.GET.get('q') != None:
                order_status = request.GET.get('q')
                orders = Order.objects.filter(status=order_status)
            else:
                orders = Order.objects.exclude(status='Pending')

            customer = MyUser.object.exclude(admin=True)
            total_order = len(
                Order.objects.exclude(status='Pending'))
            orders_paid = len(Order.objects.exclude(status='Pending').exclude(
                status='Ordered').exclude(status='Completed').exclude(status='Cancelled'))
            orders_cancle = len(Order.objects.exclude(status='Pending').exclude(
                status='Ordered').exclude(status='Completed').exclude(status='Paid'))
            orders_complete = len(Order.objects.exclude(status='Pending').exclude(
                status='Ordered').exclude(status='Cancelled').exclude(status='Paid'))
            orders_ordered = len(Order.objects.exclude(status='Pending').exclude(
                status='Completed').exclude(status='Cancelled').exclude(status='Paid'))
            context = {'customers': customer,
                       'orders': orders, 'total_order': total_order, 'orders_paid': orders_paid,
                       'orders_cancle': orders_cancle, 'orders_complete': orders_complete,
                       'orders_ordered': orders_ordered
                       }
            return render(request, 'orders/dashboard.html', context)
        else:
            return render(request, 'error.html')


class UpdateOrderStatus(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'orders.change_order'
    model = Order
    fields = ['status']
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id=self.kwargs.get('pk'))
        except:
            order = None
        if order == None or order.status == 'Completed':
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_admin:
            return render(self.request, 'error.html')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard')


class CheckOutView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        user_id = request.user
        check_cart = Order.objects.filter(
            user_id=user_id, status='Pending').exclude(total=0).first()
        check_cart.status = 'Ordered'
        check_cart.save()
        return redirect('home')


class DasboardPastOrder(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, pk):
        if request.user.is_admin:
            user = MyUser.object.filter(id=pk).first()
            recent_order = Order.objects.filter(
                user_id=user.id).exclude(status='Pending')
            context = {'user': user, 'recent_order': recent_order}
            return render(request, 'orders/dashboardpastorder.html', context)
        else:
            return render(request, 'error.html')


class DashboardPastOrderDetail(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, pk, val1):
        if request.user.is_admin:
            cart_item = OrderItem.objects.filter(
                order_id=pk)
            context = {'cart_item': cart_item, 'user': val1}
            return render(request, 'orders/dashboardpastorderdetail.html', context)
        else:
            return render(request, 'error.html')


class DashboardOrderDetail(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, pk):
        if request.user.is_admin:
            cart_item = OrderItem.objects.filter(
                order_id=pk)
            context = {'cart_item': cart_item}
            return render(request, 'orders/dashboardorderdetail.html', context)
        else:
            return render(request, 'error.html')


class PastOrderView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        user = request.user
        recent_order = Order.objects.filter(
            user_id=user).exclude(status='Pending')
        context = {'user': user, 'recent_order': recent_order}
        return render(request, 'orders/pastorder.html', context)


class PastOrderDetail(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, pk):
        cart_item = OrderItem.objects.filter(
            order_id=pk)
        context = {'cart_item': cart_item}
        return render(request, 'orders/pastorderview.html', context)
