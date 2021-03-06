from rest_framework import serializers
from myuser.models import MyUser
from shop.models import Product, Order, Return


SEX = [(1, "female"), (2, "male"), (3, "unknown")]
ENGLISH_LEVEL = [(1, "A1"), (2, "A2"), (3, "B1"), (4, "B2"), (5, "C1"), (6, "C2")]


class Task1Serializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    sex = serializers.ChoiceField(choices=SEX, default=3)
    age = serializers.IntegerField(min_value=18, max_value=100)
    english_level = serializers.ChoiceField(choices=ENGLISH_LEVEL, default=1)

    def validate(self, attrs):
        sex = attrs.get("sex")
        age = attrs.get("age")
        english_level = attrs.get("english_level")
        condition1 = all([int(sex) == 1, age > 22, int(english_level) > 3])
        condition2 = all([int(sex) == 2, age >= 20, int(english_level) > 3])
        if not condition1 and not condition2:
            raise serializers.ValidationError("Ne")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ["id", "username", "password"]


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "cost", "amount"]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Order
        fields = ["user", "product", "amount", "create_date"]

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data.pop("user"))
        product = Product.objects.create(**validated_data.pop("product"))
        return Order.objects.create(user=user, product=product, **validated_data)


class SimpleOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    create_date = serializers.DateTimeField(read_only=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invalid amount")
        return value


    class Meta:
        model = Order
        fields = ["id", "product", "amount", "create_date"]


class UserWithOrdersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    orders = SimpleOrderSerializer(many=True)

    def create(self, validated_data):
        orders = validated_data.pop("orders")
        user = MyUser.objects.create_user(**validated_data)
        for elem in orders:
            Order.objects.create(user=user, **elem)
        return user

    class Meta:
        model = MyUser
        fields = ["username", "password", "orders"]


class ReturnSerializer(serializers.ModelSerializer):
    create_date = serializers.DateField(read_only=True)

    class Meta:
        model = Return
        fields = ["order", "create_date"]


class ExpireTokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["key", ""]


