from django.shortcuts import render

from django.views.generic import ListView, DetailView, TemplateView

from store.models import Category, Product, ProductImages, Banner


class HomeListView(TemplateView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('-id')
        categories = Category.objects.all().order_by('-id')
        banners = Banner.objects.filter(is_active=True).order_by('-id')[0:3]
        context = {
            'products': products,
            'banners': banners,
            'categories': categories

        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        if request.method =='post' or request.method =='POST':
            search_product = request.POST.get('search_product')
            products = Product.objects.filter(name__icontains=search_product).order_by('-id')

            context = {
                'products': products,

            }
            return render(request, 'index.html', context)

    # model = Product
    # template_name = 'index.html'
    # context_object_name = 'products'
    #
    # def get_context_data(self, *args,**kwargs): ##cmt
    #     context = super().get_context_data(*args,**kwargs)
    #     context['banners'] = Banner.objects.filter(is_active=True).order_by('-id')[0:3]
    #     return context

    def valid_form(self, form):
        return super().valid_form(form)

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['product_tshirt'] = Product.objects.filter(category__name='tshirt')
        context['product_blazers'] = Product.objects.filter(category__name='blazers')
        context['product_jacket'] = Product.objects.filter(category__name='jacket')
        context['product_kids'] = Product.objects.filter(category__name='kids')
        context['product_sunglass'] = Product.objects.filter(category__name='sunglass')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-details.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images']=ProductImages.objects.filter(product=self.object.id)
        return context

# def product_details(request, pk):
#     item = Product.objects.get(id=pk)
#     photo = ProductImages.object
#     categories = Category.objects.all()
#     context = {
#         'item': item,
#         'categories': categories,
#     }
#     return render(request, 'product-details.html', context)