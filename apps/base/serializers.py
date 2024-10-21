from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.base.models import (
     Banner, FAQ, AboutApp, Support, Ad, VersionControl, PrivacyPolicy, OfferAgreement
)



class BannerListSerializer(ModelSerializer):

    class Meta:
        model = Banner
        fields = ('pk', 'title', 'sub_title', 'description', 'url', 'image')


class BannerDetailSerializer(ModelSerializer):

    class Meta:
        model = Banner
        fields = ('pk', 'title', 'sub_title', 'description', 'url', 'image')


class AboutAppSerializer(ModelSerializer):

    class Meta:
        model = AboutApp
        fields = '__all__'


class FAQSerializer(ModelSerializer):

    class Meta:
        model = FAQ
        fields = ('question', 'answer')


class SupportSerializer(ModelSerializer):
    faqs = serializers.SerializerMethodField()

    def get_faqs(self, _):
        serializer = FAQSerializer(
            FAQ.objects.all(), many=True, context=self.context
        )
        return serializer.data

    class Meta:
        model = Support
        fields = ('phone_number', 'faqs')


class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = ('title', 'sub_title', 'description', 'image')


class AdPageSerializer(ModelSerializer):
    ads = serializers.SerializerMethodField()

    def get_ads(self, _):
        serializer = AdSerializer(
            Ad.objects.all(), many=True, context=self.context
        )
        return serializer.data

    class Meta:
        model = Support
        fields = ('ad_phone_number', 'ads')


class AndroidVersionControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersionControl
        fields = ('android_version', 'android_force_update')


class IOSVersionControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersionControl
        fields = ('ios_version', 'ios_force_update')


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ('descriptions')
        
class OfferAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferAgreement
        fields = ('descriptions')