import skiff
import os
import pytest
import time


token = os.getenv("DO_TOKEN")
assert token is not None

s = skiff.rig(token)
assert s is not None

# I just want to test stuff, don't judge this code


@pytest.fixture
def droplet(request):
    # for simplicity, this requires that you already have an ssh key uploaded
    # mostly because I don't want any emails
    my_droplet = s.Droplet.create(name="skiff.test", region="nyc1", size="512mb", image=5141286, ssh_keys=[s.Key.all()[0]])
    my_droplet.wait_till_done()
    my_droplet = my_droplet.reload()

    def fin():
        my_droplet.destroy()
        my_droplet.wait_till_done()
        # assert that it's deleted
        with pytest.raises(ValueError):
            s.Droplet.get(my_droplet.id)

    request.addfinalizer(fin)

    return my_droplet


class TestDroplet:
    def test_rename(self, droplet):
        droplet.rename("skiff.rename")
        droplet.wait_till_done()
        assert droplet.name == "skiff.rename"

    def test_reboot(self, droplet):
        droplet.reboot()
        assert droplet.has_action_in_progress()
        droplet.wait_till_done()

    # I'm just going to assume that all of the actions work
    # to keep testing times down and myself sane

    def test_all(self, droplet):
        # depends on droplet so I can test length
        ds = s.Droplet.all()
        assert len(ds) > 0

    def test_kernels(self, droplet):
        assert len(droplet.kernels()) > 0

    # I'm just going to assume that snapshots and backups work as well
    # I don't feel like paying money to test that functionality

    def test_get(self, droplet):
        new_droplet = s.Droplet.get(droplet.id)
        assert new_droplet.id == droplet.id


class TestDomains:
    def test_create(self, droplet):
        droplet.create_domain("mysuperrandomdomainname.com")
        assert s.Domain.get("mysuperrandomdomainname.com") is not None

    def test_all(self):
        assert len(s.Domain.all()) > 0

    def test_record_create(self):
        domain = s.Domain.get("mysuperrandomdomainname.com")
        record = domain.create_record(type="CNAME", name="*", data="@")
        assert record is not None
        record.update("test")
        assert record.name == "test"
        assert record.destroy()

    def test_records(self):
        records = s.Domain.get("mysuperrandomdomainname.com").records()
        assert len(records) > 0

    def test_get(self):
        assert s.Domain.get("mysuperrandomdomainname.com") is not None

    def test_destroy(self, droplet):
        assert s.Domain.get("mysuperrandomdomainname.com").destroy()


class TestImages:
    def test_all(self):
        assert len(s.Image.all()) > 0

    def test_get(self):
        # test string search
        img = s.Image.get("Ubuntu")
        assert img is not None
        # test id search
        id_img = s.Image.get(img.id)
        assert id_img is not None
        # test slug search
        slug_img = s.Image.get(img.slug)
        assert slug_img is not None

        # assert equality
        assert (img.id == id_img.id)
        assert (img.id == slug_img.id)

    # I'm going to assume the update and delete actions work


class TestRegions:
    def test_all(self):
        assert len(s.Region.all()) > 0


class TestSizes:
    def test_all(self):
        assert len(s.Size.all()) > 0
