from PIL import Image
from collections import defaultdict
import hashlib
import imagehash
from disjoint_sets import disjoint_sets


class exact_hasher:
    BLOCKSIZE = 65536

    def __init__(self):
        self.hash_dict = defaultdict(list)

    def _hash(self, file_path):
        hasher = hashlib.md5()

        with open(file_path, 'rb') as image_file:
            buf = image_file.read(self.BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = image_file.read(self.BLOCKSIZE)

        key = hasher.hexdigest()
        return key

    def add(self, file_path):
        key = self._hash(file_path)
        self.hash_dict[key].append(file_path)

    def find(self, file_path):
        """
        Returns the key of file_path in hash_dict if it exists
        """
        key = self._hash(file_path)
        if key in self.hash_dict:
            return key
        return None

    def get_hash_dict(self):
        return self.hash_dict


class approx_image_hasher:
    def __init__(self, hash_size=8, hamming_tol=10):
        """
        Utilize disjoint set to track similar images
        """
        self.hamming_tol = hamming_tol
        self.hash_size = hash_size

        self._disjoint_set = disjoint_sets()
        self.parllel_hash_list = []

    def _hash(self, file_path):
        img = Image.open(file_path)
        return imagehash.phash(img, hash_size=self.hash_size)

    def add(self, file_path):
        key = self._hash(file_path)
        self._disjoint_set.add()
        self.parllel_hash_list.append((key, file_path))

        key_ind = len(self.parllel_hash_list)-1

        # check through all keys added so far to union with similar
        for compare_ind, (compare_hash, _) in enumerate(self.parllel_hash_list[:-1]):
            hamming_dist = compare_hash-key
            if hamming_dist <= self.hamming_tol:
                self._disjoint_set.union(key_ind, compare_ind)

    def find(self, file_path):
        """
        Returns what would be the dictionary key for this entry if it was
        created now.

        May not return None even if file_path hasn't been added if there is an
        extremely similar image that has been added such that hashes are the
        same.
        """
        hash_to_find = self._hash(file_path)
        for compare_ind, (compare_hash, _) in enumerate(self.parllel_hash_list):
            if hash_to_find == compare_hash:
                return self._disjoint_set.find(compare_ind)
        return None

    def get_hash_dict(self):
        # Convert current disjoint set into hash_dict format
        # Uses root_ind as key instead of the hash
        hash_dict = defaultdict(list)
        for ind in range(len(self.parllel_hash_list)):
            root_ind = self._disjoint_set.find(ind)
            hash_dict[root_ind].append(self.parllel_hash_list[ind][1])

        return hash_dict
