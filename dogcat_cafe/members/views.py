from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm,LoginForm,UserProfileForm

from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.views import LoginView

from django.http import JsonResponse
from django.views import View
from .models import *

from django.contrib import messages
from django.core.mail import send_mail

from django.db.models import Q



def is_active_and_not_superuser(user):
    return user.is_active and not user.is_superuser and not user.is_staff

def is_login(user):
    return not user.is_active and not user.is_superuser and not user.is_staff


def home(request):
    suggested_foods = Food.objects.filter(stock=True, suggested=True)
    news = New.objects.filter(display=True)
    return render(request, "home.html",{'suggested_foods': suggested_foods,'news':news})

@user_passes_test(is_login, login_url='/')
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            subject = 'ยืนยันการลงทะเบียน'
            message = f'ยินดีต้อนรับ \n\n คุณ{user.first_name} {user.last_name} \n\n ชื่อผู้ใช้ของคุณ: {user.username}!'
            from_email = 'หมาแมวคาเฟ่@Dogcat.com'
            recipient_list = [user.email]
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "members/register.html", {"form": form})



@user_passes_test(is_active_and_not_superuser, login_url='/')
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'members/edit_profile.html', {'form': form})

@user_passes_test(is_login, login_url='/')
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user=user)
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, "members/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')



def food_list(request):
    foods = Food.objects.all()
    return render(request,'members/food.html',{'foods':foods})


class CalendarEvents(View):
    def get(self, request, *args, **kwargs):
        events = []
        pets = Pet.objects.all()

        for pet in pets:
            events.append({
                'id':pet.id,
                'title': pet.name,
                'start': pet.date_time.isoformat(),
                'image': pet.profile.url if pet.profile else None,
            })

        return JsonResponse(events, safe=False)
    

def pets(request,id):
    pets = Pet.objects.get(pk=id)
    return render(request,'members/pets.html',{'pets':pets})

@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/admin')
def dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request,'members/dashboard.html',{'user_profile':user_profile})


@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def add_to_cart(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, food=food)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    cart_item.calculate_total_price()
    cart.calculate_total_price()

    messages.success(request, f'เพิ่ม {food.name} ลงในตะกร้าแล้ว')
    return redirect('cart_detail')

@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def decrease_quantity(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, food=food)

    cart_item.decrease_quantity()
    cart_item.calculate_total_price()

    cart.calculate_total_price()

    return redirect('cart_detail')

@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def increase_quantity(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, food=food)

    cart_item.increase_quantity()
    cart_item.calculate_total_price()

    cart.calculate_total_price()

    return redirect('cart_detail')

@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def remove_from_cart(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, food=food)

    # ลบ CartItem ออกจากตะกร้า
    cart_item.remove_from_cart()

    # คำนวณราคารวมใหม่ของ Cart
    cart.calculate_total_price()

    return redirect('cart_detail')


@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def cart_detail(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        cart_items = cart.cartitem_set.all()

        total_price_cart = sum(cart_item.total_price for cart_item in cart_items)


        return render(request, 'members/cart_detail.html', {'cart_items': cart_items, 'total_price_cart': total_price_cart})
    except Cart.DoesNotExist:
        return render(request, 'members/cart_detail.html', {})
    


@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def create_order(request):
    user = request.user
    cart = Cart.objects.get(user=user)

    items_str = "\n".join([f"{item.food.name} - จำนวน: {item.quantity} จานละ: {item.food.price}" for item in cart.cartitem_set.all()])

    total_p = sum(item.total_price for item in cart.cartitem_set.all())
    
    order = Order.objects.create(user=user, cart=cart, total_price=total_p,items=items_str)

    
    cart.save()
    

    return redirect('send_order_email')


@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def send_order_email(request):
    user = request.user
    cart = Cart.objects.get(user=user)

    user_order = Order.objects.filter(user=request.user, is_cancelled=False, is_paid=False).latest('id')
    total = user_order.total_price
    items = "\n".join([f"{item.food.name} - จำนวน: {item.quantity} ราคา: {item.food.price * item.quantity}" for item in user_order.cart.cartitem_set.all()])
    subject = 'ยืนยันคำสั่งซื้อ'
    message = f'ขอบคณสำหรับการสั่งซื้อ\n\nรายการสินค้า:\n\n{items}\n\nรวม: {total} บาท\n\n'
    recipient_list = [request.user.email]
    from_email = 'หมาแมวคาเฟ่@Dogcat.com'
    send_mail(subject, message, from_email, recipient_list)
    cart.cartitem_set.all().delete()

    return redirect('order')


@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def order_detail(request):

    user_orders = Order.objects.filter(user=request.user,is_cancelled=False,is_paid=False).order_by('-id')
    total = sum(i.total_price for i in user_orders.all())

    return render(request, 'members/order_detail.html', {'orders': user_orders,'total':total})


@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def order_detail(request):

    user_orders = Order.objects.filter(user=request.user,is_cancelled=False,is_paid=False).order_by('-id')
    total = sum(i.total_price for i in user_orders.all())

    return render(request, 'members/order_detail.html', {'orders': user_orders,'total':total})


@login_required(login_url='login')
@user_passes_test(is_active_and_not_superuser, login_url='/')
def order_history(request):

    user_orders_cancel = Order.objects.filter(user=request.user, is_cancelled=True)
    total_cancel = (sum(i.total_price for i in user_orders_cancel.all()))


    user_orders = Order.objects.filter(Q(user=request.user, is_cancelled=True, is_paid=False) | Q(user=request.user, is_paid=True, is_cancelled=False)).order_by('-id')    
    total = (sum(i.total_price for i in user_orders.all())) - total_cancel

    return render(request, 'members/order_history.html', {'orders': user_orders,'total':total})


