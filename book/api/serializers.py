from rest_framework import serializers
from book.models import Book, Category, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        # exclude = ['book']

class ReviewSerializerWithoutBook(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ['book']
    

class BookSerializer(serializers.ModelSerializer):
    # len_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = "__all__" 
        # fields = ["id","name","description"]
        # exclude = ["id"]

    # def get_len_name(self, obj):
    #     return len(obj.name)

    
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and Description can not be same!")
    #     return data
    
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")        
    #     return value

class CategorySerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    # books = serializers.StringRelatedField(many=True)
    # books = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # books = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='book_detail')
    
    class Meta:
        model = Category
        fields = "__all__"