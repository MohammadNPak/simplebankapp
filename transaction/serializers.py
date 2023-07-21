from rest_framework import serializers
from .models import Transaction,Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()  # Add the 'id' field to the serializer
    Date = serializers.ReadOnlyField()
    Type = serializers.CharField(write_only=True)
    Category = serializers.SlugRelatedField(slug_field='name',queryset=Category.objects.all())

    class Meta:
        model = Transaction
        exclude = ['user']

    def create(self, validated_data):
        # Set the user to the authenticated user before creating the transaction
        user = self.context['request'].user
        return Transaction.objects.create(user=user, **validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['Type'] = 'Income' if instance.Type == 'I' else 'Expense'
        return representation

    def to_internal_value(self, data):
        type_str = data.get('Type', None)
        if type_str:
            if type_str == 'Income':
                data['Type'] = 'I'
            elif type_str == 'Expense':
                data['Type'] = 'E'
            else:
                raise serializers.ValidationError("Invalid type value. Must be 'Income' or 'Expense'.")
        return super().to_internal_value(data)
