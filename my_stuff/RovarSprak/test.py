import unittest
import rovar_sprak

class TestRovarSprak(unittest.TestCase):

    def test1(self):
        rs = rovar_sprak.RovarSprak('Jag talar Rövarspråket!')
        self.assertEqual(rs.text, 'Jojagog totalolaror Rorövovarorsospoproråkoketot!')

    def test2(self):
        rs = rovar_sprak.RovarSprak()
        rs.text = "I'm speaking Robber's language!"
        self.assertEqual(rs.text, "I'mom sospopeakokinongog Rorobobboberor'sos lolanongoguagoge!")



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRovarSprak)
    unittest.TextTestRunner(verbosity=2).run(suite)