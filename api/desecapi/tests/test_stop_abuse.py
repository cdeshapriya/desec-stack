from django.conf import settings
from django.core import management

from desecapi import models
from desecapi.tests.base import DomainOwnerTestCase


def block_exists(ip):
    return models.BlockedSubnet.objects.filter(subnet__net_contains=ip).exists()


class StopAbuseCommandTest(DomainOwnerTestCase):
    def setUp(self):
        super().setUp()
        self.create_rr_set(
            self.my_domains[1], ["127.0.0.1", "4.2.2.4"], type="A", ttl=123
        )
        self.create_rr_set(
            self.other_domains[1], ["40.1.1.1", "127.0.0.2"], type="A", ttl=456
        )
        for d in self.my_domains + self.other_domains:
            self.create_rr_set(d, ["ns1.example.", "ns2.example."], type="NS", ttl=456)
            self.create_rr_set(
                d,
                ["ns1.example.", "ns2.example."],
                type="NS",
                ttl=456,
                subname="subname",
            )
            self.create_rr_set(d, ['"foo"'], type="TXT", ttl=456)

    def test_noop(self):
        # test implicit by absence assertPdnsRequests
        management.call_command("stop-abuse")

    def test_remove_rrsets_by_domain_name(self):
        with self.assertRequests(
            self.requests_desec_rr_sets_update(name=self.my_domain.name)
        ):
            management.call_command("stop-abuse", self.my_domain)
        self.assertEqual(
            models.RRset.objects.filter(domain__name=self.my_domain.name).count(), 1
        )  # only NS left
        self.assertEqual(
            set(
                models.RR.objects.filter(
                    rrset__domain__name=self.my_domain.name
                ).values_list("content", flat=True)
            ),
            set(settings.DEFAULT_NS),
        )
        self.assertTrue(block_exists("3.2.2.3"))
        self.assertFalse(block_exists("40.1.1.1"))
        self.assertFalse(block_exists("127.0.0.1"))

    def test_remove_rrsets_by_email(self):
        with self.assertRequests(
            *[self.requests_desec_rr_sets_update(name=d.name) for d in self.my_domains],
            expect_order=False,
        ):
            management.call_command("stop-abuse", self.owner.email)
        self.assertEqual(
            models.RRset.objects.filter(domain__name=self.my_domain.name).count(), 1
        )  # only NS left
        self.assertEqual(
            set(
                models.RR.objects.filter(
                    rrset__domain__name=self.my_domain.name
                ).values_list("content", flat=True)
            ),
            set(settings.DEFAULT_NS),
        )
        self.assertTrue(block_exists("3.2.2.3"))
        self.assertTrue(block_exists("4.2.2.4"))
        self.assertFalse(block_exists("40.1.1.1"))
        self.assertFalse(block_exists("127.0.0.1"))

    def test_disable_user_by_domain_name(self):
        with self.assertRequests(
            self.requests_desec_rr_sets_update(name=self.my_domain.name)
        ):
            management.call_command("stop-abuse", self.my_domain)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.is_active, False)

    def test_disable_user_by_email(self):
        with self.assertRequests(
            *[self.requests_desec_rr_sets_update(name=d.name) for d in self.my_domains],
            expect_order=False,
        ):
            management.call_command("stop-abuse", self.owner.email)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.is_active, False)

    def test_keep_other_owned_domains_name(self):
        with self.assertRequests(
            self.requests_desec_rr_sets_update(name=self.my_domain.name)
        ):
            management.call_command("stop-abuse", self.my_domain)
        self.assertGreater(
            models.RRset.objects.filter(domain__name=self.my_domains[1].name).count(), 1
        )

    def test_dont_keep_other_owned_domains_email(self):
        with self.assertRequests(
            *[self.requests_desec_rr_sets_update(name=d.name) for d in self.my_domains],
            expect_order=False,
        ):
            management.call_command("stop-abuse", self.owner.email)
        self.assertEqual(
            models.RRset.objects.filter(domain__name=self.my_domains[1].name).count(), 1
        )

    def test_only_disable_owner(self):
        with self.assertRequests(
            self.requests_desec_rr_sets_update(name=self.my_domains[0].name),
            self.requests_desec_rr_sets_update(name=self.my_domains[1].name),
            expect_order=False,
        ):
            management.call_command("stop-abuse", self.my_domain, self.owner.email)
        self.my_domain.owner.refresh_from_db()
        self.other_domain.owner.refresh_from_db()
        self.assertEqual(self.my_domain.owner.is_active, False)
        self.assertEqual(self.other_domain.owner.is_active, True)

    def test_disable_owners_by_domain_name(self):
        with self.assertRequests(
            self.requests_desec_rr_sets_update(name=self.my_domain.name),
            self.requests_desec_rr_sets_update(name=self.other_domain.name),
            expect_order=False,
        ):
            management.call_command("stop-abuse", self.my_domain, self.other_domain)
        self.my_domain.owner.refresh_from_db()
        self.other_domain.owner.refresh_from_db()
        self.assertEqual(self.my_domain.owner.is_active, False)
        self.assertEqual(self.other_domain.owner.is_active, False)

    def test_disable_owners_by_email(self):
        with self.assertRequests(
            *[
                self.requests_desec_rr_sets_update(name=d.name)
                for d in self.my_domains + self.other_domains
            ],
            expect_order=False,
        ):
            management.call_command(
                "stop-abuse",
                self.owner.email,
                *[d.owner.email for d in self.other_domains],
            )
        self.my_domain.owner.refresh_from_db()
        self.other_domain.owner.refresh_from_db()
        self.assertEqual(self.my_domain.owner.is_active, False)
        self.assertEqual(self.other_domain.owner.is_active, False)
