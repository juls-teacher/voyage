from django.contrib import admin
from products.models import Product, Customer, Order, OrderItem, Address


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "description",)
    fields = ["title", "image", "price", "description",]
    readonly_fields = ()
    search_fields = ("title", "description")

    def save_form(self, request, form, change):
        return super().save_form(request, form, change)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "email",)
    fields = ["user", "name", "email",]
    readonly_fields = ()
    search_fields = ("user", "name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "date_ordered", "complete", "transaction_id",)
    fields = ["customer", "date_ordered", "complete", "transaction_id", ]
    readonly_fields = ("date_ordered",)
    search_fields = ("customer",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "order", "quantity", "date_added",)
    fields = ["product", "order", "quantity", "date_added", ]
    readonly_fields = ("date_added",)
    search_fields = ("product",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("customer", "order", "address", "city", "state", "zipcode", "date_added","phone_number",)
    fields = ["customer", "order", "address", "city", "state", "zipcode", "date_added", "phone_number",]
    readonly_fields = ("date_added",)
    search_fields = ("phone_number",)
