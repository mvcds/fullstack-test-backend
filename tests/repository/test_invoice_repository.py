from datetime import datetime
from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from fullstack_test.domain.invoice import Invoice
from fullstack_test.domain.orm import Base
from fullstack_test.repository.invoice_repository import InvoiceRepository


class TestInvoiceRepository(TestCase):
    engine = create_engine("sqlite:///:memory:")
    session_factory = sessionmaker(bind=engine)
    Base = declarative_base()

    def setUp(self):
        Base.metadata.create_all(self.engine)

        session = self.session_factory()
        invoice = Invoice(
            vendor='Vendor A',
            vendor_tax_registration_number='TAX123456A',
            vendor_bank_details='BANK12345A',
            vendor_address='123 Vendor St, City A',
            billing_address='456 Billing Rd, City B',
            number='INV-123',
            po_number='PO1234A',
            date_of_issue=datetime.now().date(),
            due_date=datetime.now().date(),
            payment_terms=30,
            description='x2 MacBook Pro',
            line_item_details='x2 MacBook Pro',
            pre_tax_amount=14000.00,
            discount=0.0,
            tax_amount=2000.00,
            total_amount=16000.00,
            currency='EUR',
            gl_code='EQ12',
            cost_centre='Equipment',
        )

        session.add(invoice)
        session.commit()
        session.close()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_that_find_all_returns_all_database_objects(self):
        repository = InvoiceRepository(self.session_factory())
        all_invoices = repository.find_all()

        self.assertEqual(1, len(all_invoices))
        self.assertEqual('INV-123', all_invoices[0].number)

    def test_that_find_by_id_returns_an_instance(self):
        repository = InvoiceRepository(self.session_factory())
        invoice = repository.find_by_id(1)

        self.assertEqual('INV-123', invoice.number)

    def test_that_find_by_id_returns_none(self):
        repository = InvoiceRepository(self.session_factory())
        invoice = repository.find_by_id(-1)

        self.assertIsNone(invoice)

    def test_that_update_status_does_its_thing(self):
        invoice_id = 1
        repository = InvoiceRepository(self.session_factory())
        repository.update_status(invoice_id, 'APPROVED')

        updated_invoice = self.session_factory() \
            .query(Invoice) \
            .filter_by(id=invoice_id) \
            .first()

        self.assertEqual('APPROVED', updated_invoice.status)