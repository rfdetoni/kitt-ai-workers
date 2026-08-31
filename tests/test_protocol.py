import unittest
from kitt_workers.protocol import Request, decode_request, encode
class ProtocolTest(unittest.TestCase):
 def test_roundtrip(self):
  req=Request("echo",{"value":"olá"}); parsed=decode_request(encode(req)); self.assertEqual(req.id,parsed.id); self.assertEqual("olá",parsed.payload["value"])
if __name__=="__main__": unittest.main()
