import unittest

from game.boxes import Box, Street, Station
from game.user import User


class BoxTest(unittest.TestCase):

    def test_getBoxName(self):
        box1 = Box(25, "street", "box1")
        box2 = Box(86, "station", "box2")
        self.assertEqual(box1.getBoxName(), "box1")
        self.assertEqual(box2.getBoxName(), "box2")

    def test_get_type(self):
        box1 = Box(25, "street", "box1")
        box2 = Box(86, "station", "box2")
        box3 = Box(45, None, "box3")
        self.assertEqual(box1.getType(), "street")
        self.assertEqual(box2.getType(), "station")
        self.assertIsNone(box3.getType())


class StreetTest(unittest.TestCase):

    def test_get_owner(self):
        chloe = User("Chloe",0)
        gildas = User("Gildas",1)
        street1 = Street(12, "street", "test", 25, 22, "yellow")
        street2 = Street(15, "street", "gravelines", 250, 85, "red")
        street3 = Street(17, "street", "dunkerque", 52, 74, "blue", chloe, gildas)
        street2.owner = chloe
        self.assertEqual(street1.getOwner(), None)
        self.assertEqual(street2.getOwner(), chloe)
        self.assertEqual(street3.getOwner(), gildas)

    def test_get_price(self):
        street1 = Street(12, "street", "test", 25, 22, "yellow")
        street2 = Street(15, "street", "gravelines", None, 85, "red")
        street3 = Street(17, "street", "dunkerque", 0, 74, "blue")
        self.assertEqual(street1.getPrice(), 25)
        self.assertEqual(street2.getPrice(), None)
        self.assertEqual(street3.getPrice(), 0)

    def test_get_color(self):
        street1 = Street(12, "street", "test", 25, 22, "yellow")
        street2 = Street(15, "street", "gravelines", 250, 85, "red")
        street3 = Street(17, "street", "dunkerque", 0, 74, None)
        self.assertEqual(street1.getColor(), "yellow")
        self.assertEqual(street2.getColor(), "red")
        self.assertEqual(street3.getColor(), None)

    def test_get_rent(self):
        street1 = Street(12, "street", "test", 25, 22, "yellow")
        street2 = Street(15, "street", "gravelines", 250, None, "red")
        self.assertEqual(street1.getRent(), 22)
        self.assertEqual(street2.getRent(), None)

    def test_get_home(self):
        chloe = User("Chloe",0)
        street1 = Street(12, "street", "test", 25, 22, "yellow")
        street2 = Street(15, "street", "gravelines", 250, None, "red", chloe, chloe, 3)
        self.assertEqual(street1.getHome(), 0)
        self.assertEqual(street2.getHome(), 3)

    def test_set_homes(self):
        chloe = User("Chloe",0)
        street1 = Street(12, "street", "test", 25, 22, "yellow")
        street2 = Street(15, "street", "gravelines", 250, None, "red", chloe, chloe, 3)
        street3 = Street(17, "street", "dunkerque", 326, 58, "red", chloe, chloe, 8)
        street1.setHomes(5)
        street2.setHomes(4)
        street3.setHomes(0)
        self.assertEqual(street1.getHome(), 5)
        self.assertEqual(street2.getHome(), 4)
        self.assertEqual(street3.getHome(), 0)


if __name__ == '__main__':
    unittest.main()
