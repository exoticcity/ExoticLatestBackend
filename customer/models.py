from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.contrib.auth.hashers import make_password
# Create your models here.

class BCCustomer(models.Model):
    No = models.CharField(max_length=110, unique=True)
    Name = models.CharField(max_length=100)
    SearchName = models.CharField(max_length=100)
    Name2 = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Contact = models.CharField(max_length=100)
    PhoneNo = models.CharField(max_length=150)
    TelexNo = models.CharField(max_length=100)
    Blocked = models.CharField(max_length=100)
    DocumentSendingProfile = models.CharField(max_length=100)
    ShiptoCode = models.CharField(max_length=100)
    OurAccountNo = models.CharField(max_length=100)
    TerritoryCode = models.CharField(max_length=100)
    GlobalDimension1Code = models.CharField(max_length=100)
    GlobalDimension2Code = models.CharField(max_length=100)
    ChainName = models.CharField(max_length=100)
    BudgetedAmount = models.IntegerField(default=0)
    CreditLimitLCY = models.IntegerField(default=0)
    CustomerPostingGroup = models.CharField(max_length=100)
    CurrencyCode = models.CharField(max_length=100)
    CustomerPriceGroup = models.CharField(max_length=100)
    LanguageCode = models.CharField(max_length=100)
    RegistrationNumber = models.CharField(max_length=100)
    StatisticsGroup = models.IntegerField(default=0)
    PaymentTermsCode = models.CharField(max_length=100)
    SalespersonCode = models.CharField(max_length=100)
    ShipmentMethodCode = models.CharField(max_length=100)
    PlaceofExport = models.CharField(max_length=100)
    CustomerDiscGroup = models.CharField(max_length=100)
    CountryRegionCode = models.CharField(max_length=100)
    Amount = models.IntegerField(default=0)
    DebitAmount = models.IntegerField(default=0)
    CreditAmount = models.IntegerField(default=0)
    InvoiceAmounts = models.IntegerField(default=0)
    OtherAmountsLCY = models.IntegerField(default=0)
    Comment = models.BooleanField(default=False)
    LastStatementNo = models.IntegerField(default=0)
    Prepayment = models.IntegerField(default=0)
    PartnerType = models.CharField(max_length=100)
    Payments = models.IntegerField(default=0)
    PostCode = models.CharField(max_length=100)
    PrintStatements = models.BooleanField(default=False)
    PricesIncludingVAT = models.BooleanField(default=False)
    ProfitLCY = models.IntegerField(default=0)
    BilltoCustomerNo = models.CharField(max_length=100)
    Priority = models.IntegerField(default=0)
    PaymentMethodCode = models.CharField(max_length=100)
    LastModifiedDateTime = models.DateTimeField()
    GlobalDimension1Filter = models.CharField(max_length=100)
    GlobalDimension2Filter = models.CharField(max_length=100)
    Balance = models.IntegerField(default=0)
    BalanceLCY = models.IntegerField(default=0)
    BalanceDue = models.IntegerField(default=0)
    NetChange = models.IntegerField(default=0)
    NetChangeLCY = models.IntegerField(default=0)
    SalesLCY = models.IntegerField(default=0)
    InvAmountsLCY = models.IntegerField(default=0)
    InvDiscountsLCY = models.IntegerField(default=0)
    NoofInvoices = models.IntegerField(default=0)
    InvoiceDiscCode = models.CharField(max_length=100)
    InvoiceCopies = models.IntegerField(default=0)
    PmtDiscountsLCY = models.IntegerField(default=0)
    PmtToleranceLCY = models.IntegerField(default=0)
    BalanceDueLCY = models.IntegerField(default=0)
    PaymentsLCY = models.IntegerField(default=0)
    CrMemoAmounts = models.IntegerField(default=0)
    CrMemoAmountsLCY = models.IntegerField(default=0)
    FinanceChargeMemoAmounts = models.IntegerField(default=0)
    ShippedNotInvoiced = models.IntegerField(default=0)
    ShippedNotInvoicedLCY = models.IntegerField(default=0)
    ShippingAgentCode = models.CharField(max_length=100)
    ApplicationMethod = models.CharField(max_length=100)
    LocationCode = models.CharField(max_length=100)
    FaxNo = models.CharField(max_length=100)
    VATBusPostingGroup = models.CharField(max_length=100)
    VATRegistrationNo = models.CharField(max_length=100)
    CombineShipments = models.BooleanField(default=False)
    GenBusPostingGroup = models.CharField(max_length=100)
    GLN = models.CharField(max_length=100)
    County = models.CharField(max_length=100)
    EMail = models.EmailField(max_length=100)
    EORINumber = models.CharField(max_length=100)
    UseGLNinElectronicDocument = models.BooleanField(default=False)
    ReminderTermsCode = models.CharField(max_length=100)
    ReminderAmounts = models.IntegerField(default=0)
    ReminderAmountsLCY = models.IntegerField(default=0)
    TaxAreaCode = models.CharField(max_length=100)
    TaxAreaID = models.CharField(max_length=100)
    TaxLiable = models.BooleanField(default=False)
    CurrencyFilter = models.CharField(max_length=100)
    EnterpriseNo = models.CharField(max_length=100)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    addressLine1 = models.CharField(max_length=200, blank=True, null=True)
    addressLine2 = models.CharField(max_length=200, blank=True, null=True)
    region_code = models.CharField(max_length=5, blank=True, null=True)
    language_code = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    enterprise_no = models.CharField(max_length=200, blank=True, null=True)
    CustomerPriceGroup = models.CharField(
        max_length=100, blank=True, null=True)
    Vat = models.CharField(
        max_length=100, blank=True, null=True)
    postalCode = models.CharField(max_length=50, blank=True, null=True)
    phoneNumber = models.CharField(max_length=50, blank=True, null=True)
    mobile_phoneNumber = models.CharField(max_length=50, blank=True, null=True)
    customer_id = models.CharField(max_length=550, unique=True)
    blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'addressLine1',
                       'addressLine2', 'city', 'postalCode', 'phoneNumber']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)

        super(Customer, self).save(*args, **kwargs)