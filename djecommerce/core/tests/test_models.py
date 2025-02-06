from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django_countries.fields import Country
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from core.models import Address, UserProfile, Item, OrderItem, Payment, Coupon, Order
from core.choices import AddressChoices, CategoryChoices, LabelChoices, enum_to_choices

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user)
    
    def test_user_profile_creation(self):
        user = User.objects.create(username='testuser2', password='password1234')
        user_profile = UserProfile.objects.create(user=user)
        self.assertTrue(isinstance(user_profile, UserProfile))
        self.assertEqual(user_profile.__str__(), user.username)

    def test_str_method(self):
        self.assertEqual(str(self.user_profile), self.user.username)

    def test_default_one_click_purchasing(self):
        self.assertFalse(self.user_profile.one_click_purchasing)

    def test_payment_customer_id (self):
        self.user_profile.payment_customer_id = 'cus_12345'
        self.user_profile.save()
        self.assertEqual(self.user_profile.payment_customer_id, 'cus_12345')
   
        
class ItemModelTest(TestCase):

    def setUp(self):
        image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.item = Item.objects.create(
            title="Test Item",
            price=10.0,
            discount_price=5.0,
            category=CategoryChoices.SHIRT.value[0],
            label=LabelChoices.PRIMARY.value[0],
            description="This is a test item.",
            slug="test-item",
            image=image_file
        )

    def test_title_field(self):
        self.item.title = "New Title"
        self.assertEqual(self.item.title, "New Title")

    def test_price_field(self):
        self.item.price = 15.0
        self.item.full_clean()  # This will call the validators
        self.assertEqual(self.item.price, 15.0)

    def test_price_field_negative(self):
        self.item.price = -5.0
        with self.assertRaises(ValidationError):
            self.item.full_clean()

    def test_discount_price_field(self):
        self.item.discount_price = 3.0
        self.item.full_clean()
        self.assertEqual(self.item.discount_price, 3.0)

    def test_discount_price_field_negative(self):
        self.item.discount_price = -1.0
        with self.assertRaises(ValidationError):
            self.item.full_clean()

    def test_category_field(self):
        self.item.category = CategoryChoices.OUTWEAR # Example choice, modify as per your enum
        self.assertEqual(self.item.category, CategoryChoices.OUTWEAR)

    def test_label_field(self):
        self.item.label = LabelChoices.SECONDARY
        self.assertEqual(self.item.label, LabelChoices.SECONDARY)

    def test_slug_field(self):
        self.item.slug = "new-slug"
        self.assertEqual(self.item.slug, "new-slug")

    def test_description_field(self):
        self.item.description = "Updated description."
        self.assertEqual(self.item.description, "Updated description.")

    def test_image_field(self):
        # Assuming that a valid image file has been uploaded, here we just test that the field exists
        self.assertIsNotNone(self.item.image)

    def test_creation_and_retrieval(self):
        item = Item.objects.get(title="Test Item")
        self.assertEqual(item.price, 10.0)
        self.assertEqual(item.discount_price, 5.0)
        self.assertEqual(item.category, CategoryChoices.SHIRT.value[0])
        self.assertEqual(item.label, LabelChoices.PRIMARY.value[0])

    """ def test_get_absolute_url(self):
        expected_url = f"/core/product/{self.item.slug}/"
        self.assertEqual(self.item.get_absolute_url(), expected_url)

    def test_get_add_to_cart_url(self):
        expected_url = f"/core/add-to-cart/{self.item.slug}/"
        self.assertEqual(self.item.get_add_to_cart_url(), expected_url)

    def test_get_remove_from_cart_url(self):
        expected_url = f"/core/remove-from-cart/{self.item.slug}/"
        self.assertEqual(self.item.get_remove_from_cart_url(), expected_url) """

    def test_slug_generation_on_save(self):
        item = Item(title="Another Test Item", price=20.0, category=CategoryChoices.SHIRT, label=LabelChoices.SECONDARY, description="Another test item description.")
        item.save()
        self.assertEqual(item.slug, "another-test-item")


class OrderItemModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.item = Item.objects.create(title='Test Item', price=100.0, discount_price=80.0)
        self.order_item = OrderItem.objects.create(user=self.user, item=self.item, quantity=2)

    def test_str_method(self):
        self.assertEqual(str(self.order_item), '2 x Test Item')

    def test_get_total_item_price(self):
        self.assertEqual(self.order_item.get_total_item_price(), 200.0)

    def test_get_total_discount_item_price(self):
        self.assertEqual(self.order_item.get_total_discount_item_price(), 160.0)

    def test_get_amount_saved(self):
        self.assertEqual(self.order_item.get_amount_saved(), 40.0)

    def test_get_final_price(self):
        self.assertEqual(self.order_item.get_final_price(), 160.0)

    def test_check_constraint(self):
        order_item_invalid = OrderItem(user=self.user, item=self.item, quantity=-1)
        with self.assertRaises(Exception):
            order_item_invalid.save()



User = get_user_model()

class AddressModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.address = Address.objects.create(
            user=self.user,
            street_address='123 Test St',
            apartment_address='Apt 1',
            country='US',
            zip='12345',
            address_type=AddressChoices.SHIPPING.value[0],
            default=True
        )

    def test_address_creation(self):
        address = Address.objects.get(id=self.address.id)
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.street_address, '123 Test St')
        self.assertEqual(address.apartment_address, 'Apt 1')
        self.assertEqual(address.country, Country(code='US'))
        self.assertEqual(address.zip, '12345')
        self.assertEqual(address.address_type, AddressChoices.SHIPPING.value[0])
        self.assertTrue(address.default)

    def test_address_str(self):
        address = Address.objects.get(id=self.address.id)
        self.assertEqual(str(address), 'testuser - Shipping')

    def test_default_value(self):
        address = Address.objects.get(id=self.address.id)
        self.assertTrue(address.default)
        

class PaymentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='12345')
        Payment.objects.create(payment_charge_id='ch_1GpWpQ2eZvKYlo2C2WdzRA2e', user=user, amount=100.0)

    def test_payment_creation(self):
        payment = Payment.objects.get(id=1)
        self.assertEqual(payment.payment_charge_id, 'ch_1GpWpQ2eZvKYlo2C2WdzRA2e')
        self.assertEqual(payment.user.username, 'testuser')
        self.assertEqual(payment.amount, 100.0)

    def test_payment_str(self):
        payment = Payment.objects.get(id=1)
        self.assertEqual(str(payment), 'testuser - 100.0')

#test

class CouponModelTest(TestCase):
    
    def test_coupon_code_validation(self):
        # Valid coupon codes
        valid_codes = ['ABC123', '1234', 'XYZ7890', '123456789012345']
        for code in valid_codes:
            coupon = Coupon(code=code, amount=10.0)
            try:
                coupon.full_clean()  # This will run model validations
            except ValidationError:
                self.fail(f'Validation failed for valid code: {code}')
        
        # Invalid coupon codes
        invalid_codes = ['abc123', '123', 'XYZ78901!', 'TOOLONGCOUPONCODE']
        for code in invalid_codes:
            coupon = Coupon(code=code, amount=10.0)
            with self.assertRaises(ValidationError, msg=f'Validation did not raise for invalid code: {code}'):
                coupon.full_clean()  # This will run model validations

    def test_coupon_amount(self):
        # Valid amounts
        valid_amounts = [0.0, 10.0, 99999999.99]
        for amount in valid_amounts:
            coupon = Coupon(code='VALIDCODE', amount=amount)
            try:
                coupon.full_clean()  # This will run model validations
            except ValidationError:
                self.fail(f'Validation failed for valid amount: {amount}')
        
        # Invalid amounts (optional: add this if you are using DecimalField with validators)
        # invalid_amounts = [-1.0, 100000000.0]
        # for amount in invalid_amounts:
        #     coupon = Coupon(code='VALIDCODE', amount=amount)
        #     with self.assertRaises(ValidationError, msg=f'Validation did not raise for invalid amount: {amount}'):
        #         coupon.full_clean()  # This will run model validations

    def test_coupon_str_method(self):
        coupon = Coupon(code='VALIDCODE', amount=10.0)
        self.assertEqual(str(coupon), 'VALIDCODE')

class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.address = Address.objects.create(
            user=self.user,
            street_address='123 Test St', 
            apartment_address='1A', 
            country='US', 
            zip='12345'
        )
        self.payment = Payment.objects.create(
            payment_charge_id='12345',
            user=self.user,
            amount=100.00
        )
        self.coupon = Coupon.objects.create(
            code='TESTCOUPON',
            amount=10.00
        )
        self.order = Order.objects.create(
            user=self.user,
            ref_code='ABC123',
            ordered_date=timezone.now(),
            shipping_address=self.address,
            billing_address=self.address,
            payment=self.payment,
            coupon=self.coupon,
            ordered=True
        )

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, 'testuser')
        self.assertEqual(self.order.ref_code, 'ABC123')
        self.assertTrue(self.order.ordered)
        self.assertEqual(str(self.order), f"Order ABC123 by testuser - Ordered: True")

    def test_get_total(self):
        image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        item = Item.objects.create(
            title='Test Item',
            price=50.00,
            discount_price=40.00,
            category=CategoryChoices.SHIRT.value[0],
            label=LabelChoices.PRIMARY.value[0],
            slug='test-item',
            description='A test item.',
            image=image_file
        )
        order_item = OrderItem.objects.create(
            user=self.user,
            ordered=True,
            item=item,
            quantity=2
        )
        self.order.items.add(order_item)
        self.assertEqual(self.order.get_total(), 70.00)

        


