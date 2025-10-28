import re
from datetime import datetime
from django.db import transaction
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order

# -------------------
# TYPES
# -------------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

# Node type for filtering
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filter_fields = ['name', 'email']
        interfaces = (graphene.relay.Node,)

# -------------------
# MUTATIONS
# -------------------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists.")
        if phone and not re.match(r"^\+?\d[\d\-]{7,14}$", phone):
            raise Exception("Invalid phone number format.")
        customer = Customer.objects.create(name=name, email=email, phone=phone)
        return CreateCustomer(customer=customer, message="Customer created successfully.")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(graphene.JSONString, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created_customers = []
        errors = []
        for entry in input:
            name = entry.get("name")
            email = entry.get("email")
            phone = entry.get("phone")
            if not name or not email:
                errors.append(f"Missing fields for {entry}")
                continue
            if Customer.objects.filter(email=email).exists():
                errors.append(f"Email {email} already exists.")
                continue
            customer = Customer.objects.create(name=name, email=email, phone=phone)
            created_customers.append(customer)
        return BulkCreateCustomers(customers=created_customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(required=False)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive.")
        if stock < 0:
            raise Exception("Stock cannot be negative.")
        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID.")

        products = Product.objects.filter(pk__in=product_ids)
        if not products:
            raise Exception("Invalid product IDs.")

        total = sum([p.price for p in products])
        order = Order.objects.create(customer=customer, total_amount=total)
        order.products.set(products)
        order.save()

        return CreateOrder(order=order)

# -------------------
# ROOT QUERY
# -------------------
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    # Added filtered connection field
    filtered_customers = DjangoFilterConnectionField(CustomerNode)

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()

# -------------------
# ROOT MUTATION
# -------------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


class UpdateLowStockProducts(graphene.Mutation):
    success = graphene.String()
    updated = graphene.List(graphene.String)

    def mutate(self, info):
        updated = []
        for p in Product.objects.filter(stock__lt=10):
            p.stock += 10
            p.save()
            updated.append(p.name)
        return UpdateLowStockProducts(success="Products updated", updated=updated)