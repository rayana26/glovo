from .models import (UserProfile, Courier, Contact, Category,Product,Review,Address,Store,Order)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ('username', 'email', 'password', 'first_name', 'last_name')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = UserProfile.objects.create_user(**validated_data)
    return user

  def to_representation(self, instance):
    refresh = RefreshToken.for_user(instance)
    return {
      'user': {
        'username': instance.username,
        'email': instance.email,
      },
      'access': str(refresh.access_token),
      'refresh': str(refresh),
    }


class UserLoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Неверные учетные данные")

  def to_representation(self, instance):
    refresh = RefreshToken.for_user(instance)
    return {
      'user': {
        'username': instance.username,
        'email': instance.email,
      },
      'access': str(refresh.access_token),
      'refresh': str(refresh),
    }


class UserProfileListSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['username', 'email', 'password']


class UserProfileDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = '__all__'

class UserProfileNameSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['username']

class CourierSerializers(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['user','courier_status']

class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['contact_number']

class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_name']

class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name']

class ProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','product_name']

class ProductCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializers(serializers.ModelSerializer):
    courier_assignments = CourierSerializers(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['client','courier','courier_assignments']

class ProductDetailSerializers(serializers.ModelSerializer):
    product_order = OrderSerializers(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['product_name','product_img','product_description','product_order']


class StoreListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id','store_name','store_img']

class StoreDetailSerializers(serializers.ModelSerializer):
    product_store = ProductListSerializers(many=True, read_only=True)
    store_contact = ContactSerializers(many=True, read_only=True)
    address_store = AddressSerializers(many=True, read_only=True)
    store_contact = serializers.CharField()
    class Meta:
        model = Store
        fields = ['product_store','store_name','store_img','descriptions','owner','created_date', 'store_contact','address_store',
            ]


class CategoryDetailSerializers(serializers.ModelSerializer):
    category_store = StoreListSerializers(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['category_name','category_store']


class ReviewSerializer(serializers.ModelSerializer):
  created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%H')
  client = UserProfileNameSerializer()
  class Meta:
    model = Review
    fields = ['client', 'text', 'rating', 'created_date']

class ReviewCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = '__all__'

