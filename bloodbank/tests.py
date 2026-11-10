from django.test import TestCase
from django.urls import reverse

from .models import Donor


class DonorPagesTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Find Blood Donors")

    def test_search_filters_by_group_and_all_location_fields(self):
        match = Donor.objects.create(
            name="Matching Donor",
            blood_group="O+",
            contact_number="1111111111",
            country="India",
            state="Karnataka",
            district="Tumkur",
            city="Koratagere",
        )
        Donor.objects.create(
            name="Other Donor",
            blood_group="O+",
            contact_number="2222222222",
            country="India",
            state="Karnataka",
            district="Bengaluru",
            city="Bengaluru",
        )

        response = self.client.get(
            reverse("search_results"),
            {
                "blood_group": "O+",
                "country": "India",
                "state": "Karnataka",
                "district": "Tumkur",
                "city": "Koratagere",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["donors"]), [match])

    def test_registration_saves_donor(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "New Donor",
                "blood_group": "A+",
                "contact_number": "3333333333",
                "country": "India",
                "state": "Karnataka",
                "district": "Tumkur",
                "city": "Koratagere",
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Donor.objects.filter(name="New Donor").exists())

    def test_registration_duplicate_matches_database_constraint(self):
        registration = {
            "name": "Same Name",
            "blood_group": "B+",
            "contact_number": "4444444444",
            "country": "India",
            "state": "Karnataka",
            "district": "Tumkur",
            "city": "Koratagere",
        }
        first_response = self.client.post(reverse("register"), registration)

        registration["city"] = "Bengaluru"
        second_response = self.client.post(reverse("register"), registration)

        self.assertRedirects(first_response, reverse("home"))
        self.assertRedirects(second_response, reverse("home"))
        self.assertEqual(Donor.objects.filter(name="Same Name").count(), 2)

        duplicate_response = self.client.post(reverse("register"), registration)

        self.assertEqual(duplicate_response.status_code, 200)
        self.assertEqual(Donor.objects.filter(name="Same Name").count(), 2)
