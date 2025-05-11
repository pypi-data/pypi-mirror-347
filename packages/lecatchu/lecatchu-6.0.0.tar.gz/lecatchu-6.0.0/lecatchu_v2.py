import lzma
import hashlib
import json

class Combiner:
	def __init__(self):
		pass
	def combine(self, target, count):
		target = list(target)
		new = target.copy()
		newtarget = target.copy()
		while len(new) < count:
			newpart = []
			for comb1 in newtarget:
				if len(newpart)+len(new) >= count:
					break
				for comb2 in target:
					newpart.append(comb1+comb2)
					if len(newpart)+len(new) >= count:
						break
			newtarget = newpart.copy()
			new += newpart.copy()
			if len(new) >= count:
				break
		return new[:count]

class LeCatchu_Engine:
	def __init__(self, sbox="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890.,_-+"):
		sbox = list(sbox)
		self.combiner = Combiner()
		self.seperator = sbox[0]
		self.fullsbox = sbox
		sbox = sbox[1:]
		if len(sbox) == 0:
			raise ValueError("Sbox entry is too small. Must be at least 2 digits.")
		self.sbox = sbox
		self.coding_sbox = self.combiner.combine(self.sbox, 1114112)
		self.decoding_sbox = {}
		for i, h in enumerate(self.coding_sbox):
			self.decoding_sbox[h] = i
	def encode(self, target):
		if not isinstance(target, str):
			raise ValueError("Encoding input can only be string type object")
		new = []
		for h in target:
			new.append(self.coding_sbox[ord(h)])
		return self.seperator.join(new).encode("utf-8")
	def decode(self, target):
		if not isinstance(target, bytes):
			raise ValueError("Decoding input can only be byte type object")
		target = target.decode("utf-8")
		new = []
		for h in target.split(self.seperator):
			new.append(chr(self.decoding_sbox[h]))
		return "".join(new)
	def process_hash(self, key, xbase=1): 
		okey = str(key)
		hashs = []
		for _ in range(xbase):
			key = hashlib.sha256(str(key).encode(errors="ignore")).hexdigest()
			hashs.append(key) 
			key = key+okey
		return int("".join(hashs), 16)
	def hash_stream(self, key, xbase=1): 
		okey = str(key)
		while True:
			for _ in range(xbase):
				key = hashlib.sha256(str(key).encode(errors="ignore")).hexdigest()
				key+=okey
			yield int(hashlib.sha256(key.encode(errors="ignore")).hexdigest(), 16)
	def encrypt(self, target, key, xbase=1):
		keygen = self.hash_stream(key, xbase)
		return ''.join(chr((ord(c) + next(keygen)) % 1114112) for c in target)
	def decrypt(self, target, key, xbase=1):
		keygen = self.hash_stream(key, xbase)
		return ''.join(chr((ord(c) - next(keygen)) % 1114112) for c in target)
	def encrypts(self, target, keys, xbase=1):
		for key in keys:
			target = self.encrypt(target, key, xbase)
		return target
	def decrypts(self, target, keys, xbase=1):
		for key in keys:
			target = self.decrypt(target, key, xbase)
		return target
	def generate_key(self, seed, xbase=1):
		return self.process_hash(seed, xbase)
	def generate_keys(self, seed, count=32, xbase=1):
		keys = []
		for _ in range(count):
			seed = self.generate_key(seed, xbase)
			keys.append(seed)
		return keys
	def generate_key_opti(self, seed):
		return self.generate_key(seed, xbase=1)
	def generate_key_pro(self, seed):
		return self.generate_key(seed, xbase=40)
	def compress(self, target):
		return lzma.compress(target)
	def decompress(self, target):
		return lzma.decompress(target)
	def lestr(self, target):
		return json.dumps({"": target}, default=repr)
	def leval(self, target):
		return json.loads(target)[""]
	def encode_direct(self, target):
		return target.encode("utf-8", errors="ignore")
	def decode_direct(self, target):
		return target.decode("utf-8", errors="ignore")
